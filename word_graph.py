from typing import Set, Dict, List
from collections import defaultdict

class WordGraph:
    def __init__(self):
        self.words: Set[str] = set()
        self.graph: Dict[str, Set[str]] = defaultdict(set)
        
    def load_words(self, filename: str) -> None:
        try:
            with open(filename, 'r') as file:
                self.words = {word.strip().lower() for word in file if word.strip()}
        except FileNotFoundError:
            print(f"Error: Could not find file {filename}")
            self.words = set()
    
    def find_neighbors(self, word: str) -> Set[str]:
        neighbors = set()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != word[i]:
                    new_word = word[:i] + c + word[i+1:]
                    if new_word in self.words:
                        neighbors.add(new_word)
        return neighbors
    
    def build_graph(self) -> None:
        self.graph.clear()
        
        for word in self.words:
            neighbors = self.find_neighbors(word)
            self.graph[word].update(neighbors)
            for neighbor in neighbors:
                self.graph[neighbor].add(word)
    
    def get_neighbors(self, word: str) -> Set[str]:
        return self.graph.get(word, set())
    
    def word_exists(self, word: str) -> bool:
        return word in self.words
    
    def get_word_count(self) -> int:
        return len(self.words)
    
    def get_edge_count(self) -> int:
        return sum(len(neighbors) for neighbors in self.graph.values()) // 2