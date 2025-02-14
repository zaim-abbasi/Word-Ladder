from collections import deque
from typing import List, Set, Dict, Optional, Tuple
from heapq import heappush, heappop
from word_graph import WordGraph

class SearchAlgorithms:
    def __init__(self, word_graph: WordGraph):
        self.word_graph = word_graph

    def g_cost(self, path: List[str]) -> int:
        return len(path) - 1

    def h_cost(self, current: str, target: str) -> int:
        return sum(1 for a, b in zip(current, target) if a != b)

    def f_cost(self, g: int, h: int) -> int:
        return g + h

    def get_path_info(self, path: List[str], target: str) -> Dict[str, int]:
        current = path[-1]
        g = self.g_cost(path)
        h = self.h_cost(current, target)
        f = self.f_cost(g, h)
        return {
            'g_cost': g,
            'h_cost': h,
            'f_cost': f,
            'path_length': len(path)
        }

    def bfs(self, start: str, target: str) -> Tuple[Optional[List[str]], Dict[str, int]]:
        if not (self.word_graph.word_exists(start) and self.word_graph.word_exists(target)):
            return None, {}

        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current_word, path = queue.popleft()
            
            if current_word == target:
                return path, self.get_path_info(path, target)

            for neighbor in self.word_graph.get_neighbors(current_word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))

        return None, {}

    def ucs(self, start: str, target: str) -> Tuple[Optional[List[str]], Dict[str, int]]:
        if not (self.word_graph.word_exists(start) and self.word_graph.word_exists(target)):
            return None, {}

        queue = [(0, start, [start])]
        visited = {start}

        while queue:
            cost, current_word, path = heappop(queue)

            if current_word == target:
                return path, self.get_path_info(path, target)

            for neighbor in self.word_graph.get_neighbors(current_word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    g_cost = self.g_cost(new_path)
                    heappush(queue, (g_cost, neighbor, new_path))

        return None, {}

    def astar(self, start: str, target: str) -> Tuple[Optional[List[str]], Dict[str, int]]:
        if not (self.word_graph.word_exists(start) and self.word_graph.word_exists(target)):
            return None, {}

        queue = [(self.h_cost(start, target), start, [start])]
        visited = {start}
        g_scores = {start: 0}

        while queue:
            _, current_word, path = heappop(queue)

            if current_word == target:
                return path, self.get_path_info(path, target)

            for neighbor in self.word_graph.get_neighbors(current_word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    g = self.g_cost(new_path)
                    h = self.h_cost(neighbor, target)
                    f = self.f_cost(g, h)
                    g_scores[neighbor] = g
                    heappush(queue, (f, neighbor, new_path))

        return None, {}