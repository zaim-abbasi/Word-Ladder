from typing import Set, Dict, Optional
from collections import defaultdict

class WordGraph:
    def __init__(self):
        # storing all valid words from dictionary
        self.word_list = set()
        # making connections between words
        self.word_connections = defaultdict(set)
        # remembering where each word came from
        self.word_parents = {}
        
    def load_words(self, filename: str) -> None:
        try:
            # reading words from file and making them lowercase, simple stuff
            with open(filename, 'r') as file:
                self.word_list = {word.strip().lower() for word in file if word.strip()}
        except FileNotFoundError:
            print(f"error: could not find file {filename}")
            self.word_list = set()
    
    def find_similar_words(self, word: str) -> Set[str]:
        similar_words = set()
        # trying to change each letter one by one
        for position in range(len(word)):
            # trying every possible letter
            for new_letter in 'abcdefghijklmnopqrstuvwxyz':
                # no point using same letter, right?
                if new_letter != word[position]:
                    # making new word by changing just one letter
                    changed_word = word[:position] + new_letter + word[position+1:]
                    # if it's a real word, add it to our list
                    if changed_word in self.word_list:
                        similar_words.add(changed_word)
        return similar_words
    
    def build_word_network(self) -> None:
        # clearing old stuff first
        self.word_connections.clear()
        self.word_parents.clear()
        
        # grouping words by length to make life easier
        length_groups = defaultdict(set)
        for word in self.word_list:
            length_groups[len(word)].add(word)
        
        # connecting similar words together
        for length, words in length_groups.items():
            for word in words:
                similar_words = self.find_similar_words(word)
                for similar_word in similar_words:
                    # only connect if word doesn't have parent already
                    if similar_word not in self.word_parents:
                        self.word_connections[word].add(similar_word)
                        self.word_parents[similar_word] = word
    
    def get_connected_words(self, word: str) -> Set[str]:
        connected_words = set()
        
        # getting words we can reach from here
        if word in self.word_connections:
            connected_words.update(self.word_connections[word])
        
        # getting word we came from
        if word in self.word_parents:
            connected_words.add(self.word_parents[word])
        
        return connected_words
    
    def get_neighbors(self, word: str) -> Set[str]:
        # getting all connected words for search algorithms
        return self.get_connected_words(word)
    
    def get_path_to_start(self, word: str) -> list[str]:
        path = [word]
        current_word = word
        
        # following the breadcrumbs back home
        while current_word in self.word_parents:
            current_word = self.word_parents[current_word]
            path.append(current_word)
        
        return path
    
    def find_possible_words(self, start: str, target: str) -> Set[str]:
        visited_words = set()
        words_to_check = [start]
        
        # checking each word and its friends
        while words_to_check:
            current_word = words_to_check.pop(0)
            if current_word not in visited_words:
                visited_words.add(current_word)
                # adding connected words to check later
                for connected_word in self.get_connected_words(current_word):
                    if connected_word not in visited_words:
                        words_to_check.append(connected_word)
        
        return visited_words
    
    def is_valid_word(self, word: str) -> bool:
        # checking if word exists in dictionary
        return word.lower() in self.word_list
    
    def word_exists(self, word: str) -> bool:
        # alias for is_valid_word for compatibility
        return self.is_valid_word(word)
    
    def count_words(self) -> int:
        return len(self.word_list)
    
    def count_connections(self) -> int:
        parent_links = len(self.word_parents)
        direct_links = sum(len(connections) for connections in self.word_connections.values())
        return parent_links + direct_links