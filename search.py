from typing import List, Dict, Optional, Tuple
from word_graph import WordGraph

# simple queue implementation
class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def is_empty(self):
        return len(self.items) == 0

# simple stack implementation
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        return len(self.items) == 0

class SearchAlgorithms:
    def __init__(self, word_graph: WordGraph):
        self.word_graph = word_graph

    # g(n): counts steps we've taken so far
    def g_cost(self, path: List[str]) -> int:
        return len(path) - 1

    # h(n): estimates remaining steps by counting different letters
    def h_cost(self, current: str, target: str) -> int:
        if len(current) != len(target):
            return float('inf')
        different_letters = 0
        for i in range(len(current)):
            if current[i] != target[i]:
                different_letters += 1
        return different_letters

    # f(n) = g(n) + h(n): total cost estimate
    def f_cost(self, g: int, h: int) -> int:
        return g + h

    # get info about a path including all costs
    def get_path_info(self, path: List[str], target: str) -> Dict[str, int]:
        current = path[-1]
        g = self.g_cost(path)  # actual steps taken
        h = self.h_cost(current, target)  # estimated steps left
        f = self.f_cost(g, h)  # total cost estimate
        
        return {
            'g_cost': g,
            'h_cost': h,
            'f_cost': f,
            'path_length': len(path)
        }

    # breadth-first search using queue
    def bfs(self, start: str, target: str) -> Tuple[Optional[List[str]], Dict[str, int]]:
        # check if words exist
        if not (self.word_graph.word_exists(start) and self.word_graph.word_exists(target)):
            return None, {}

        # use our simple queue
        queue = Queue()
        queue.enqueue((start, [start]))  # (word, path)
        seen = {start}
        
        while not queue.is_empty():
            # get next word to check
            current, path = queue.dequeue()
            
            # found the target!
            if current == target:
                return path, self.get_path_info(path, target)

            # check each neighbor
            for next_word in self.word_graph.get_neighbors(current):
                if next_word not in seen:
                    seen.add(next_word)
                    new_path = path + [next_word]
                    queue.enqueue((next_word, new_path))

        return None, {}

    # uniform cost search using list as priority queue
    def ucs(self, start: str, target: str) -> Tuple[Optional[List[str]], Dict[str, int]]:
        # check if words exist
        if not (self.word_graph.word_exists(start) and self.word_graph.word_exists(target)):
            return None, {}

        # use simple list as priority queue
        queue = [(0, start, [start])]  # (steps, word, path)
        seen = {start}

        while queue:
            # find path with lowest steps
            min_index = 0
            for i in range(len(queue)):
                if queue[i][0] < queue[min_index][0]:
                    min_index = i
            
            # remove and get the best path
            steps, current, path = queue.pop(min_index)
            
            # found the target!
            if current == target:
                return path, self.get_path_info(path, target)

            # check each neighbor
            for next_word in self.word_graph.get_neighbors(current):
                if next_word not in seen:
                    seen.add(next_word)
                    new_path = path + [next_word]
                    new_steps = self.g_cost(new_path)
                    queue.append((new_steps, next_word, new_path))

        return None, {}

    # A* search using list as priority queue
    def astar(self, start: str, target: str) -> Tuple[Optional[List[str]], Dict[str, int]]:
        # check if words exist
        if not (self.word_graph.word_exists(start) and self.word_graph.word_exists(target)):
            return None, {}

        # use simple list as priority queue
        queue = [(self.h_cost(start, target), start, [start])]  # (f_cost, word, path)
        seen = {start}
        g_scores = {start: 0}

        while queue:
            # find path with lowest total cost
            min_index = 0
            for i in range(len(queue)):
                if queue[i][0] < queue[min_index][0]:
                    min_index = i
            
            # remove and get the best path
            _, current, path = queue.pop(min_index)
            
            # found the target!
            if current == target:
                return path, self.get_path_info(path, target)

            # check each neighbor
            for next_word in self.word_graph.get_neighbors(current):
                if next_word not in seen:
                    seen.add(next_word)
                    new_path = path + [next_word]
                    g = self.g_cost(new_path)  # actual cost
                    h = self.h_cost(next_word, target)  # estimated remaining
                    f = self.f_cost(g, h)  # total estimate
                    g_scores[next_word] = g
                    queue.append((f, next_word, new_path))

        return None, {}
