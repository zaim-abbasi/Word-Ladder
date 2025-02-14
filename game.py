# Word Ladder Game - A fun word transformation puzzle
# Author: Your Name
# Created: 2024

from typing import Optional, List, Tuple, Dict
from word_graph import WordGraph
from search import SearchAlgorithms
import random

class WordLadderGame:
    def __init__(self):
        # Core game components
        self.word_graph = WordGraph()
        self.search = None
        
        # Current game state
        self.current_word = None
        self.target_word = None
        self.moves = []
        self.best_path = None
        
        # Game settings
        self.difficulty = "beginner"
        self.score = 0
        self.banned_words = set()
        self.move_limit = 10
        
        # Algorithm settings
        self.algorithm_stats = {}
        self.selected_algorithm = 'A*'
        
        # How hard we try to find good word pairs
        self.max_attempts = 100
        
    def initialize_game(self, dictionary_path: str):
        """Start up the game with our word dictionary"""
        try:
            # Load and validate our dictionary
            self.word_graph.load_words(dictionary_path)
            if self.word_graph.get_word_count() == 0:
                print("Oops! Dictionary is empty")
                return False
                
            # Build connections between words
            self.word_graph.build_graph()
            self.search = SearchAlgorithms(self.word_graph)
            return True
        except Exception as e:
            print(f"Game setup failed: {str(e)}")
            return False
        
    def set_algorithm(self, algorithm: str):
        """Switch between different pathfinding strategies"""
        if algorithm in ['BFS', 'UCS', 'A*']:
            self.selected_algorithm = algorithm
            # Recalculate best path with new algorithm
            if self.current_word and self.target_word:
                self.best_path = self.calculate_best_path()
    
    def set_difficulty(self, difficulty: str):
        """Change game difficulty and adjust settings"""
        try:
            self.difficulty = difficulty.lower()
            
            # Each difficulty has its own rules
            if self.difficulty == "beginner":
                self.move_limit = 10
                self.banned_words.clear()
            elif self.difficulty == "advanced":
                self.move_limit = 15
                self.banned_words.clear()
            elif self.difficulty == "challenge":
                self.move_limit = 12
                # Pick some longer words to ban
                word_list = list(self.word_graph.words)
                self.banned_words = set(random.sample([w for w in word_list if len(w) > 4], 5))
            
            # Try to start a new game with these settings
            if not self.start_new_game_for_difficulty():
                print("Couldn't start a game with these settings")
                return False
            return True
        except Exception as e:
            print(f"Couldn't change difficulty: {str(e)}")
            return False
        
    def find_valid_word_pair(self, min_len: int, max_len: int, min_path: int, max_path: int) -> Optional[Tuple[str, str]]:
        """Find two words that make a good puzzle"""
        try:
            # Get words that fit our criteria
            word_list = [w for w in self.word_graph.words 
                        if min_len <= len(w) <= max_len 
                        and w not in self.banned_words]
            
            if not word_list:
                return None
            
            # Try different starting words
            for _ in range(self.max_attempts):
                start_word = random.choice(word_list)
                potential_targets = []
                
                # Look for good target words
                for target in random.sample(word_list, min(50, len(word_list))):
                    if target != start_word:
                        path, _ = self.search.astar(start_word, target)
                        if path and min_path <= len(path) <= max_path:
                            potential_targets.append(target)
                            # Stop once we have enough good options
                            if len(potential_targets) >= 5:
                                break
                
                if potential_targets:
                    return start_word, random.choice(potential_targets)
            
            return None
        except Exception as e:
            print(f"Problem finding word pair: {str(e)}")
            return None
        
    def get_fallback_word_pair(self) -> Tuple[str, str]:
        """Get reliable word pairs when we can't find random ones"""
        # Classic word pairs that usually work
        reliable_pairs = [
            ("cat", "dog"),   # Animals
            ("cold", "warm"), # Temperature
            ("dark", "light"), # Opposites
            ("head", "tail"), # Body parts
            ("good", "evil"), # Morality
            ("love", "hate"), # Emotions
            ("life", "dead"), # Existence
            ("soft", "hard"), # Texture
            ("fast", "slow"), # Speed
            ("poor", "rich")  # Wealth
        ]
        
        # Try our reliable pairs first
        for start, target in reliable_pairs:
            if (self.word_graph.word_exists(start) and 
                self.word_graph.word_exists(target) and
                start not in self.banned_words and 
                target not in self.banned_words):
                path, _ = self.search.astar(start, target)
                if path:
                    return start, target
        
        # Last resort: just pick any valid words
        valid_words = [w for w in self.word_graph.words if w not in self.banned_words and len(w) >= 3]
        if len(valid_words) >= 2:
            return valid_words[0], valid_words[1]
        
        raise ValueError("Can't find any working word pairs!")
        
    def get_word_pair_for_difficulty(self) -> Tuple[str, str]:
        """Pick words appropriate for current difficulty"""
        word_pair = None
        
        # Different difficulties need different word lengths and path lengths
        if self.difficulty == "beginner":
            word_pair = self.find_valid_word_pair(3, 4, 3, 5)  # Short words, short paths
        elif self.difficulty == "advanced":
            word_pair = self.find_valid_word_pair(4, 6, 5, 8)  # Medium words, longer paths
        else:  # challenge
            word_pair = self.find_valid_word_pair(5, 7, 6, 10) # Long words, complex paths
        
        # Fall back to reliable pairs if needed
        if word_pair is None:
            return self.get_fallback_word_pair()
        return word_pair
        
    def start_new_game_for_difficulty(self) -> bool:
        """Start a new game with current difficulty settings"""
        try:
            # Give it a few tries to find good words
            for attempt in range(3):
                try:
                    start_word, target_word = self.get_word_pair_for_difficulty()
                    if self.start_new_game(start_word, target_word):
                        return True
                except Exception as e:
                    print(f"Try {attempt + 1} failed: {str(e)}")
                    continue
            return False
        except Exception as e:
            print(f"Couldn't start new game: {str(e)}")
            return False
        
    def is_word_valid(self, word: str) -> bool:
        """Check if a word can be used in the game"""
        if not word:
            return False
        word = word.lower()
        return (self.word_graph.word_exists(word) and 
                word not in self.banned_words)
        
    def is_valid_move(self, word: str) -> bool:
        """Check if a word is a legal next move"""
        if not word or not isinstance(word, str):
            return False
        if len(self.moves) >= self.move_limit:
            return False
        word = word.lower()
        if not self.is_word_valid(word):
            return False
        return word in self.word_graph.get_neighbors(self.current_word)
        
    def get_algorithm_comparison(self) -> Dict:
        """Compare how different algorithms solve the puzzle"""
        if not self.current_word or not self.target_word:
            return {}
            
        results = {}
        algorithms = {
            'BFS': self.search.bfs,   # Breadth-first search
            'UCS': self.search.ucs,   # Uniform cost search
            'A*': self.search.astar   # A* search
        }
        
        # Try each algorithm
        for name, algorithm in algorithms.items():
            path, costs = algorithm(self.current_word, self.target_word)
            if path is not None:
                results[name] = {
                    'path': path,
                    'costs': costs
                }
                
        return results
        
    def get_hint(self) -> Tuple[Optional[str], str]:
        """Get AI help for the next move"""
        if not self.best_path:
            return None, "No solution exists!"
            
        try:
            current_index = self.best_path.index(self.current_word)
        except ValueError:
            # We're off the best path, find a new one
            algo_name = 'astar' if self.selected_algorithm == 'A*' else self.selected_algorithm.lower()
            new_path, costs = getattr(self.search, algo_name)(
                self.current_word, self.target_word
            )
            if not new_path:
                return None, "Can't find a path from here!"
            self.best_path = new_path
            current_index = 0

        if current_index >= len(self.best_path) - 1:
            return None, "You're already at the target!"
            
        next_word = self.best_path[current_index + 1]
        
        # Calculate costs for the hint
        current_path = self.best_path[current_index:]
        g_cost = len(current_path) - 1
        h_cost = self.search.h_cost(self.current_word, self.target_word)
        f_cost = g_cost + h_cost
        
        hint_message = (
            f"Using {self.selected_algorithm}\n"
            f"Current cost {g_cost}\n"
            f"Estimated remaining {h_cost}\n"
            f"Total estimated cost {f_cost}\n"
            f"Try this word: '{next_word}'"
        )
            
        return next_word, hint_message
        
    def calculate_best_path(self) -> Optional[List[str]]:
        """Find the best solution path"""
        if not self.current_word or not self.target_word:
            return None
            
        algorithm_paths = self.get_algorithm_comparison()
        
        # Save stats for each algorithm
        self.algorithm_stats = {
            name: {
                'path': info['path'],
                'length': len(info['path']),
                'costs': info['costs']
            }
            for name, info in algorithm_paths.items()
        }
        
        # Use selected algorithm's path if available
        if self.selected_algorithm in algorithm_paths:
            return algorithm_paths[self.selected_algorithm]['path']
        
        # Otherwise use shortest available path
        valid_paths = [info['path'] for info in algorithm_paths.values()]
        return min(valid_paths, key=len) if valid_paths else None
        
    def calculate_score(self) -> int:
        """Calculate player's score based on performance"""
        if not self.best_path:
            return 0
            
        optimal_moves = len(self.best_path) - 1
        actual_moves = len(self.moves) - 1
        
        if actual_moves == 0:
            return 0
            
        remaining_moves = self.move_limit - actual_moves
        
        # Base score depends on how close to optimal solution
        base_score = min(1000 * (optimal_moves / actual_moves), 1000)
        # Bonus for having moves left
        move_bonus = remaining_moves * 100
        
        # Different difficulties get different multipliers
        multipliers = {
            "beginner": 1.0,
            "advanced": 1.5,
            "challenge": 2.0
        }
        
        return int((base_score + move_bonus) * multipliers.get(self.difficulty, 1.0))
        
    def start_new_game(self, start_word: str, target_word: str) -> bool:
        """Set up a new game with given words"""
        try:
            start_word = start_word.lower()
            target_word = target_word.lower()
            
            # Make sure both words are valid
            if not (self.is_word_valid(start_word) and self.is_word_valid(target_word)):
                return False
                
            # Make sure there's a path between the words
            path, _ = self.search.astar(start_word, target_word)
            if not path:
                return False
                
            # Initialize game state
            self.current_word = start_word
            self.target_word = target_word
            self.moves = [start_word]
            self.best_path = path
            self.score = 0
            self.algorithm_stats = {}
            return True
        except Exception as e:
            print(f"Problem starting new game: {str(e)}")
            return False
        
    def make_move(self, new_word: str) -> bool:
        """Try to make a move in the game"""
        try:
            new_word = new_word.lower()
            if not self.is_valid_move(new_word):
                return False
                
            self.current_word = new_word
            self.moves.append(new_word)
            return True
        except Exception as e:
            print(f"Move failed: {str(e)}")
            return False
        
    def is_solved(self) -> bool:
        """Check if puzzle is solved"""
        return self.current_word == self.target_word
        
    def get_minimum_moves(self) -> int:
        """Get shortest possible solution length"""
        return len(self.best_path) - 1 if self.best_path else 0
        
    def get_current_moves(self) -> int:
        """Get number of moves made so far"""
        return len(self.moves) - 1
        
    def get_remaining_moves(self) -> int:
        """Get how many moves are left"""
        return self.move_limit - self.get_current_moves()