import pandas as pd
try:
    from .preprocess import NamePreprocessor
    from .blocking import BlockingStrategy
    from .scoring import NameScorer
except ImportError:
    from preprocess import NamePreprocessor
    from blocking import BlockingStrategy
    from scoring import NameScorer
import logging

logging.basicConfig(level=logging.INFO)

class NameMatchingPipeline:
    def __init__(self, blocking_strategy="metaphone", threshold=80.0):
        self.blocking_strategy = blocking_strategy
        self.threshold = threshold
        self.preprocessor = NamePreprocessor()
        self.blocker = BlockingStrategy(strategy=blocking_strategy)
        self.scorer = NameScorer()
    
    def process_csv_files(self, file_paths):
        if len(file_paths) < 2:
            raise ValueError("Need at least two files to compare.")

        df1 = self._read_and_preprocess(file_paths[0])
        df2 = self._read_and_preprocess(file_paths[1])
        matches = self._find_duplicates(df1, df2)
        matches_df = pd.DataFrame(matches)
        return matches_df

    def _read_and_preprocess(self, file_path):
        df = pd.read_csv(file_path)
        df.columns = [self.preprocessor.standardize_col_name(col) for col in df.columns]
        return df
    
    def _find_duplicates(self, df1, df2):
        matches = []
        common_columns = list(set(df1.columns) & set(df2.columns))
        
        if not common_columns:
            return matches
        
        blocking_column = self._choose_blocking_column(common_columns)
        blocks = self.blocker.create_blocks(df1, df2, blocking_column)
        logging.info(f"Created {len(blocks)} blocks using column '{blocking_column}' to compare.")
        
        for i, block in enumerate(blocks):
            if (i + 1) % 10 == 0:
                logging.info(f"Processing block {i + 1}/{len(blocks)}...")
            records1 = block['df1_names']
            records2 = block['df2_names']
            
            for idx1, name1 in records1.items():
                for idx2, name2 in records2.items():
                    overall_score = self._calculate_overall_similarity(
                        df1.loc[idx1], df2.loc[idx2], common_columns
                    )
                    
                    if overall_score >= self.threshold:
                        match = {
                            'id1': idx1,
                            'id2': idx2,
                            'record1': df1.loc[idx1].to_dict(),
                            'record2': df2.loc[idx2].to_dict(),
                            'similarity_score': overall_score,
                            'blocking_key': block['key'],
                            'matching_columns': common_columns
                        }
                        matches.append(match)
        
        return matches
    
    def _choose_blocking_column(self, common_columns):
        name_keywords = ['name', 'full_name', 'fullname', 'first_name', 'firstname', 'last_name', 'lastname']
        
        for keyword in name_keywords:
            if keyword in common_columns:
                return keyword
        
        for keyword in name_keywords:
            for col in common_columns:
                if keyword in col.lower():
                    return col
        
        non_date_columns = []
        for col in common_columns:
            col_lower = col.lower()
            if not any(date_word in col_lower for date_word in ['date', 'dob', 'birth', 'time', 'year', 'id', 'number']):
                non_date_columns.append(col)
        
        return non_date_columns[0] if non_date_columns else common_columns[0]
    
    def _calculate_overall_similarity(self, record1, record2, columns):
        total_score = 0
        for col in columns:
            total_score += self.scorer.calculate_similarity(
                str(record1[col]), str(record2[col])
            )
        return total_score / len(columns) if columns else 0