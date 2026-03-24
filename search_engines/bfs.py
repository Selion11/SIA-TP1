import time
from collections import deque
from .search_algorithm import SearchAlgorithm

class BFS(SearchAlgorithm):
    def __init__(self, max_nodes=None):
        self.max_nodes = max_nodes

    def search(self, game, max_nodes=None):
        initial_state = game.get_initial_state()
        self.max_nodes = max_nodes
        
        if game.is_goal(initial_state):
            return [], 0, 0

        frontier = deque([(initial_state, [])])
        visited = {initial_state}
        nodes_expanded = 0
        start_time = time.time()
        last_log_time = start_time
        print(f"--- Iniciando búsqueda BFS ---")
        
        while frontier:
            state, path = frontier.popleft()
            nodes_expanded += 1
            
            if nodes_expanded % 100000 == 0: # Chequea cada 100k nodos para no ser pesado
                current_time = time.time()
                if current_time - last_log_time >= 10:
                    elapsed = current_time - start_time
                    print(f"   [VIVO] {nodes_expanded/1000000:.1f}M nodos... | Tiempo: {int(elapsed)}s | Frontera: {len(frontier)}")
                    last_log_time = current_time

            if nodes_expanded % 1000 == 0:
                elapsed = time.time() - start_time
                print(f"[LOG] Nodos expandidos: {nodes_expanded} | Frontera: {len(frontier)} | Tiempo: {elapsed:.2f}s")

            if self.max_nodes is not None and nodes_expanded > self.max_nodes:
                print(f"--- Límite de nodos alcanzado ({self.max_nodes}) ---")
                return None, "LIMIT", "LIMIT"

            for next_state, action in game.get_successors(state):
                if next_state not in visited:
                    new_path = path + [action]

                    if game.is_goal(next_state):
                        print(f"--- ¡Solución encontrada! ---")
                        return new_path, nodes_expanded, len(frontier)

                    visited.add(next_state)
                    frontier.append((next_state, new_path))
        
        return None, nodes_expanded, len(frontier)