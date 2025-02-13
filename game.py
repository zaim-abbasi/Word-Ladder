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
        self.move_limit = float('inf')
        self.algorithm_stats = {}
        self.selected_algorithm = 'A*'  # Default algorithm
        
    def initialize_game(self, dictionary_path: str) -> None:
        """Initialize the game by loading the dictionary and building the graph."""
        self.word_graph.load_words(dictionary_path)
        self.word_graph.build_graph()
        self.search = SearchAlgorithms(self.word_graph)
        
    def set_algorithm(self, algorithm: str) -> None:
        """Set the algorithm to use for hints and path finding."""
        if algorithm in ['BFS', 'UCS', 'A*']:
            self.selected_algorithm = algorithm
            # Recalculate best path with new algorithm
            if self.current_word and self.target_word:
                self.best_path = self.calculate_best_path()
    
    def set_difficulty(self, difficulty: str) -> None:
        """Set game difficulty level and corresponding move limits."""
        self.difficulty = difficulty.lower()
        
        # Set move limits based on difficulty
        if self.difficulty == "beginner":
            self.move_limit = 10
        elif self.difficulty == "advanced":
            self.move_limit = 15
        else:  # challenge mode
            self.move_limit = 12
            word_list = list(self.word_graph.words)
            self.banned_words = set(random.sample(word_list, min(5, len(word_list))))
        
    def validate_word(self, word: str) -> bool:
        """Check if a word exists in the dictionary and is not banned."""
        word = word.lower()
        return (self.word_graph.word_exists(word) and 
                word not in self.banned_words)
        
    def is_valid_move(self, word: str) -> bool:
        """Check if the proposed word is a valid one-letter transformation."""
        if not self.validate_word(word):
            return False
        if len(self.moves) >= self.move_limit:
            return False
        return word in self.word_graph.get_neighbors(self.current_word)
        
    def get_algorithm_comparison(self) -> Dict[str, Dict]:
        """Compare paths and costs found by different algorithms."""
        paths_and_costs = {
            'BFS': self.search.bfs(self.current_word, self.target_word),
            'UCS': self.search.ucs(self.current_word, self.target_word),
            'A*': self.search.astar(self.current_word, self.target_word)
        }
        
        return {
            name: {
                'path': path,
                'costs': costs
            }
            for name, (path, costs) in paths_and_costs.items()
            if path is not None
        }
        
    def get_hint(self) -> Tuple[Optional[str], str]:
        """Get an intelligent hint based on the current game state and selected algorithm."""
        if not self.best_path:
            return None, "No solution exists!"
            
        current_index = self.best_path.index(self.current_word)
        if current_index >= len(self.best_path) - 1:
            return None, "You're already at the target word!"
            
        # Get algorithm comparisons with costs
        algorithm_paths = self.get_algorithm_comparison()
        
        # Get next word and costs for selected algorithm
        algo_info = algorithm_paths.get(self.selected_algorithm, {})
        if not algo_info:
            return None, f"No solution found using {self.selected_algorithm}!"
            
        path = algo_info['path']
        costs = algo_info['costs']
        next_word = path[current_index + 1]
        
        # Create detailed hint message
        hint_type = "Algorithm Analysis"
        message = (
            f"Using {self.selected_algorithm}:\n"
            f"Current g(n) (cost so far): {costs['g_cost']}\n"
            f"h(n) (estimated remaining cost): {costs['h_cost']}\n"
            f"f(n) (total estimated cost): {costs['f_cost']}\n"
            f"Suggested next word: '{next_word}'"
        )
            
        return next_word, f"{hint_type}: {message}"
        
    def calculate_best_path(self) -> Optional[List[str]]:
        """Calculate the optimal solution using the selected algorithm."""
        algorithm_paths = self.get_algorithm_comparison()
        
        # Store algorithm statistics
        self.algorithm_stats = {
            name: {
                'path': info['path'],
                'length': len(info['path']),
                'costs': info['costs']
            }
            for name, info in algorithm_paths.items()
        }
        
        # Use selected algorithm's path
        if self.selected_algorithm in algorithm_paths:
            return algorithm_paths[self.selected_algorithm]['path']
        
        # Fallback to shortest available path if selected algorithm fails
        valid_paths = [info['path'] for info in algorithm_paths.values()]
        return min(valid_paths, key=len) if valid_paths else None
        
    def calculate_score(self) -> int:
        """Calculate score based on moves taken, difficulty, and remaining moves."""
        if not self.best_path:
            return 0
            
        optimal_moves = len(self.best_path) - 1
        actual_moves = len(self.moves) - 1
        remaining_moves = self.move_limit - actual_moves
        
        # Base score calculation
        base_score = 1000 * (optimal_moves / actual_moves)
        
        # Bonus for remaining moves
        move_bonus = remaining_moves * 100
        
        # Difficulty multipliers
        multipliers = {
            "beginner": 1.0,
            "advanced": 1.5,
            "challenge": 2.0
        }
        
        return int((base_score + move_bonus) * multipliers.get(self.difficulty, 1.0))
        
    def start_new_game(self, start_word: str, target_word: str) -> bool:
        """Start a new game with the given start and target words."""
        start_word = start_word.lower()
        target_word = target_word.lower()
        
        if not (self.validate_word(start_word) and self.validate_word(target_word)):
            return False
            
        self.current_word = start_word
        self.target_word = target_word
        self.moves = [start_word]
        self.best_path = self.calculate_best_path()
        self.score = 0
        self.algorithm_stats = {}
        return True
        
    def make_move(self, new_word: str) -> bool:
        """Attempt to make a move with the given word."""
        new_word = new_word.lower()
        if not self.is_valid_move(new_word):
            return False
            
        self.current_word = new_word
        self.moves.append(new_word)
        return True
        
    def is_solved(self) -> bool:
        """Check if the puzzle has been solved."""
        solved = self.current_word == self.target_word
        if solved:
            self.score = self.calculate_score()
        return solved
        
    def get_minimum_moves(self) -> int:
        """Get the minimum number of moves required to solve the puzzle."""
        return len(self.best_path) - 1 if self.best_path else 0
        
    def get_current_moves(self) -> int:
        """Get the number of moves made so far."""
        return len(self.moves) - 1
        
    def get_remaining_moves(self) -> int:
        """Get the number of moves remaining before hitting the limit."""
        return self.move_limit - self.get_current_moves()