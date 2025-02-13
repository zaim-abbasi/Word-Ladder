from collections import deque
from typing import List, Set, Dict, Optional
from heapq import heappush, heappop
from word_graph import WordGraph

class SearchAlgorithms:
    def __init__(self, word_graph: WordGraph):
        self.word_graph = word_graph

    def bfs(self, start: str, target: str) -> Optional[List[str]]:
        """
        Breadth-First Search implementation to find shortest path between words.
        Returns the path as a list of words, or None if no path exists.
        """
        if not (self.word_graph.word_exists(start) and self.word_graph.word_exists(target)):
            return None

        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            current_word, path = queue.popleft()
            
            if current_word == target:
                return path

            for neighbor in self.word_graph.get_neighbors(current_word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))

        return None

    def ucs(self, start: str, target: str) -> Optional[List[str]]:
        """
        Uniform Cost Search implementation.
        Since all transformations have equal cost (1), this will behave similarly to BFS
        but is implemented with a priority queue for extensibility.
        """
        if not (self.word_graph.word_exists(start) and self.word_graph.word_exists(target)):
            return None

        # Priority queue entries are (cost, word, path)
        queue = [(0, start, [start])]
        visited = {start}

        while queue:
            cost, current_word, path = heappop(queue)

            if current_word == target:
                return path

            for neighbor in self.word_graph.get_neighbors(current_word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    # Cost increases by 1 for each transformation
                    heappush(queue, (cost + 1, neighbor, new_path))

        return None

    def _heuristic(self, word: str, target: str) -> int:
        """
        Heuristic function for A* search.
        Returns the number of differing letters between two words.
        """
        return sum(1 for a, b in zip(word, target) if a != b)

    def astar(self, start: str, target: str) -> Optional[List[str]]:
        """
        A* Search implementation using letter differences as heuristic.
        """
        if not (self.word_graph.word_exists(start) and self.word_graph.word_exists(target)):
            return None

        # Priority queue entries are (f_score, word, path)
        # f_score = g_score (path length) + heuristic
        queue = [(self._heuristic(start, target), start, [start])]
        visited = {start}
        g_scores = {start: 0}  # Cost from start to current node

        while queue:
            _, current_word, path = heappop(queue)

            if current_word == target:
                return path

            for neighbor in self.word_graph.get_neighbors(current_word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    g_score = g_scores[current_word] + 1
                    g_scores[neighbor] = g_score
                    new_path = path + [neighbor]
                    f_score = g_score + self._heuristic(neighbor, target)
                    heappush(queue, (f_score, neighbor, new_path))

        return None