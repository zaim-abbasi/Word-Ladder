from typing import List, Dict, Optional, Tuple
from word_graph import WordGraph
import heapq

class SimpleQueue:
    def __init__(self):
        # simple queue for bfs
        self.items_to_process = []
    
    def add_item(self, item):
        self.items_to_process.append(item)
    
    def get_next_item(self):
        if not self.is_empty():
            return self.items_to_process.pop(0)
        return None
    
    def is_empty(self):
        return len(self.items_to_process) == 0

class SmartQueue:
    def __init__(self):
        # smart queue for ucs and a*, using heapq for proper ordering
        self.items_to_process = []
        self.item_counter = 0  # need this to keep fifo order when priority same

    def is_empty(self):
        return len(self.items_to_process) == 0

    def add_item(self, item, priority):
        # adding item with priority, counter helps maintain order
        heapq.heappush(self.items_to_process, (priority, self.item_counter, item))
        self.item_counter += 1

    def get_next_item(self):
        # getting item with lowest priority
        return heapq.heappop(self.items_to_process)[2]

class SearchAlgorithms:
    def __init__(self, word_graph: WordGraph):
        self.word_graph = word_graph

    def get_steps_taken(self, path: List[str]) -> int:
        # g(n): counting steps we took so far
        return len(path) - 1

    def estimate_remaining_steps(self, current_word: str, target_word: str) -> int:
        # h(n): heuristic - counting different letters between words
        if len(current_word) != len(target_word):
            return float('inf')
        
        return sum(1 for i in range(len(current_word)) 
                  if current_word[i] != target_word[i])

    def calculate_total_cost(self, steps_taken: int, estimated_steps: int) -> int:
        # f(n) = g(n) + h(n): total cost calculation
        return steps_taken + estimated_steps

    def get_path_stats(self, path: List[str], target_word: str) -> Dict[str, int]:
        # getting all the stats about path, very useful info
        current_word = path[-1]
        steps_taken = self.get_steps_taken(path)
        estimated_steps = self.estimate_remaining_steps(current_word, target_word)
        total_cost = self.calculate_total_cost(steps_taken, estimated_steps)
        
        return {
            'g_cost': steps_taken,
            'h_cost': estimated_steps,
            'f_cost': total_cost,
            'path_length': len(path)
        }

    def bfs(self, start_word: str, target_word: str) -> Tuple[Optional[List[str]], Dict[str, int]]:
        # bfs search - goes level by level
        if not (self.word_graph.word_exists(start_word) and self.word_graph.word_exists(target_word)):
            return None, {}

        search_queue = SimpleQueue()
        search_queue.add_item((start_word, [start_word]))
        visited_words = {start_word}
        
        while not search_queue.is_empty():
            current_word, current_path = search_queue.get_next_item()
            
            if current_word == target_word:
                return current_path, self.get_path_stats(current_path, target_word)

            for next_word in self.word_graph.get_neighbors(current_word):
                if next_word not in visited_words:
                    visited_words.add(next_word)
                    new_path = current_path + [next_word]
                    search_queue.add_item((next_word, new_path))

        return None, {}

    def ucs(self, start_word: str, target_word: str) -> Tuple[Optional[List[str]], Dict[str, int]]:
        # ucs search - uniform cost search
        if not (self.word_graph.word_exists(start_word) and self.word_graph.word_exists(target_word)):
            return None, {}

        search_queue = SmartQueue()
        search_queue.add_item((start_word, [start_word]), 0)
        visited_words = {start_word}
        
        while not search_queue.is_empty():
            current_word, current_path = search_queue.get_next_item()
            
            if current_word == target_word:
                return current_path, self.get_path_stats(current_path, target_word)

            for next_word in self.word_graph.get_neighbors(current_word):
                if next_word not in visited_words:
                    visited_words.add(next_word)
                    new_path = current_path + [next_word]
                    path_cost = self.get_steps_taken(new_path)
                    search_queue.add_item((next_word, new_path), path_cost)

        return None, {}

    def astar(self, start_word: str, target_word: str) -> Tuple[Optional[List[str]], Dict[str, int]]:
        # a* search - smart search using heuristics
        if not (self.word_graph.word_exists(start_word) and self.word_graph.word_exists(target_word)):
            return None, {}

        search_queue = SmartQueue()
        initial_estimate = self.estimate_remaining_steps(start_word, target_word)
        search_queue.add_item((start_word, [start_word]), initial_estimate)
        visited_words = {start_word}
        path_costs = {start_word: 0}
        
        while not search_queue.is_empty():
            current_word, current_path = search_queue.get_next_item()
            
            if current_word == target_word:
                return current_path, self.get_path_stats(current_path, target_word)

            for next_word in self.word_graph.get_neighbors(current_word):
                if next_word not in visited_words:
                    visited_words.add(next_word)
                    new_path = current_path + [next_word]
                    steps_taken = self.get_steps_taken(new_path)
                    estimated_steps = self.estimate_remaining_steps(next_word, target_word)
                    total_cost = self.calculate_total_cost(steps_taken, estimated_steps)
                    path_costs[next_word] = steps_taken
                    search_queue.add_item((next_word, new_path), total_cost)

        return None, {}