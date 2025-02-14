from typing import Optional, List, Tuple, Dict
from word_graph import WordGraph
from search import SearchAlgorithms
import random

class WordLadderGame:
    def __init__(self):
        self.word_graph = WordGraph()
        self.search = None
        self.current_word = None
        self.target_word = None
        self.moves = []
        self.best_path = None
        self.difficulty = "beginner"
        self.score = 0
        self.banned_words = set()
        self.move_limit = 10
        self.algorithm_stats = {}
        self.selected_algorithm = 'A*'
        
    def initialize_game(self, dictionary_path: str):
        self.word_graph.load_words(dictionary_path)
        self.word_graph.build_graph()
        self.search = SearchAlgorithms(self.word_graph)
        
    def set_algorithm(self, algorithm: str):
        if algorithm in ['BFS', 'UCS', 'A*']:
            self.selected_algorithm = algorithm
            if self.current_word and self.target_word:
                self.best_path = self.calculate_best_path()
    
    def set_difficulty(self, difficulty: str):
        self.difficulty = difficulty.lower()
        
        # Adjust game settings based on difficulty
        if self.difficulty == "beginner":
            self.move_limit = 10
            self.banned_words.clear()
        elif self.difficulty == "advanced":
            self.move_limit = 15
            self.banned_words.clear()
        elif self.difficulty == "challenge":
            self.move_limit = 12
            # Select random banned words for challenge mode
            word_list = list(self.word_graph.words)
            self.banned_words = set(random.sample([w for w in word_list if len(w) > 4], 5))
        
        # Start new game with appropriate word pair
        self.start_new_game_for_difficulty()
        
    def get_word_pair_for_difficulty(self):
        word_list = list(self.word_graph.words)
        
        if self.difficulty == "beginner":
            # For beginner, use 3-4 letter words
            valid_words = [w for w in word_list if 3 <= len(w) <= 4]
            start_word = random.choice(valid_words)
            
            # Find potential target words that are reachable
            potential_targets = []
            for target in valid_words:
                if target != start_word:
                    path, _ = self.search.astar(start_word, target)
                    if path and 3 <= len(path) <= 5:  # Keep it simple for beginners
                        potential_targets.append(target)
            
            target_word = random.choice(potential_targets) if potential_targets else random.choice(valid_words)
            
        elif self.difficulty == "advanced":
            # For advanced, use 4-6 letter words
            valid_words = [w for w in word_list if 4 <= len(w) <= 6]
            start_word = random.choice(valid_words)
            
            # Find target words that require more steps
            potential_targets = []
            for target in valid_words:
                if target != start_word:
                    path, _ = self.search.astar(start_word, target)
                    if path and 5 <= len(path) <= 8:  # More challenging
                        potential_targets.append(target)
            
            target_word = random.choice(potential_targets) if potential_targets else random.choice(valid_words)
            
        else:  # Challenge mode
            # Use longer words and ensure they're not banned
            valid_words = [w for w in word_list if len(w) >= 5 and w not in self.banned_words]
            start_word = random.choice(valid_words)
            
            # Find complex paths avoiding banned words
            potential_targets = []
            for target in valid_words:
                if target != start_word:
                    path, _ = self.search.astar(start_word, target)
                    if path and 6 <= len(path) <= 10:  # Complex transformations
                        valid_path = all(word not in self.banned_words for word in path)
                        if valid_path:
                            potential_targets.append(target)
            
            target_word = random.choice(potential_targets) if potential_targets else random.choice(valid_words)
        
        return start_word, target_word
        
    def start_new_game_for_difficulty(self):
        start_word, target_word = self.get_word_pair_for_difficulty()
        return self.start_new_game(start_word, target_word)
        
    def is_word_valid(self, word: str):
        word = word.lower()
        return (self.word_graph.word_exists(word) and 
                word not in self.banned_words)
        
    def is_valid_move(self, word: str):
        if not self.is_word_valid(word):
            return False
        if len(self.moves) >= self.move_limit:
            return False
        return word in self.word_graph.get_neighbors(self.current_word)
        
    def get_algorithm_comparison(self):
        results = {}
        algorithms = {
            'BFS': self.search.bfs,
            'UCS': self.search.ucs,
            'A*': self.search.astar
        }
        
        for name, algorithm in algorithms.items():
            path, costs = algorithm(self.current_word, self.target_word)
            if path is not None:
                results[name] = {
                    'path': path,
                    'costs': costs
                }
                
        return results
        
    def get_hint(self):
        if not self.best_path:
            return None, "No solution exists!"
            
        try:
            current_index = self.best_path.index(self.current_word)
        except ValueError:
            new_path, costs = getattr(self.search, self.selected_algorithm.lower())(
                self.current_word, self.target_word
            )
            if not new_path:
                return None, "No valid path found from current position!"
            self.best_path = new_path
            current_index = 0

        if current_index >= len(self.best_path) - 1:
            return None, "You're already at the target word!"
            
        next_word = self.best_path[current_index + 1]
        
        current_path = self.best_path[current_index:]
        g_cost = len(current_path) - 1
        h_cost = self.search.h_cost(self.current_word, self.target_word)
        f_cost = g_cost + h_cost
        
        hint_message = (
            f"Using {self.selected_algorithm}:\n"
            f"Current cost: {g_cost}\n"
            f"Estimated remaining: {h_cost}\n"
            f"Total estimated cost: {f_cost}\n"
            f"Suggested next word: '{next_word}'"
        )
            
        return next_word, hint_message
        
    def calculate_best_path(self):
        algorithm_paths = self.get_algorithm_comparison()
        
        self.algorithm_stats = {
            name: {
                'path': info['path'],
                'length': len(info['path']),
                'costs': info['costs']
            }
            for name, info in algorithm_paths.items()
        }
        
        if self.selected_algorithm in algorithm_paths:
            return algorithm_paths[self.selected_algorithm]['path']
        
        valid_paths = [info['path'] for info in algorithm_paths.values()]
        return min(valid_paths, key=len) if valid_paths else None
        
    def calculate_score(self):
        if not self.best_path:
            return 0
            
        optimal_moves = len(self.best_path) - 1
        actual_moves = len(self.moves) - 1
        
        if actual_moves == 0:
            return 0
            
        remaining_moves = self.move_limit - actual_moves
        
        base_score = min(1000 * (optimal_moves / actual_moves), 1000)
        move_bonus = remaining_moves * 100
        
        multipliers = {
            "beginner": 1.0,
            "advanced": 1.5,
            "challenge": 2.0
        }
        
        return int((base_score + move_bonus) * multipliers.get(self.difficulty, 1.0))
        
    def start_new_game(self, start_word: str, target_word: str):
        start_word = start_word.lower()
        target_word = target_word.lower()
        
        if not (self.is_word_valid(start_word) and self.is_word_valid(target_word)):
            return False
            
        self.current_word = start_word
        self.target_word = target_word
        self.moves = [start_word]
        self.best_path = self.calculate_best_path()
        self.score = 0
        self.algorithm_stats = {}
        return True
        
    def make_move(self, new_word: str):
        new_word = new_word.lower()
        if not self.is_valid_move(new_word):
            return False
            
        self.current_word = new_word
        self.moves.append(new_word)
        return True
        
    def is_solved(self):
        if self.current_word == self.target_word:
            self.score = self.calculate_score()
            return True
        return False
        
    def get_minimum_moves(self):
        return len(self.best_path) - 1 if self.best_path else 0
        
    def get_current_moves(self):
        return len(self.moves) - 1
        
    def get_remaining_moves(self):
        return self.move_limit - self.get_current_moves()