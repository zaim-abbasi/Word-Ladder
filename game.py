from typing import Optional, List, Tuple
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
        
    def initialize_game(self, dictionary_path: str) -> None:
        """Initialize the game by loading the dictionary and building the graph."""
        self.word_graph.load_words(dictionary_path)
        self.word_graph.build_graph()
        self.search = SearchAlgorithms(self.word_graph)
        
    def set_difficulty(self, difficulty: str) -> None:
        """Set game difficulty level."""
        self.difficulty = difficulty.lower()
        if self.difficulty == "challenge":
            # Add random banned words for challenge mode
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
        return word in self.word_graph.get_neighbors(self.current_word)
        
    def get_hint(self) -> Tuple[Optional[str], str]:
        """Get an intelligent hint based on the current game state."""
        if not self.best_path:
            return None, "No solution exists!"
            
        current_index = self.best_path.index(self.current_word)
        if current_index >= len(self.best_path) - 1:
            return None, "You're already at the target word!"
            
        next_word = self.best_path[current_index + 1]
        
        # Calculate different paths using different algorithms
        bfs_path = self.search.bfs(self.current_word, self.target_word)
        ucs_path = self.search.ucs(self.current_word, self.target_word)
        astar_path = self.best_path  # Already calculated using A*
        
        # Compare paths to provide more insightful hints
        if all(p and p[1] == next_word for p in [bfs_path, ucs_path, astar_path] if p):
            hint_type = "Strong hint"
            message = f"All algorithms suggest using '{next_word}' as your next move!"
        else:
            hint_type = "Strategic hint"
            diff_letters = sum(1 for a, b in zip(next_word, self.current_word) if a != b)
            changed_pos = next(i for i, (a, b) in enumerate(zip(next_word, self.current_word)) if a != b)
            message = f"Try changing letter position {changed_pos + 1} to get closer to the target word."
            
        return next_word, f"{hint_type}: {message}"
        
    def calculate_best_path(self) -> Optional[List[str]]:
        """Calculate the optimal solution using multiple search algorithms."""
        # Try all three algorithms and choose the best result
        paths = {
            'bfs': self.search.bfs(self.current_word, self.target_word),
            'ucs': self.search.ucs(self.current_word, self.target_word),
            'astar': self.search.astar(self.current_word, self.target_word)
        }
        
        # Filter out None paths and sort by length
        valid_paths = [p for p in paths.values() if p]
        if not valid_paths:
            return None
            
        return min(valid_paths, key=len)
        
    def calculate_score(self) -> int:
        """Calculate score based on moves taken and difficulty."""
        if not self.best_path:
            return 0
            
        optimal_moves = len(self.best_path) - 1
        actual_moves = len(self.moves) - 1
        
        # Base score calculation
        base_score = 1000 * optimal_moves / actual_moves
        
        # Difficulty multipliers
        multipliers = {
            "beginner": 1.0,
            "advanced": 1.5,
            "challenge": 2.0
        }
        
        return int(base_score * multipliers.get(self.difficulty, 1.0))
        
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