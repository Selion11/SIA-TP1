import time
from collections import deque
from .search_algorithm import SearchAlgorithm

class BFS(SearchAlgorithm):
    def __init__(self, max_nodes=500000):
        self.max_nodes = max_nodes

    def search(self, game):
        initial_state = game.get_initial_state()
        frontier = deque([(initial_state, [])])
        visited = {initial_state}
        nodes_expanded = 0
        start_time = time.time()

        print(f"--- Iniciando búsqueda BFS ---")
        
        while frontier:
            state, path = frontier.popleft()
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
                    visited.add(next_state)
                    frontier.append((next_state, path + [action]))
        
        return None, nodes_expanded