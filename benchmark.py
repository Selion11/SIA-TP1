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
    
    # --- NUEVA ESTRUCTURA DE RUNS ---
    # Diccionario: { "mapa.txt": [ lista_de_algoritmos_a_correr ] }
    # Esto te permite comentar/descomentar mapas o algoritmos fácilmente.
    runs_plan = {
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
        "level_7.txt": [
            {"algo_name": "BFS", "algo_obj": BFS(), "heuristic": "Ninguna"},
            {"algo_name": "DFS", "algo_obj": DFS(), "heuristic": "Ninguna"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan"), "heuristic": "manhattan"},
            {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"}
        ]
    }

    os.makedirs("resultados/gifs", exist_ok=True)
    os.makedirs("resultados", exist_ok=True)

    # Si el archivo CSV ya existe, cargamos los datos previos para no pisarlos.
    # Si no existe, creamos una lista vacía.
    if os.path.exists(CSV_PATH):
        print(f"--- [INFO] Archivo {CSV_PATH} encontrado. Se agregarán los nuevos resultados. ---")
        existing_df = pd.read_csv(CSV_PATH)
        results = existing_df.to_dict('records')
    else:
        print(f"--- [INFO] Creando nuevo archivo {CSV_PATH}. ---")
        results = []

    print("==================================================")
    print(f" INICIANDO BENCHMARK (Límite: {MAX_NODES} nodos) ")
    print("==================================================")

    for map_file, runs in runs_plan.items():
        map_path = os.path.join("maps", map_file)
        if not os.path.exists(map_path): 
            print(f"--- [AVISO] El mapa {map_file} no existe en la carpeta 'maps/'. Saltando... ---")
            continue
            
        map_name = map_file.split(".")[0]
        
        for run in runs:
            algo_name = run["algo_name"]
            heuristic = run["heuristic"]
            algo_instance = run["algo_obj"]
            safe_algo_name = algo_name.replace("*", "star").lower()
            
            display_name = algo_name if heuristic == "Ninguna" else f"{algo_name} ({heuristic})"
            gif_name = f"resultados/gifs/{safe_algo_name}_{map_name}_{heuristic}.gif"

            print(f"\nCorriendo {map_name} con {display_name}...")
            game = SokobanGame(load_map(map_path))
            
            start_time = time.time()
            try:
                path, expanded, frontier = algo_instance.search(game, max_nodes=MAX_NODES)
                elapsed_time = time.time() - start_time
                
                if expanded == "LIMIT":
                    steps = "LIMIT"
                    print(f"--- Límite alcanzado para {display_name} ---")
                else:
                    steps = len(path) if path else 0
                    print(f"--- Completado en {elapsed_time:.2f}s ---")

            except Exception as e:
                print(f"Error inesperado en {display_name}: {e}")
                path, expanded, frontier, steps = None, "ERROR", "ERROR", "ERROR"
                elapsed_time = time.time() - start_time

            # Agregamos el resultado actual a la lista
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
            results.append(new_result)
            
            # --- GUARDADO INCREMENTAL ---
            # Guardamos el DataFrame entero cada vez que termina un algoritmo.
            # Así, si cortás con Ctrl+C o la PC se reinicia, no perdés nada.
            pd.DataFrame(results).to_csv(CSV_PATH, index=False)
            
            if path and steps != "LIMIT":
                print(f"Generando GIF...")
                game_for_viz = SokobanGame(load_map(map_path))
                run_visualization(game_for_viz, precomputed_path=path, save_video=True, 
                                  output_filename=gif_name, auto_close=True)

    print("\n==================================================")
    print(" BENCHMARK FINALIZADO ")
    print(f" Resultados guardados en: {CSV_PATH}")
    print(" Ahora podés correr 'plotter.py' para generar los gráficos.")
    print("==================================================")

if __name__ == "__main__":
    run_benchmarks()