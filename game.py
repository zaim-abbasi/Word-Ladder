from typing import Optional, List, Tuple, Dict
from word_graph import WordGraph
from search import SearchAlgorithms
import random

class WordLadderGame:
    def __init__(self):
        # main game things we need
        self.word_graph = WordGraph()
        self.search = None
        
        # keeping track of game situation
        self.current_word = None
        self.target_word = None
        self.moves = []
        self.best_path = None
        
        # game settings
        self.difficulty = "beginner"
        self.score = 0
        self.banned_words = set()
        self.move_limit = 10
        
        # keeping track of which search method working best
        self.algorithm_stats = {}
        self.selected_algorithm = 'A*'
        
        # how much we try to find good word pairs
        self.max_attempts = 100  # Increased from 50 to 100
        
        # setting for different modes
        self.restricted_letters = set()  # for challenge mode
        self.min_word_length = 3  
        self.max_word_length = 7 
        
    def initialize_game(self, dictionary_path: str):
        try:
            # loading our dictionary
            self.word_graph.load_words(dictionary_path)
            if self.word_graph.count_words() == 0:
                print("error: Dictionary is Empty!")
                return False
                
            # making word connections
            self.word_graph.build_word_network()
            self.search = SearchAlgorithms(self.word_graph)
            return True
        except Exception as e:
            print(f"Game Setup Failed: {str(e)}")
            return False
        
    def set_algorithm(self, algorithm: str):
        # changing search method
        if algorithm in ['BFS', 'UCS', 'A*']:
            self.selected_algorithm = algorithm
            # need to find path again with new method
            if self.current_word and self.target_word:
                self.best_path = self.calculate_best_path()
    
    def set_difficulty(self, difficulty: str):
        try:
            self.difficulty = difficulty.lower()
            
            # different settings for different levels
            if self.difficulty == "beginner":
                # easy mode for new players
                self.move_limit = 10
                self.min_word_length = 3
                self.max_word_length = 4
                self.banned_words.clear()
                self.restricted_letters.clear()
                
            elif self.difficulty == "advanced":
                # thora mushkil mode
                self.move_limit = 15
                self.min_word_length = 4
                self.max_word_length = 6
                self.banned_words.clear()
                self.restricted_letters.clear()
                
            elif self.difficulty == "challenge":
                # hardcore mode
                self.move_limit = 12
                self.min_word_length = 4  # Reduced from 5 to 4
                self.max_word_length = 6  # Reduced from 7 to 6
                self.banned_words.clear()
                
                # finding good word pair first
                word_pair = self.find_valid_word_pair(4, 6, 5, 8)  # Adjusted parameters
                if word_pair:
                    start_word, target_word = word_pair
                    # getting all possible words in between
                    possible_words = self.word_graph.find_possible_words(start_word, target_word)
                    # picking some words to ban
                    ban_candidates = [w for w in possible_words 
                                   if w != start_word and w != target_word]
                    if ban_candidates:
                        self.banned_words = set(random.sample(ban_candidates, 
                                                            min(3, len(ban_candidates))))  # Reduced from 5 to 3
                    
                # blocking some letters
                self.restricted_letters = set(random.sample('abcdefghijklmnopqrstuvwxyz', 2))  # Reduced from 3 to 2
            
            # trying to start game with new settings
            if not self.start_new_game_for_difficulty():
                print("new settings se game start nahi hua")
                return False
            return True
            
        except Exception as e:
            print(f"difficulty change nahi hui: {str(e)}")
            return False
        
    def find_valid_word_pair(self, min_len: int, max_len: int, min_path: int, max_path: int) -> Optional[Tuple[str, str]]:
        try:
            # getting words that fit our rules
            word_list = [w for w in self.word_graph.word_list 
                        if min_len <= len(w) <= max_len 
                        and w not in self.banned_words
                        and not any(letter in self.restricted_letters for letter in w)]
            
            if not word_list:
                return None
            
            # trying different starting words
            for _ in range(self.max_attempts):
                start_word = random.choice(word_list)
                potential_targets = []
                
                # looking for good target words
                for target in random.sample(word_list, min(100, len(word_list))):  # Increased from 50 to 100
                    if target != start_word:
                        path, _ = self.search.astar(start_word, target)
                        if path and min_path <= len(path) <= max_path:
                            potential_targets.append(target)
                            # bas itne kaafi hain
                            if len(potential_targets) >= 5:
                                break
                
                if potential_targets:
                    return start_word, random.choice(potential_targets)
            
            return None
        except Exception as e:
            print(f"word pair dhundne mein masla hogaya: {str(e)}")
            return None
        
    def get_fallback_word_pair(self) -> Tuple[str, str]:
        # tried and tested word pairs
        reliable_pairs = [
            ("cat", "dog"),   
            ("cold", "warm"),
            ("dark", "light"), 
            ("head", "tail"),
            ("good", "evil"), 
            ("love", "hate"), 
            ("life", "dead"), 
            ("soft", "hard"), 
            ("fast", "slow"), 
            ("poor", "rich") 
        ]
        
        # trying our trusted pairs first
        for start, target in reliable_pairs:
            if (self.word_graph.is_valid_word(start) and 
                self.word_graph.is_valid_word(target) and
                start not in self.banned_words and 
                target not in self.banned_words and
                not any(letter in self.restricted_letters for letter in start) and
                not any(letter in self.restricted_letters for letter in target)):
                path, _ = self.search.astar(start, target)
                if path:
                    return start, target
        
        # last option: koi bhi do words
        valid_words = [w for w in self.word_graph.word_list 
                      if w not in self.banned_words 
                      and len(w) >= self.min_word_length
                      and len(w) <= self.max_word_length
                      and not any(letter in self.restricted_letters for letter in w)]
        if len(valid_words) >= 2:
            return random.choice(valid_words), random.choice(valid_words)
        
        raise ValueError("koi bhi working word pair nahi mila!")
        
    def get_word_pair_for_difficulty(self) -> Tuple[str, str]:
        word_pair = None
        
        # different difficulties need different types of words
        if self.difficulty == "beginner":
            word_pair = self.find_valid_word_pair(3, 4, 3, 5)  # easy peasy
        elif self.difficulty == "advanced":
            word_pair = self.find_valid_word_pair(4, 6, 5, 8)  # getting tougher
        else:  # challenge
            word_pair = self.find_valid_word_pair(4, 6, 5, 8)  # Adjusted parameters
        
        # if pair not found, using fallback
        if word_pair is None:
            return self.get_fallback_word_pair()
        return word_pair
        
    def start_new_game_for_difficulty(self) -> bool:
        try:
            # giving it a few tries to find good words
            for attempt in range(3):
                try:
                    start_word, target_word = self.get_word_pair_for_difficulty()
                    if self.start_new_game(start_word, target_word):
                        return True
                except Exception as e:
                    print(f"try {attempt + 1} fail hogaya: {str(e)}")
                    continue
            return False
        except Exception as e:
            print(f"new game start nahi hua: {str(e)}")
            return False
        
    def is_word_valid(self, word: str) -> bool:
        if not word:
            return False
            
        word = word.lower()
        
        # checking all the rules
        if not self.word_graph.is_valid_word(word):
            return False
            
        if word in self.banned_words:
            return False
            
        # length check karo
        if len(word) < self.min_word_length or len(word) > self.max_word_length:
            return False
            
        # challenge mode mein extra checks
        if self.difficulty == "challenge":
            if any(letter in self.restricted_letters for letter in word):
                return False
                
        return True
        
    def is_valid_move(self, word: str) -> bool:
        # checking if move is allowed
        if not word or not isinstance(word, str):
            return False
        if len(self.moves) >= self.move_limit:
            return False
        word = word.lower()
        if not self.is_word_valid(word):
            return False
        return word in self.word_graph.get_connected_words(self.current_word)
        
    def get_algorithm_comparison(self) -> Dict:
        # comparing different search methods
        if not self.current_word or not self.target_word:
            return {}
            
        results = {}
        algorithms = {
            'BFS': self.search.bfs,   # simple search
            'UCS': self.search.ucs,   # cost wala search
            'A*': self.search.astar   # smart search
        }
        
        # trying each method
        for name, algorithm in algorithms.items():
            path, costs = algorithm(self.current_word, self.target_word)
            if path is not None:
                results[name] = {
                    'path': path,
                    'costs': costs
                }
                
        return results
        
    def get_hint(self) -> Tuple[Optional[str], str]:
        # getting help from AI
        if not self.best_path:
            return None, "No path found yet!"
            
        try:
            current_index = self.best_path.index(self.current_word)
        except ValueError:
            # we're lost, need new directions
            algo_name = 'astar' if self.selected_algorithm == 'A*' else self.selected_algorithm.lower()
            new_path, costs = getattr(self.search, algo_name)(
                self.current_word, self.target_word
            )
            if not new_path:
                return None, "No path found from current word!"
            self.best_path = new_path
            current_index = 0

        if current_index >= len(self.best_path) - 1:
            return None, "You're already at the end!"
            
        next_word = self.best_path[current_index + 1]
        
        # calculating hint costs
        current_path = self.best_path[current_index:]
        g_cost = len(current_path) - 1
        h_cost = self.search.estimate_remaining_steps(self.current_word, self.target_word)
        f_cost = g_cost + h_cost
        
        hint_message = (
        f"Using {self.selected_algorithm}\n"
        f"So far {g_cost} steps\n"
        f"Estimated {h_cost} steps remaining\n"
        f"Total estimate {f_cost} steps\n"
        f"Try: '{next_word}'"
    )

            
        return next_word, hint_message
        
    def calculate_best_path(self) -> Optional[List[str]]:
        # finding best solution
        if not self.current_word or not self.target_word:
            return None
            
        algorithm_paths = self.get_algorithm_comparison()
        
        # saving stats for each method
        self.algorithm_stats = {
            name: {
                'path': info['path'],
                'length': len(info['path']),
                'costs': info['costs']
            }
            for name, info in algorithm_paths.items()
        }
        
        # using selected method's path if available
        if self.selected_algorithm in algorithm_paths:
            return algorithm_paths[self.selected_algorithm]['path']
        
        # otherwise use shortest path we found
        valid_paths = [info['path'] for info in algorithm_paths.values()]
        return min(valid_paths, key=len) if valid_paths else None
        
    def calculate_score(self) -> int:
        # calculating score
        if not self.best_path:
            return 0
            
        optimal_moves = len(self.best_path) - 1
        actual_moves = len(self.moves) - 1
        
        if actual_moves == 0:
            return 0
            
        remaining_moves = self.move_limit - actual_moves
        
        # base score depends on efficiency
        base_score = min(1000 * (optimal_moves / actual_moves), 1000)
        # bonus for saving moves
        move_bonus = remaining_moves * 100
        
        # different modes get different multipliers
        multipliers = {
            "beginner": 1.0,
            "advanced": 1.5,
            "challenge": 2.0
        }
        
        return int((base_score + move_bonus) * multipliers.get(self.difficulty, 1.0))
        
    def start_new_game(self, start_word: str, target_word: str) -> bool:
        try:
            start_word = start_word.lower()
            target_word = target_word.lower()
            
            # checking if words are valid
            if not (self.is_word_valid(start_word) and self.is_word_valid(target_word)):
                return False
                
            # making sure there's a path between words
            path, _ = self.search.astar(start_word, target_word)
            if not path:
                return False
                
            # setting up new game
            self.current_word = start_word
            self.target_word = target_word
            self.moves = [start_word]
            self.best_path = path
            self.score = 0
            self.algorithm_stats = {}
            return True
        except Exception as e:
            print(f"Issue in starting a new game: {str(e)}")
            return False
        
    def make_move(self, new_word: str) -> bool:
        try:
            new_word = new_word.lower()
            if not self.is_valid_move(new_word):
                return False
                
            self.current_word = new_word
            self.moves.append(new_word)
            return True
        except Exception as e:
            print(f"Move Failed: {str(e)}")
            return False
        
    def is_solved(self) -> bool:
        # checking if puzzle solved
        return self.current_word == self.target_word
        
    def get_minimum_moves(self) -> int:
        # kitne minimum moves chahiye
        return len(self.best_path) - 1 if self.best_path else 0
        
    def get_current_moves(self) -> int:
        # kitne moves ho gaye
        return len(self.moves) - 1
        
    def get_remaining_moves(self) -> int:
        # kitne moves baki hain
        return self.move_limit - self.get_current_moves()