import time
import heapq
from .search_algorithm import SearchAlgorithm
from .heuristics import heuristic_manhattan, heuristic_manhattan_player

class AStar(SearchAlgorithm):
    def __init__(self, heuristic_name="manhattan", max_nodes=None):
        self.max_nodes = max_nodes
        self.heuristic_name = heuristic_name

    def search(self, game, max_nodes=None):
        initial_state = game.get_initial_state()
        goals = game.goals
        self.max_nodes = max_nodes
        
        # --- SELECCIÓN DINÁMICA DE HEURÍSTICA ---
        if self.heuristic_name == "manhattan":
            h_func = lambda s: heuristic_manhattan(s, goals)
        elif self.heuristic_name == "manhattan_player":
            h_func = lambda s: heuristic_manhattan_player(s, goals)
        else:
            print(f"[Aviso] Heurística '{self.heuristic_name}' no reconocida. Usando h=0 (Dijkstra).")
            h_func = lambda s: 0 
            
        frontier = []
        tie_breaker = 0 
        
        heapq.heappush(frontier, (h_func(initial_state), tie_breaker, 0, initial_state, []))
        best_costs = {initial_state: 0}
        
        nodes_expanded = 0
        start_time = time.time()
        last_log_time = start_time
        print(f"--- Iniciando búsqueda A* (Heurística: {self.heuristic_name}) ---")
        
        while frontier:
            f_cost, _, g_cost, state, path = heapq.heappop(frontier)
            
            if g_cost > best_costs.get(state, float('inf')):
                continue

            nodes_expanded += 1
            
            if nodes_expanded % 100000 == 0: # Chequea cada 100k nodos para no ser pesado
                current_time = time.time()
                if current_time - last_log_time >= 10:
                    elapsed = current_time - start_time
                    print(f"   [VIVO] {nodes_expanded/1000000:.1f}M nodos... | Tiempo: {int(elapsed)}s | Frontera: {len(frontier)}")
                    last_log_time = current_time

            if nodes_expanded % 1000 == 0:
                elapsed = time.time() - start_time
                print(f"[LOG] Nodos expandidos: {nodes_expanded} | Frontera: {len(frontier)} | f_cost actual: {f_cost} | Tiempo: {elapsed:.2f}s")

            if self.max_nodes is not None and nodes_expanded > self.max_nodes:
                print(f"--- Límite de nodos alcanzado ({self.max_nodes}) ---")
                return None, "LIMIT", "LIMIT"

            if game.is_goal(state):
                print(f"--- ¡Solución encontrada! ---")
                return path, nodes_expanded, len(frontier)

            for next_state, action in game.get_successors(state):
                new_g_cost = g_cost + 1 
                
                if new_g_cost < best_costs.get(next_state, float('inf')):
                    best_costs[next_state] = new_g_cost
                    
                    h_cost = h_func(next_state)
                    new_f_cost = new_g_cost + h_cost
                    
                    tie_breaker += 1
                    heapq.heappush(frontier, (new_f_cost, tie_breaker, new_g_cost, next_state, path + [action]))
        
        return None, nodes_expanded, len(frontier)