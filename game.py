"""
Word Ladder Game Logic Module

This module contains the core game logic for the Word Ladder game, where players
transform one word into another by changing one letter at a time.
"""

from typing import Optional, List, Tuple, Dict
from word_graph import WordGraph
from search import SearchAlgorithms

class WordLadderGame:
    """Manages the core game logic for Word Ladder."""
    
    def __init__(self):
        """Initialize a new game instance with default settings."""
        self.word_graph = WordGraph()
        self.search = None
        self.current_word = None
        self.target_word = None
        self.moves = []
        self.best_path = None
        self.difficulty = "beginner"
        self.score = 0
        self.banned_words = set()
        self.move_limit = 10  # Default move limit
        self.algorithm_stats = {}
        self.selected_algorithm = 'A*'
        
    def initialize_game(self, dictionary_path: str) -> None:
        """
        Set up the game by loading words and creating the word graph.
        
        Args:
            dictionary_path (str): Path to the dictionary file
        """
        self.word_graph.load_words(dictionary_path)
        self.word_graph.build_graph()
        self.search = SearchAlgorithms(self.word_graph)
        
    def set_algorithm(self, algorithm: str) -> None:
        """
        Change the search algorithm used for hints and path finding.
        
        Args:
            algorithm (str): Name of the algorithm ('BFS', 'UCS', or 'A*')
        """
        if algorithm in ['BFS', 'UCS', 'A*']:
            self.selected_algorithm = algorithm
            if self.current_word and self.target_word:
                self.best_path = self.calculate_best_path()
    
    def set_difficulty(self, difficulty: str) -> None:
        """
        Set the game difficulty and adjust move limits accordingly.
        
        Args:
            difficulty (str): Difficulty level ('beginner', 'advanced', or 'challenge')
        """
        self.difficulty = difficulty.lower()
        
        # Set move limits based on difficulty
        if self.difficulty == "beginner":
            self.move_limit = 10
        elif self.difficulty == "advanced":
            self.move_limit = 15
        elif self.difficulty == "challenge":
            self.move_limit = 12
            # Add some random banned words in challenge mode
            word_list = list(self.word_graph.words)
            self.banned_words = set(word_list[:5])  # Take first 5 words instead of random
        
    def is_word_valid(self, word: str) -> bool:
        """
        Check if a word exists in the dictionary and isn't banned.
        
        Args:
            word (str): Word to check
            
        Returns:
            bool: True if the word is valid, False otherwise
        """
        word = word.lower()
        return (self.word_graph.word_exists(word) and 
                word not in self.banned_words)
        
    def is_valid_move(self, word: str) -> bool:
        """
        Check if the proposed word is a valid next move.
        
        Args:
            word (str): Word to check
            
        Returns:
            bool: True if the move is valid, False otherwise
        """
        if not self.is_word_valid(word):
            return False
        if len(self.moves) >= self.move_limit:
            return False
        return word in self.word_graph.get_neighbors(self.current_word)
        
    def get_algorithm_comparison(self) -> Dict[str, Dict]:
        """
        Compare paths and costs found by different algorithms.
        
        Returns:
            Dict: Results from each algorithm including paths and costs
        """
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
        
    def get_hint(self) -> Tuple[Optional[str], str]:
        """
        Get a hint for the next move based on the selected algorithm.
        
        Returns:
            Tuple[Optional[str], str]: Next suggested word and explanation
        """
        if not self.best_path:
            return None, "No solution exists!"
            
        current_index = self.best_path.index(self.current_word)
        if current_index >= len(self.best_path) - 1:
            return None, "You're already at the target word!"
            
        algorithm_paths = self.get_algorithm_comparison()
        algo_info = algorithm_paths.get(self.selected_algorithm, {})
        
        if not algo_info:
            return None, f"No solution found using {self.selected_algorithm}!"
            
        path = algo_info['path']
        costs = algo_info['costs']
        next_word = path[current_index + 1]
        
        hint_message = (
            f"Using {self.selected_algorithm}:\n"
            f"Current cost: {costs['g_cost']}\n"
            f"Estimated remaining: {costs['h_cost']}\n"
            f"Total estimated cost: {costs['f_cost']}\n"
            f"Suggested next word: '{next_word}'"
        )
            
        return next_word, hint_message
        
    def calculate_best_path(self) -> Optional[List[str]]:
        """
        Find the optimal solution path using the selected algorithm.
        
        Returns:
            Optional[List[str]]: List of words in the optimal path, or None if no path exists
        """
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
        
        # Find shortest available path if selected algorithm fails
        valid_paths = [info['path'] for info in algorithm_paths.values()]
        return min(valid_paths, key=len) if valid_paths else None
        
    def calculate_score(self) -> int:
        """
        Calculate the player's score based on performance.
        
        Returns:
            int: Final score
        """
        if not self.best_path:
            return 0
            
        optimal_moves = len(self.best_path) - 1
        actual_moves = len(self.moves) - 1
        
        if actual_moves == 0:  # Prevent division by zero
            return 0
            
        remaining_moves = self.move_limit - actual_moves
        
        # Calculate score components
        base_score = min(1000 * (optimal_moves / actual_moves), 1000)  # Cap at 1000
        move_bonus = remaining_moves * 100
        
        # Apply difficulty multipliers
        multipliers = {
            "beginner": 1.0,
            "advanced": 1.5,
            "challenge": 2.0
        }
        
        return int((base_score + move_bonus) * multipliers.get(self.difficulty, 1.0))
        
    def start_new_game(self, start_word: str, target_word: str) -> bool:
        """
        Initialize a new game with given start and target words.
        
        Args:
            start_word (str): Starting word
            target_word (str): Target word to reach
            
        Returns:
            bool: True if game started successfully, False otherwise
        """
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
        
    def make_move(self, new_word: str) -> bool:
        """
        Attempt to make a move in the game.
        
        Args:
            new_word (str): Word to move to
            
        Returns:
            bool: True if move was valid and made, False otherwise
        """
        new_word = new_word.lower()
        if not self.is_valid_move(new_word):
            return False
            
        self.current_word = new_word
        self.moves.append(new_word)
        return True
        
    def is_solved(self) -> bool:
        """
        Check if the puzzle has been solved.
        
        Returns:
            bool: True if current word matches target word, False otherwise
        """
        if self.current_word == self.target_word:
            self.score = self.calculate_score()
            return True
        return False
        
    def get_minimum_moves(self) -> int:
        """
        Get the minimum number of moves needed to solve the puzzle.
        
        Returns:
            int: Minimum number of moves required
        """
        return len(self.best_path) - 1 if self.best_path else 0
        
    def get_current_moves(self) -> int:
        """
        Get the number of moves made so far.
        
        Returns:
            int: Number of moves made
        """
        return len(self.moves) - 1
        
    def get_remaining_moves(self) -> int:
        """
        Get the number of moves remaining before hitting the limit.
        
        Returns:
            int: Number of moves remaining
        """
        return self.move_limit - self.get_current_moves()