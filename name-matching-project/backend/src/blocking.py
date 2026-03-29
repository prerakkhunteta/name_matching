import pandas as pd
import re
from metaphone import doublemetaphone

class BlockingStrategy:
    def __init__(self, strategy="metaphone"):
        self.strategy = strategy
        self.strategies = {
            "metaphone": self._metaphone_blocking,
            "first_char": self._first_char_blocking,
            "length": self._length_blocking,
            "soundex": self._soundex_blocking
        }
    
    def create_blocks(self, df1, df2, name_column):
        if self.strategy not in self.strategies:
            raise ValueError(f"Unknown blocking strategy: {self.strategy}")
        return self.strategies[self.strategy](df1, df2, name_column)
    
    def _metaphone_blocking(self, df1, df2, name_column):
        blocks = []
        df1_metaphones = self._get_metaphone_codes(df1, name_column)
        df2_metaphones = self._get_metaphone_codes(df2, name_column)
        common_codes = set(df1_metaphones.keys()) & set(df2_metaphones.keys())
        
        for code in common_codes:
            block = {
                'key': f"metaphone_{code}",
                'df1_names': df1_metaphones[code],
                'df2_names': df2_metaphones[code]
            }
            blocks.append(block)
        return blocks
    
    def _get_metaphone_codes(self, df, name_column):
        metaphone_dict = {}
        for idx, name in df[name_column].items():
            if pd.isna(name) or name == '':
                continue
            
            primary, secondary = doublemetaphone(str(name))
            code = primary if primary else secondary
            
            if code:
                if code not in metaphone_dict:
                    metaphone_dict[code] = {}
                metaphone_dict[code][idx] = name
        return metaphone_dict
    
    def _first_char_blocking(self, df1, df2, name_column):
        blocks = []
        df1_chars = self._get_first_chars(df1, name_column)
        df2_chars = self._get_first_chars(df2, name_column)
        common_chars = set(df1_chars.keys()) & set(df2_chars.keys())
        
        for char in common_chars:
            block = {
                'key': f"first_char_{char}",
                'df1_names': df1_chars[char],
                'df2_names': df2_chars[char]
            }
            blocks.append(block)
        return blocks
    
    def _get_first_chars(self, df, name_column):
        char_dict = {}
        for idx, name in df[name_column].items():
            if pd.isna(name) or name == '':
                continue
            
            first_char = str(name)[0].lower()
            if first_char.isalpha():
                if first_char not in char_dict:
                    char_dict[first_char] = {}
                char_dict[first_char][idx] = name
        return char_dict
    
    def _length_blocking(self, df1, df2, name_column):
        blocks = []
        length_ranges = [(1, 5), (6, 10), (11, 15), (16, 20), (21, 30)]
        
        for min_len, max_len in length_ranges:
            df1_names = self._get_names_by_length(df1, name_column, min_len, max_len)
            df2_names = self._get_names_by_length(df2, name_column, min_len, max_len)
            
            if df1_names and df2_names:
                block = {
                    'key': f"length_{min_len}_{max_len}",
                    'df1_names': df1_names,
                    'df2_names': df2_names
                }
                blocks.append(block)
        return blocks
    
    def _get_names_by_length(self, df, name_column, min_len, max_len):
        names = {}
        for idx, name in df[name_column].items():
            if pd.isna(name) or name == '':
                continue
            name_len = len(str(name))
            if min_len <= name_len <= max_len:
                names[idx] = name
        return names
    
    def _soundex_blocking(self, df1, df2, name_column):
        blocks = []
        df1_soundex = self._get_soundex_codes(df1, name_column)
        df2_soundex = self._get_soundex_codes(df2, name_column)
        common_codes = set(df1_soundex.keys()) & set(df2_soundex.keys())
        
        for code in common_codes:
            block = {
                'key': f"soundex_{code}",
                'df1_names': df1_soundex[code],
                'df2_names': df2_soundex[code]
            }
            blocks.append(block)
        return blocks
    
    def _get_soundex_codes(self, df, name_column):
        soundex_dict = {}
        for idx, name in df[name_column].items():
            if pd.isna(name) or name == '':
                continue
            code = self._simple_soundex(str(name))
            if code:
                if code not in soundex_dict:
                    soundex_dict[code] = {}
                soundex_dict[code][idx] = name
        return soundex_dict
    
    def _simple_soundex(self, name):
        if not name:
            return ""
        
        soundex_rules = {
            'b': '1', 'f': '1', 'p': '1', 'v': '1',
            'c': '2', 'g': '2', 'j': '2', 'k': '2', 'q': '2', 's': '2', 'x': '2', 'z': '2',
            'd': '3', 't': '3',
            'l': '4',
            'm': '5', 'n': '5',
            'r': '6'
        }
        
        result = name[0].upper()
        for char in name[1:].lower():
            if char in soundex_rules:
                code = soundex_rules[char]
                if result[-1] != code:
                    result += code
        
        result = result.ljust(4, '0')[:4]
        return result  