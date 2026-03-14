import heapq
import time
from itertools import count

from .search_algorithm import SearchAlgorithm


class Greedy(SearchAlgorithm):
    def __init__(self, max_nodes=500000):
        self.max_nodes = max_nodes

    def _heuristic(self, state, goals):
        player, boxes = state

        if not boxes:
            return 0

        boxes_to_goals = 0
        for br, bc in boxes:
            min_dist = min(abs(br - gr) + abs(bc - gc) for gr, gc in goals)
            boxes_to_goals += min_dist

        player_to_box = min(abs(player[0] - br) + abs(player[1] - bc) for br, bc in boxes)

        return boxes_to_goals + player_to_box

    def search(self, game):
        initial_state = game.get_initial_state()
        tie_breaker = count()
        initial_h = self._heuristic(initial_state, game.goals)

        frontier = [(initial_h, next(tie_breaker), initial_state, [])]
        visited = set()
        nodes_expanded = 0
        start_time = time.time()

        print(f"--- Iniciando búsqueda GREEDY ---")

        while frontier:
            _, _, state, path = heapq.heappop(frontier)

            if state in visited:
                continue

            visited.add(state)
            nodes_expanded += 1

            if nodes_expanded % 1000 == 0:
                elapsed = time.time() - start_time
                print(f"[LOG] Nodos expandidos: {nodes_expanded} | Frontera: {len(frontier)} | Tiempo: {elapsed:.2f}s")

            if nodes_expanded > self.max_nodes:
                print(f"--- Límite de nodos alcanzado ({self.max_nodes}) ---")
                return None, nodes_expanded

            if game.is_goal(state):
                print(f"--- ¡Solución encontrada! ---")
                return path, nodes_expanded

            for next_state, action in game.get_successors(state):
                if next_state not in visited:
                    h = self._heuristic(next_state, game.goals)
                    heapq.heappush(frontier, (h, next(tie_breaker), next_state, path + [action]))

        return None, nodes_expanded