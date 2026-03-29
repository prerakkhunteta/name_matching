import difflib
import re
from typing import Tuple

class NameScorer:
    def __init__(self):
        self.algorithms = {
            "levenshtein": self._levenshtein_similarity,
            "jaro_winkler": self._jaro_winkler_similarity,
            "sequence_matcher": self._sequence_matcher_similarity,
            "cosine": self._cosine_similarity,
            "hybrid": self._hybrid_similarity
        }
    
    def calculate_similarity(self, name1: str, name2: str, algorithm: str = "hybrid") -> float:
        if algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        clean_name1 = self._clean_name(name1)
        clean_name2 = self._clean_name(name2)
        
        if not clean_name1 or not clean_name2:
            return 0.0
        
        return self.algorithms[algorithm](clean_name1, clean_name2)
    
    def _clean_name(self, name: str) -> str:
        if not name:
            return ""
        name = str(name).lower().strip()
        name = re.sub(r'\s+', ' ', name)
        return name
    
    def _levenshtein_similarity(self, name1: str, name2: str) -> float:
        if name1 == name2:
            return 100.0
        
        distance = self._levenshtein_distance(name1, name2)
        max_len = max(len(name1), len(name2))
        if max_len == 0:
            return 100.0
        
        similarity = ((max_len - distance) / max_len) * 100
        return max(0.0, similarity)
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _jaro_winkler_similarity(self, name1: str, name2: str) -> float:
        if name1 == name2:
            return 100.0
        
        jaro_sim = self._jaro_similarity(name1, name2)
        prefix_len = self._common_prefix_length(name1, name2)
        winkler_sim = jaro_sim + (0.1 * prefix_len * (1 - jaro_sim))
        
        return min(100.0, winkler_sim * 100)
    
    def _jaro_similarity(self, s1: str, s2: str) -> float:
        if s1 == s2:
            return 1.0
        
        if len(s1) == 0 or len(s2) == 0:
            return 0.0
        
        match_distance = (max(len(s1), len(s2)) // 2) - 1
        if match_distance < 0:
            match_distance = 0
        
        s1_matches = [False] * len(s1)
        s2_matches = [False] * len(s2)
        
        matches = 0
        transpositions = 0
        
        for i in range(len(s1)):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len(s2))
            
            for j in range(start, end):
                if s2_matches[j]:
                    continue
                if s1[i] == s2[j]:
                    s1_matches[i] = True
                    s2_matches[j] = True
                    matches += 1
                    break
        
        if matches == 0:
            return 0.0
        
        k = 0
        for i in range(len(s1)):
            if not s1_matches[i]:
                continue
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1
        
        jaro_sim = (matches / len(s1) + matches / len(s2) + (matches - transpositions / 2) / matches) / 3
        return jaro_sim
    
    def _common_prefix_length(self, s1: str, s2: str) -> int:
        prefix_len = 0
        for i in range(min(len(s1), len(s2))):
            if s1[i] == s2[i]:
                prefix_len += 1
            else:
                break
        return min(prefix_len, 4)
    
    def _sequence_matcher_similarity(self, name1: str, name2: str) -> float:
        if name1 == name2:
            return 100.0
        similarity = difflib.SequenceMatcher(None, name1, name2).ratio()
        return similarity * 100
    
    def _cosine_similarity(self, name1: str, name2: str) -> float:
        if name1 == name2:
            return 100.0
        
        bigrams1 = self._get_character_bigrams(name1)
        bigrams2 = self._get_character_bigrams(name2)
        
        if not bigrams1 or not bigrams2:
            return 0.0
        
        intersection = set(bigrams1.keys()) & set(bigrams2.keys())
        dot_product = sum(bigrams1[bg] * bigrams2[bg] for bg in intersection)
        
        magnitude1 = sum(count ** 2 for count in bigrams1.values()) ** 0.5
        magnitude2 = sum(count ** 2 for count in bigrams2.values()) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        cosine_sim = dot_product / (magnitude1 * magnitude2)
        return cosine_sim * 100
    
    def _get_character_bigrams(self, text: str) -> dict:
        bigrams = {}
        for i in range(len(text) - 1):
            bigram = text[i:i+2]
            bigrams[bigram] = bigrams.get(bigram, 0) + 1
        return bigrams
    
    def _hybrid_similarity(self, name1: str, name2: str) -> float:
        if name1 == name2:
            return 100.0
        
        levenshtein_sim = self._levenshtein_similarity(name1, name2)
        jaro_winkler_sim = self._jaro_winkler_similarity(name1, name2)
        sequence_sim = self._sequence_matcher_similarity(name1, name2)
        cosine_sim = self._cosine_similarity(name1, name2)
        
        weights = [0.3, 0.3, 0.2, 0.2]
        hybrid_sim = (
            levenshtein_sim * weights[0] +
            jaro_winkler_sim * weights[1] +
            sequence_sim * weights[2] +
            cosine_sim * weights[3]
        )
        
        return hybrid_sim
