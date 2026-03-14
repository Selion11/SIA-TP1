import sys
import yaml
from games.sokoban import SokobanGame
from search_engines.bfs import BFS
from search_engines.dfs import DFS

def load_config(config_file="config.yaml"):
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file) or {}
    except Exception as e:
        print(f"Error loading config file: {e}")
        sys.exit(1)

def load_map(map_path):
    try:
        with open(map_path, 'r', encoding='utf-8') as file:
            # We don't strip spaces at the right because it might affect board dimensions in some implementations, 
            # but rstrip('\n') is fine. Let's just strictly keep the lines except trailing newlines.
            return [line.rstrip('\n') for line in file.readlines()]
    except Exception as e:
        print(f"Error loading map file: {e}")
        sys.exit(1)

def run(force_no_visualize=False):
    config = load_config()
    
    map_path = config.get("board", "maps/level_1.txt")
    algorithm = config.get("algorithm", "bfs")
    visualize = config.get("visualize", False)
    
    map_data = load_map(map_path)
    game = SokobanGame(map_data)
    
    print(f"Buscando solución con algoritmo: {algorithm.upper()}...")
    
    algorithms = {
        "bfs": BFS(),
        "dfs": DFS()
        # Agregar otros algoritmos como "dfs": DFS(), "a_star": AStar(), etc.
    }
    
    algo_instance = algorithms.get(algorithm.lower())
    
    if algo_instance is None:
        print(f"El algoritmo '{algorithm}' no está soportado aún.")
        sys.exit(1)
        
    solution, nodes = algo_instance.search(game)
    
    if solution is not None:
        print(f"¡Éxito! Pasos: {len(solution)}")
        print(f"Camino: {' -> '.join(solution)}")
        print(f"Nodos expandidos: {nodes}")
        
        if visualize and not force_no_visualize:
            try:
                from visualizer import run_visualization
                print("Iniciando visualización...")
                run_visualization(game, solution)
            except ImportError as e:
                print("No se pudo iniciar la visualización. Probablemente falta instalar 'pygame'.")
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error al iniciar la visualización: {e}")
        elif visualize and force_no_visualize:
            print("Visualización desactivada por el entorno de ejecución (ej. Docker).")
    else:
        print("No se encontró solución.")
        print(f"Nodos expandidos: {nodes}")

if __name__ == "__main__":
    run()