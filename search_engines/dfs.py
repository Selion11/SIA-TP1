import time
from .search_algorithm import SearchAlgorithm

class DFS(SearchAlgorithm):
    # Límite en infinito para el benchmark
    def __init__(self, max_nodes=float('inf')):
        self.max_nodes = max_nodes

    def search(self, game):
        initial_state = game.get_initial_state()
        
        # Chequeo por si el mapa ya arranca ganado
        if game.is_goal(initial_state):
            return [], 0, 0
            
        frontier = [(initial_state, [])]
        visited = set()
        nodes_expanded = 0
        start_time = time.time()

        print(f"--- Iniciando búsqueda DFS ---")
        
        while frontier:
            state, path = frontier.pop()
            
            if state in visited:
                continue
                
            visited.add(state)
            nodes_expanded += 1

            # if nodes_expanded % 1000 == 0:
            #     elapsed = time.time() - start_time
            #     print(f"[LOG] Nodos expandidos: {nodes_expanded} | Frontera: {len(frontier)} | Tiempo: {elapsed:.2f}s")

            if nodes_expanded > self.max_nodes:
                print(f"--- Límite de nodos alcanzado ({self.max_nodes}) ---")
                return None, nodes_expanded, len(frontier)

            for next_state, action in game.get_successors(state):
                if next_state not in visited:
                    new_path = path + [action]
                    
                    # EARLY GOAL TEST: Frenamos ni bien generamos la solución
                    if game.is_goal(next_state):
                        print(f"--- ¡Solución encontrada! ---")
                        return new_path, nodes_expanded, len(frontier)
                        
                    frontier.append((next_state, new_path))
        
        return None, nodes_expanded, len(frontier)