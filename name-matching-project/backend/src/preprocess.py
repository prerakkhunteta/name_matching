import pandas as pd
import re
import unicodedata

class NamePreprocessor:
    def __init__(self):
        # Common Hindi name prefixes and suffixes
        self.hindi_prefixes = ['श्री', 'श्रीमती', 'डॉ', 'प्रो', 'कु', 'कुमारी']
        self.hindi_suffixes = ['जी', 'साहब', 'सिंह', 'कुमार', 'देवी']
        
        # Common English name prefixes and suffixes
        self.english_prefixes = ['Mr', 'Mrs', 'Ms', 'Dr', 'Prof', 'Sir', 'Lady']
        self.english_suffixes = ['Jr', 'Sr', 'I', 'II', 'III', 'IV', 'V']
    
    def preprocess_dataframe(self, df, name_column):
        """Preprocess names in a dataframe"""
        df = df.copy()
        
        if name_column in df.columns:
            df[name_column] = df[name_column].astype(str).apply(self.preprocess_name)
        
        return df
    
    def preprocess_name(self, name):
        """Clean and normalize a single name"""
        if pd.isna(name) or name == '':
            return ''
        
        # Convert to string and normalize unicode
        name = str(name).strip()
        name = unicodedata.normalize('NFKC', name)
        
        # Remove prefixes and suffixes
        name = self._remove_prefixes_suffixes(name)
        
        # Clean special characters and extra spaces
        name = re.sub(r'[^\w\s]', ' ', name)
        name = re.sub(r'\s+', ' ', name)
        
        # Convert to lowercase for consistency
        name = name.lower().strip()
        
        return name
    
    def _remove_prefixes_suffixes(self, name):
        """Remove common prefixes and suffixes from names"""
        # Remove Hindi prefixes
        for prefix in self.hindi_prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):].strip()
        
        # Remove Hindi suffixes
        for suffix in self.hindi_suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)].strip()
        
        # Remove English prefixes
        for prefix in self.english_prefixes:
            if name.lower().startswith(prefix.lower()):
                name = name[len(prefix):].strip()
        
        # Remove English suffixes
        for suffix in self.english_suffixes:
            if name.lower().endswith(suffix.lower()):
                name = name[:-len(suffix)].strip()
        
        return name
    
    def normalize_hindi_names(self, name):
        """Additional normalization for Hindi names"""
        # Remove common Hindi honorifics
        hindi_honorifics = ['जी', 'साahab', 'सिंह', 'कुमार', 'देवी', 'बाई']
        for honorific in hindi_honorifics:
            name = name.replace(honorific, '').strip()
        
        return name
    
    def normalize_english_names(self, name):
        """Additional normalization for English names"""
        # Remove common English titles
        english_titles = ['Mr', 'Mrs', 'Ms', 'Dr', 'Prof', 'Sir', 'Lady', 'Lord']
        for title in english_titles:
            name = re.sub(rf'\b{title}\b', '', name, flags=re.IGNORECASE).strip()
        
        return name

    # THIS IS THE NEW FUNCTION THAT FIXES THE ERROR
    def standardize_col_name(self, col_name):
        """Standardizes a column name to a consistent format."""
        if not isinstance(col_name, str):
            return ''
        col_name = col_name.lower()
        # Replace any non-alphanumeric characters with an underscore
        col_name = re.sub(r'[^a-z0-9]+', '_', col_name)
        # Remove leading/trailing underscores
        col_name = col_name.strip('_')
        return col_name