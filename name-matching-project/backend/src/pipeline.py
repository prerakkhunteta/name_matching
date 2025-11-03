import pandas as pd
from .preprocess import NamePreprocessor
from .blocking import BlockingStrategy
from .scoring import NameScorer
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

class NameMatchingPipeline:
    def __init__(self, blocking_strategy="metaphone", threshold=80.0):
        self.blocking_strategy = blocking_strategy
        self.threshold = threshold
        
        # Initialize components
        self.preprocessor = NamePreprocessor()
        self.blocker = BlockingStrategy(strategy=blocking_strategy)
        self.scorer = NameScorer()
    
    def process_csv_files(self, file_paths):
        """Process a list of CSV files and find duplicates between them."""
        if len(file_paths) < 2:
            raise ValueError("Need at least two files to compare.")

        # Read and preprocess both dataframes
        df1 = self._read_and_preprocess(file_paths[0])
        df2 = self._read_and_preprocess(file_paths[1])
        
        # Find duplicates
        matches = self._find_duplicates(df1, df2)
        
        # Convert matches to a DataFrame for easier analysis
        matches_df = pd.DataFrame(matches)
        return matches_df

    def _read_and_preprocess(self, file_path):
        """Read a CSV file and apply preprocessing."""
        df = pd.read_csv(file_path)
        # Standardize column names (e.g., lowercase, remove special chars)
        df.columns = [self.preprocessor.standardize_col_name(col) for col in df.columns]
        return df
    
    def _find_duplicates(self, df1, df2):
        """Find duplicate records between two dataframes by comparing all columns"""
        matches = []
        
        # Get common columns between the two dataframes
        common_columns = list(set(df1.columns) & set(df2.columns))
        
        if not common_columns:
            return matches
        
        # Apply blocking to reduce comparisons (use first column as key)
        blocking_column = common_columns[0]
        blocks = self.blocker.create_blocks(df1, df2, blocking_column)
        logging.info(f"Created {len(blocks)} blocks to compare.")
        
        for i, block in enumerate(blocks):
            if (i + 1) % 10 == 0:
                logging.info(f"Processing block {i + 1}/{len(blocks)}...")
            records1 = block['df1_names']
            records2 = block['df2_names']
            
            # Compare records within each block
            for idx1, name1 in records1.items():
                for idx2, name2 in records2.items():
                    # Calculate overall similarity across all common columns
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
    
    def _calculate_overall_similarity(self, record1, record2, columns):
        """Calculate the average similarity score across multiple columns."""
        total_score = 0
        for col in columns:
            total_score += self.scorer.calculate_similarity(
                str(record1[col]), str(record2[col])
            )
        return total_score / len(columns) if columns else 0