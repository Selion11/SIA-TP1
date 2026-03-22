import time
from collections import deque
from .search_algorithm import SearchAlgorithm

class BFS(SearchAlgorithm):
    # Cambiamos a infinito para no trabar el benchmark
    def __init__(self, max_nodes=float('inf')):
        self.max_nodes = max_nodes

    def search(self, game):
        initial_state = game.get_initial_state()
        
        # Si el estado inicial ya es la victoria, terminamos de inmediato
        if game.is_goal(initial_state):
            return [], 0, 0

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
                return None, nodes_expanded, len(frontier)

            for next_state, action in game.get_successors(state):
                if next_state not in visited:
                    new_path = path + [action]
                    
                    # EARLY GOAL TEST: Chequeamos si es meta ANTES de mandarlo a la frontera.
                    # Esto evita encolar miles de nodos inútiles de la última capa del árbol.
                    if game.is_goal(next_state):
                        print(f"--- ¡Solución encontrada! ---")
                        return new_path, nodes_expanded, len(frontier)

                    visited.add(next_state)
                    frontier.append((next_state, new_path))
        
        return None, nodes_expanded, len(frontier)