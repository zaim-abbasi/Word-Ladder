from typing import Optional, List, Tuple, Dict
from word_graph import WordGraph
from search import SearchAlgorithms
import random

class WordLadderGame:
    def __init__(self):
        # core game components
        self.word_graph = WordGraph()
        self.search = None
        
        # current game state
        self.current_word = None
        self.target_word = None
        self.moves = []
        self.best_path = None
        
        # game settings
        self.difficulty = "beginner"
        self.score = 0
        self.banned_words = set()
        self.move_limit = 10
        
        # algorithm settings
        self.algorithm_stats = {}
        self.selected_algorithm = 'A*'
        
        # how hard we try to find good word pairs
        self.max_attempts = 100
        
        # add new settings for different modes
        self.restricted_letters = set()  # for challenge mode
        self.min_word_length = 3  # shortest allowed word
        self.max_word_length = 7  # longest allowed word
        
    def initialize_game(self, dictionary_path: str):
        """start up the game with our word dictionary"""
        try:
            # load and validate our dictionary
            self.word_graph.load_words(dictionary_path)
            if self.word_graph.get_word_count() == 0:
                print("error: dictionary is empty")
                return False
                
            # build connections between words
            self.word_graph.build_graph()
            self.search = SearchAlgorithms(self.word_graph)
            return True
        except Exception as e:
            print(f"game setup failed: {str(e)}")
            return False
        
    def set_algorithm(self, algorithm: str):
        """switch between different pathfinding strategies"""
        if algorithm in ['BFS', 'UCS', 'A*']:
            self.selected_algorithm = algorithm
            # recalculate best path with new algorithm
            if self.current_word and self.target_word:
                self.best_path = self.calculate_best_path()
    
    def set_difficulty(self, difficulty: str):
        """change game difficulty and adjust settings"""
        try:
            self.difficulty = difficulty.lower()
            
            # each difficulty has its own rules
            if self.difficulty == "beginner":
                # simple settings for beginners
                self.move_limit = 10
                self.min_word_length = 3
                self.max_word_length = 4
                self.banned_words.clear()
                self.restricted_letters.clear()
                
            elif self.difficulty == "advanced":
                # harder settings for advanced players
                self.move_limit = 15
                self.min_word_length = 4
                self.max_word_length = 6
                self.banned_words.clear()
                self.restricted_letters.clear()
                
            elif self.difficulty == "challenge":
                # complex settings for experts
                self.move_limit = 12
                self.min_word_length = 5
                self.max_word_length = 7
                
                # find a good word pair first
                word_pair = self.find_valid_word_pair(5, 7, 6, 10)
                if word_pair:
                    start_word, target_word = word_pair
                    # get all possible words in transformation
                    possible_words = self.word_graph.get_transformation_tree(start_word, target_word)
                    # pick some words from the transformation tree to ban
                    ban_candidates = [w for w in possible_words 
                                   if w != start_word and w != target_word]
                    if ban_candidates:
                        self.banned_words = set(random.sample(ban_candidates, 
                                                            min(5, len(ban_candidates))))
                    
                # restrict some letters
                self.restricted_letters = set(random.sample('abcdefghijklmnopqrstuvwxyz', 3))
            
            # try to start a new game with these settings
            if not self.start_new_game_for_difficulty():
                print("couldn't start a game with these settings")
                return False
            return True
            
        except Exception as e:
            print(f"couldn't change difficulty: {str(e)}")
            return False
        
    def find_valid_word_pair(self, min_len: int, max_len: int, min_path: int, max_path: int) -> Optional[Tuple[str, str]]:
        """find two words that make a good puzzle"""
        try:
            # get words that fit our criteria
            word_list = [w for w in self.word_graph.words 
                        if min_len <= len(w) <= max_len 
                        and w not in self.banned_words]
            
            if not word_list:
                return None
            
            # try different starting words
            for _ in range(self.max_attempts):
                start_word = random.choice(word_list)
                potential_targets = []
                
                # look for good target words
                for target in random.sample(word_list, min(50, len(word_list))):
                    if target != start_word:
                        path, _ = self.search.astar(start_word, target)
                        if path and min_path <= len(path) <= max_path:
                            potential_targets.append(target)
                            # stop once we have enough good options
                            if len(potential_targets) >= 5:
                                break
                
                if potential_targets:
                    return start_word, random.choice(potential_targets)
            
            return None
        except Exception as e:
            print(f"problem finding word pair: {str(e)}")
            return None
        
    def get_fallback_word_pair(self) -> Tuple[str, str]:
        """get reliable word pairs when we can't find random ones"""
        # classic word pairs that usually work
        reliable_pairs = [
            ("cat", "dog"),   # animals
            ("cold", "warm"), # temperature
            ("dark", "light"), # opposites
            ("head", "tail"), # body parts
            ("good", "evil"), # morality
            ("love", "hate"), # emotions
            ("life", "dead"), # existence
            ("soft", "hard"), # texture
            ("fast", "slow"), # speed
            ("poor", "rich")  # wealth
        ]
        
        # try our reliable pairs first
        for start, target in reliable_pairs:
            if (self.word_graph.word_exists(start) and 
                self.word_graph.word_exists(target) and
                start not in self.banned_words and 
                target not in self.banned_words):
                path, _ = self.search.astar(start, target)
                if path:
                    return start, target
        
        # last resort: just pick any valid words
        valid_words = [w for w in self.word_graph.words if w not in self.banned_words and len(w) >= 3]
        if len(valid_words) >= 2:
            return valid_words[0], valid_words[1]
        
        raise ValueError("can't find any working word pairs!")
        
    def get_word_pair_for_difficulty(self) -> Tuple[str, str]:
        """pick words appropriate for current difficulty"""
        word_pair = None
        
        # different difficulties need different word lengths and path lengths
        if self.difficulty == "beginner":
            word_pair = self.find_valid_word_pair(3, 4, 3, 5)  # short words, short paths
        elif self.difficulty == "advanced":
            word_pair = self.find_valid_word_pair(4, 6, 5, 8)  # medium words, longer paths
        else:  # challenge
            word_pair = self.find_valid_word_pair(5, 7, 6, 10) # long words, complex paths
        
        # fall back to reliable pairs if needed
        if word_pair is None:
            return self.get_fallback_word_pair()
        return word_pair
        
    def start_new_game_for_difficulty(self) -> bool:
        """start a new game with current difficulty settings"""
        try:
            # give it a few tries to find good words
            for attempt in range(3):
                try:
                    start_word, target_word = self.get_word_pair_for_difficulty()
                    if self.start_new_game(start_word, target_word):
                        return True
                except Exception as e:
                    print(f"try {attempt + 1} failed: {str(e)}")
                    continue
            return False
        except Exception as e:
            print(f"couldn't start new game: {str(e)}")
            return False
        
    def is_word_valid(self, word: str) -> bool:
        """check if a word can be used in the game"""
        if not word:
            return False
            
        word = word.lower()
        
        # basic checks
        if not self.word_graph.word_exists(word):
            return False
            
        if word in self.banned_words:
            return False
            
        # length checks
        if len(word) < self.min_word_length or len(word) > self.max_word_length:
            return False
            
        # challenge mode letter restrictions
        if self.difficulty == "challenge":
            if any(letter in self.restricted_letters for letter in word):
                return False
                
        return True
        
    def is_valid_move(self, word: str) -> bool:
        """check if a word is a legal next move"""
        if not word or not isinstance(word, str):
            return False
        if len(self.moves) >= self.move_limit:
            return False
        word = word.lower()
        if not self.is_word_valid(word):
            return False
        return word in self.word_graph.get_neighbors(self.current_word)
        
    def get_algorithm_comparison(self) -> Dict:
        """compare how different algorithms solve the puzzle"""
        if not self.current_word or not self.target_word:
            return {}
            
        results = {}
        algorithms = {
            'BFS': self.search.bfs,   # breadth-first search
            'UCS': self.search.ucs,   # uniform cost search
            'A*': self.search.astar   # a* search
        }
        
        # try each algorithm
        for name, algorithm in algorithms.items():
            path, costs = algorithm(self.current_word, self.target_word)
            if path is not None:
                results[name] = {
                    'path': path,
                    'costs': costs
                }
                
        return results
        
    def get_hint(self) -> Tuple[Optional[str], str]:
        """get AI help for the next move"""
        if not self.best_path:
            return None, "no solution exists!"
            
        try:
            current_index = self.best_path.index(self.current_word)
        except ValueError:
            # we are off the best path, find a new one
            algo_name = 'astar' if self.selected_algorithm == 'A*' else self.selected_algorithm.lower()
            new_path, costs = getattr(self.search, algo_name)(
                self.current_word, self.target_word
            )
            if not new_path:
                return None, "can't find a path from here!"
            self.best_path = new_path
            current_index = 0

        if current_index >= len(self.best_path) - 1:
            return None, "you're already at the target!"
            
        next_word = self.best_path[current_index + 1]
        
        # calculate costs for the hint
        current_path = self.best_path[current_index:]
        g_cost = len(current_path) - 1
        h_cost = self.search.h_cost(self.current_word, self.target_word)
        f_cost = g_cost + h_cost
        
        hint_message = (
            f"using {self.selected_algorithm}\n"
            f"current cost {g_cost}\n"
            f"estimated remaining {h_cost}\n"
            f"total estimated cost {f_cost}\n"
            f"try this word: '{next_word}'"
        )
            
        return next_word, hint_message
        
    def calculate_best_path(self) -> Optional[List[str]]:
        """find the best solution path"""
        if not self.current_word or not self.target_word:
            return None
            
        algorithm_paths = self.get_algorithm_comparison()
        
        # save stats for each algorithm
        self.algorithm_stats = {
            name: {
                'path': info['path'],
                'length': len(info['path']),
                'costs': info['costs']
            }
            for name, info in algorithm_paths.items()
        }
        
        # use selected algorithm's path if available
        if self.selected_algorithm in algorithm_paths:
            return algorithm_paths[self.selected_algorithm]['path']
        
        # otherwise use shortest available path
        valid_paths = [info['path'] for info in algorithm_paths.values()]
        return min(valid_paths, key=len) if valid_paths else None
        
    def calculate_score(self) -> int:
        """calculate player's score based on performance"""
        if not self.best_path:
            return 0
            
        optimal_moves = len(self.best_path) - 1
        actual_moves = len(self.moves) - 1
        
        if actual_moves == 0:
            return 0
            
        remaining_moves = self.move_limit - actual_moves
        
        # base score depends on how close to optimal solution
        base_score = min(1000 * (optimal_moves / actual_moves), 1000)
        # bonus for having moves left
        move_bonus = remaining_moves * 100
        
        # different difficulties get different multipliers
        multipliers = {
            "beginner": 1.0,
            "advanced": 1.5,
            "challenge": 2.0
        }
        
        return int((base_score + move_bonus) * multipliers.get(self.difficulty, 1.0))
        
    def start_new_game(self, start_word: str, target_word: str) -> bool:
        """set up a new game with given words"""
        try:
            start_word = start_word.lower()
            target_word = target_word.lower()
            
            # make sure both words are valid
            if not (self.is_word_valid(start_word) and self.is_word_valid(target_word)):
                return False
                
            # make sure there's a path between the words
            path, _ = self.search.astar(start_word, target_word)
            if not path:
                return False
                
            # initialize game state
            self.current_word = start_word
            self.target_word = target_word
            self.moves = [start_word]
            self.best_path = path
            self.score = 0
            self.algorithm_stats = {}
            return True
        except Exception as e:
            print(f"problem starting new game: {str(e)}")
            return False
        
    def make_move(self, new_word: str) -> bool:
        """try to make a move in the game"""
        try:
            new_word = new_word.lower()
            if not self.is_valid_move(new_word):
                return False
                
            self.current_word = new_word
            self.moves.append(new_word)
            return True
        except Exception as e:
            print(f"move failed: {str(e)}")
            return False
        
    def is_solved(self) -> bool:
        """check if puzzle is solved"""
        return self.current_word == self.target_word
        
    def get_minimum_moves(self) -> int:
        """get shortest possible solution length"""
        return len(self.best_path) - 1 if self.best_path else 0
        
    def get_current_moves(self) -> int:
        """get number of moves made so far"""
        return len(self.moves) - 1
        
    def get_remaining_moves(self) -> int:
        """get how many moves are left"""
        return self.move_limit - self.get_current_moves()