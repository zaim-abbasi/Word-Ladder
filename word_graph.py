from typing import Set, Dict, Optional
from collections import defaultdict

class WordGraph:
    def __init__(self):
        # store all valid words
        self.words = set()
        # store word connections like a tree
        self.graph = defaultdict(set)
        # keep track of parent words
        self.parent = {}
        
    def load_words(self, filename: str) -> None:
        """load words from a file into our dictionary"""
        try:
            with open(filename, 'r') as file:
                # read each word, make it lowercase, and add to set
                self.words = {word.strip().lower() for word in file if word.strip()}
        except FileNotFoundError:
            print(f"error: could not find file {filename}")
            self.words = set()
    
    def find_neighbors(self, word: str) -> Set[str]:
        """find all valid words that differ by one letter"""
        neighbors = set()
        # try changing each letter position
        for i in range(len(word)):
            # try each possible letter
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                if letter != word[i]:
                    # make new word by changing one letter
                    new_word = word[:i] + letter + word[i+1:]
                    # add if it's a valid word
                    if new_word in self.words:
                        neighbors.add(new_word)
        return neighbors
    
    def build_graph(self) -> None:
        """build word connections in a tree-like structure"""
        # clear old connections
        self.graph.clear()
        self.parent.clear()
        
        # group words by length for better organization
        words_by_length = defaultdict(set)  # changed from list to set
        for word in self.words:
            words_by_length[len(word)].add(word)
        
        # build connections for each word length group
        for length, words in words_by_length.items():
            for word in words:
                # find neighbors but only connect to words we haven't seen
                neighbors = self.find_neighbors(word)
                for neighbor in neighbors:
                    # only add connection if neighbor isn't connected yet
                    if neighbor not in self.parent:
                        self.graph[word].add(neighbor)
                        self.parent[neighbor] = word
    
    def get_neighbors(self, word: str) -> Set[str]:
        """get all words connected to this word"""
        neighbors = set()
        
        # get children (words we connect to)
        if word in self.graph:
            neighbors.update(self.graph[word])
            
        # get parent (word that connects to us)
        if word in self.parent:
            neighbors.add(self.parent[word])
            
        return neighbors
    
    def get_path_to_root(self, word: str) -> list[str]:
        """get path from word back to its root word"""
        path = [word]
        current = word
        
        # follow parent pointers back to root
        while current in self.parent:
            current = self.parent[current]
            path.append(current)
            
        return path
    
    def get_transformation_tree(self, start: str, target: str) -> Set[str]:
        """get all words that could be part of the transformation"""
        # do a breadth-first search to find all possible words
        visited = set()
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                # add all neighbors to queue
                for neighbor in self.get_neighbors(current):
                    if neighbor not in visited:
                        queue.append(neighbor)
                        
        return visited
    
    def word_exists(self, word: str) -> bool:
        """check if a word is in our dictionary"""
        return word in self.words
    
    def get_word_count(self) -> int:
        """count how many words we have"""
        return len(self.words)
    
    def get_edge_count(self) -> int:
        """count how many connections exist between words"""
        # count parent connections
        parent_count = len(self.parent)
        # count direct connections
        direct_count = sum(len(neighbors) for neighbors in self.graph.values())
        return parent_count + direct_count