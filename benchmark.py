import os
# --- MAGIA MODO FANTASMA ---
os.environ["SDL_VIDEODRIVER"] = "dummy" 

import time
import pandas as pd

from games.sokoban import SokobanGame
from search_engines.bfs import BFS
from search_engines.dfs import DFS
from search_engines.a_star import AStar
from search_engines.greedy import Greedy
from visualizer import run_visualization

def load_map(filename):
    with open(filename, 'r') as f:
        return [list(line.rstrip('\n')) for line in f.readlines()]

def run_benchmarks():
    MAX_NODES = 12000000  # Límite de 12 Millones de nodos
    CSV_PATH = "resultados/metricas_completas.csv"
    
    runs_plan = {
        "level_1.txt": [
            {"algo_name": "BFS", "algo_obj": BFS(), "heuristic": "Ninguna"},
            {"algo_name": "DFS", "algo_obj": DFS(), "heuristic": "Ninguna"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"}
        ],
        "level_2.txt": [
            {"algo_name": "BFS", "algo_obj": BFS(), "heuristic": "Ninguna"},
            {"algo_name": "DFS", "algo_obj": DFS(), "heuristic": "Ninguna"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"}
        ],
        "level_3.txt": [
            {"algo_name": "BFS", "algo_obj": BFS(), "heuristic": "Ninguna"},
            {"algo_name": "DFS", "algo_obj": DFS(), "heuristic": "Ninguna"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"}
        ],
        "level_4.txt": [
            {"algo_name": "BFS", "algo_obj": BFS(), "heuristic": "Ninguna"},
            {"algo_name": "DFS", "algo_obj": DFS(), "heuristic": "Ninguna"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"}
        ],
        "level_5.txt": [
            {"algo_name": "BFS", "algo_obj": BFS(), "heuristic": "Ninguna"},
            {"algo_name": "DFS", "algo_obj": DFS(), "heuristic": "Ninguna"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"}
        ],
        "level_6.txt": [
            {"algo_name": "BFS", "algo_obj": BFS(), "heuristic": "Ninguna"},
            {"algo_name": "DFS", "algo_obj": DFS(), "heuristic": "Ninguna"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"}
        ],
        # "level_7.txt": [
        #     {"algo_name": "BFS", "algo_obj": BFS(), "heuristic": "Ninguna"},
        #     {"algo_name": "DFS", "algo_obj": DFS(), "heuristic": "Ninguna"},
        #     {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan"), "heuristic": "manhattan"},
        #     {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"},
        #     {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan"), "heuristic": "manhattan"},
        #     {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"}
        # ]
    }

    os.makedirs("resultados/gifs", exist_ok=True)
    os.makedirs("resultados", exist_ok=True)

    # --- 1. MEMORIA DE CORRIDAS PREVIAS ---
    completed_runs = set()
    if os.path.exists(CSV_PATH):
        try:
            df_existing = pd.read_csv(CSV_PATH)
            # Guardamos tuplas de (Mapa, Nombre_Algoritmo) que ya están en el CSV
            for _, row in df_existing.iterrows():
                completed_runs.add((row['Map'], row['Full_Name']))
            print(f"--- [INFO] Se encontraron {len(completed_runs)} corridas previas en {CSV_PATH}. Se omitirán. ---")
        except Exception as e:
            print(f"--- [AVISO] El CSV existe pero hubo un error al leerlo: {e}. Empezando de cero. ---")

    print("==================================================")
    print(f" INICIANDO BENCHMARK (Límite: {MAX_NODES} nodos) ")
    print("==================================================")

    for map_file, runs in runs_plan.items():
        map_path = os.path.join("maps", map_file)
        if not os.path.exists(map_path): 
            continue
            
        map_name = map_file.split(".")[0]
        
        for run in runs:
            algo_name = run["algo_name"]
            heuristic = run["heuristic"]
            algo_instance = run["algo_obj"]
            safe_algo_name = algo_name.replace("*", "star").lower()
            display_name = algo_name if heuristic == "Ninguna" else f"{algo_name} ({heuristic})"
            gif_name = f"resultados/gifs/{safe_algo_name}_{map_name}_{heuristic}.gif"

            # --- 2. VERIFICACIÓN ANTES DE CORRER ---
            if (map_name, display_name) in completed_runs:
                print(f"⏩ Saltando {map_name} con {display_name} (Ya calculado anteriormente)")
                continue

            print(f"\n▶️ Corriendo {map_name} con {display_name}...")
            game = SokobanGame(load_map(map_path))
            
            start_time = time.time()
            try:
                path, expanded, frontier = algo_instance.search(game, max_nodes=MAX_NODES)
                elapsed_time = time.time() - start_time
                
                if expanded == "LIMIT":
                    steps = "LIMIT"
                    print(f"--- ⚠️ Límite alcanzado para {display_name} ---")
                else:
                    steps = len(path) if path else 0
                    print(f"--- ✅ Completado en {elapsed_time:.2f}s ---")

            except Exception as e:
                print(f"--- ❌ Error inesperado en {display_name}: {e} ---")
                path, expanded, frontier, steps = None, "ERROR", "ERROR", "ERROR"
                elapsed_time = time.time() - start_time

            new_result = {
                "Map": map_name, 
                "Algorithm": algo_name, 
                "Heuristic": heuristic,
                "Time (s)": elapsed_time, 
                "Expanded Nodes": expanded,
                "Frontier Nodes": frontier, 
                "Steps": steps, 
                "Full_Name": display_name
            }
            
            # --- 3. APPEND AL CSV ---
            # Verificamos si el archivo existe en ESTE exacto momento para saber si le ponemos las cabeceras (header)
            file_exists = os.path.isfile(CSV_PATH)
            df_new = pd.DataFrame([new_result]) # Metemos el dict en una lista para hacer 1 sola fila
            df_new.to_csv(CSV_PATH, mode='a', header=not file_exists, index=False)
            
            # Agregamos al set por si el mismo algoritmo estuviera duplicado en el diccionario
            completed_runs.add((map_name, display_name))
            
            if path and steps != "LIMIT":
                print(f"Generando GIF...")
                game_for_viz = SokobanGame(load_map(map_path))
                run_visualization(game_for_viz, precomputed_path=path, save_video=True, 
                                  output_filename=gif_name, auto_close=True)

    print("\n==================================================")
    print(" BENCHMARK FINALIZADO ")
    print(f" Resultados guardados en: {CSV_PATH}")
    print("==================================================")

if __name__ == "__main__":
    run_benchmarks()