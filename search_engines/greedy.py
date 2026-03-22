import heapq
import time
from itertools import count

from .search_algorithm import SearchAlgorithm
from .heuristics import heuristic_manhattan, heuristic_manhattan_player

class Greedy(SearchAlgorithm):
    # Límite en infinito para el benchmark
    def __init__(self, heuristic_name="manhattan", max_nodes=float('inf')):
        self.max_nodes = max_nodes
        self.heuristic_name = heuristic_name

    def search(self, game):
        initial_state = game.get_initial_state()
        goals = game.goals
        
        # Chequeo por si el mapa ya arranca ganado
        if game.is_goal(initial_state):
            return [], 0, 0
        
        # --- SELECCIÓN DINÁMICA DE HEURÍSTICA ---
        if self.heuristic_name == "manhattan":
            h_func = lambda s: heuristic_manhattan(s, goals)
        elif self.heuristic_name == "manhattan_player":
            h_func = lambda s: heuristic_manhattan_player(s, goals)
        else:
            print(f"[Aviso] Heurística '{self.heuristic_name}' no reconocida. Usando manhattan por defecto.")
            h_func = lambda s: heuristic_manhattan(s, goals)

        tie_breaker = count()
        initial_h = h_func(initial_state)

        # Iniciamos la frontera con el estado inicial
        frontier = []
        heapq.heappush(frontier, (initial_h, next(tie_breaker), initial_state, []))
        
        visited = set()
        nodes_expanded = 0
        start_time = time.time()

        print(f"--- Iniciando búsqueda GREEDY (Heurística: {self.heuristic_name}) ---")

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
                return None, nodes_expanded, len(frontier)

            for next_state, action in game.get_successors(state):
                if next_state not in visited:
                    new_path = path + [action]
                    
                    # EARLY GOAL TEST: Frenamos de inmediato al tocar la meta.
                    # Como Greedy no es óptimo, no perdemos nada y ganamos velocidad.
                    if game.is_goal(next_state):
                        print(f"--- ¡Solución encontrada! ---")
                        return new_path, nodes_expanded, len(frontier)
                        
                    h = h_func(next_state)
                    heapq.heappush(frontier, (h, next(tie_breaker), next_state, new_path))

        return None, nodes_expanded