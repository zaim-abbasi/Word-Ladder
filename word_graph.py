from typing import Set, Dict, List
from collections import defaultdict

class WordGraph:
    def __init__(self):
        self.words: Set[str] = set()
        self.graph: Dict[str, Set[str]] = defaultdict(set)
        
    def load_words(self, filename: str) -> None:
        """Load words from a file into the word set."""
        try:
            with open(filename, 'r') as file:
                # Strip whitespace and convert to lowercase for consistency
                self.words = {word.strip().lower() for word in file if word.strip()}
        except FileNotFoundError:
            print(f"Error: Could not find file {filename}")
            self.words = set()
    
    def find_neighbors(self, word: str) -> Set[str]:
        """Find all valid words that differ by exactly one letter."""
        neighbors = set()
        # Try changing each position in the word
        for i in range(len(word)):
            # Try every possible letter replacement
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != word[i]:
                    # Create new word with one letter changed
                    new_word = word[:i] + c + word[i+1:]
                    # Check if it's a valid word in our dictionary
                    if new_word in self.words:
                        neighbors.add(new_word)
        return neighbors
    
    def build_graph(self) -> None:
        """Build the graph by connecting all words to their valid neighbors."""
        # Clear existing graph
        self.graph.clear()
        
        # For each word, find and store its neighbors
        for word in self.words:
            neighbors = self.find_neighbors(word)
            self.graph[word].update(neighbors)
            # Add bidirectional connections
            for neighbor in neighbors:
                self.graph[neighbor].add(word)
    
    def get_neighbors(self, word: str) -> Set[str]:
        """Get all neighbors for a given word."""
        return self.graph.get(word, set())
    
    def word_exists(self, word: str) -> bool:
        """Check if a word exists in the dictionary."""
        return word in self.words
    
    def get_word_count(self) -> int:
        """Get the total number of words in the graph."""
        return len(self.words)
    
    def get_edge_count(self) -> int:
        """Get the total number of edges (connections) in the graph."""
        # Divide by 2 because each edge is counted twice (bidirectional)
        return sum(len(neighbors) for neighbors in self.graph.values()) // 2