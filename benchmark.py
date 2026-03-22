import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sokoban import SokobanGame
from search_engines.bfs import BFS
from search_engines.dfs import DFS
from search_engines.a_star import AStar
from search_engines.greedy import Greedy
from visualizer import run_visualization

# Configuramos el estilo de los gráficos
sns.set_theme(style="whitegrid")

def load_map(filename):
    with open(filename, 'r') as f:
        return [list(line.rstrip('\n')) for line in f.readlines()]

def run_benchmarks():
    maps = ["level_4.txt", "level_5.txt", "level_6.txt", "level_7.txt"]
    
    # Definimos todas las combinaciones que pediste
    runs = [
        {"algo_name": "BFS", "algo_obj": BFS(), "heuristic": "Ninguna"},
        {"algo_name": "DFS", "algo_obj": DFS(), "heuristic": "Ninguna"},
        {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan"), "heuristic": "manhattan"},
        {"algo_name": "A*", "algo_obj": AStar(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"},
        {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan"), "heuristic": "manhattan"},
        {"algo_name": "Greedy", "algo_obj": Greedy(heuristic_name="manhattan_player"), "heuristic": "manhattan_player"}
    ]

    results = []
    
    # Crear carpeta para guardar todo si no existe
    os.makedirs("resultados", exist_ok=True)
    os.makedirs("resultados/gifs", exist_ok=True)
    os.makedirs("resultados/graficos", exist_ok=True)

    print("==================================================")
    print(" INICIANDO BENCHMARK AUTOMATIZADO ")
    print("==================================================")

    for map_file in maps:
        map_path = os.path.join("maps", map_file)
        if not os.path.exists(map_path):
            print(f"[Aviso] No se encontró {map_file}. Saltando...")
            continue
            
        map_name = map_file.split(".")[0]
        
        for run in runs:
            algo_name = run["algo_name"]
            heuristic = run["heuristic"]
            algo_instance = run["algo_obj"]
            
            # Formatear el nombre para el GIF
            if heuristic == "Ninguna":
                gif_name = f"resultados/gifs/{algo_name.lower()}_{map_name}.gif"
                display_name = algo_name
            else:
                gif_name = f"resultados/gifs/{algo_name.lower()}_{map_name}_{heuristic}.gif"
                display_name = f"{algo_name} ({heuristic})"
                
            print(f"\nCorriendo {map_name} con {display_name}...")
            
            game = SokobanGame(load_map(map_path))
            
            # Medimos tiempo y buscamos
            start_time = time.time()
            path, expanded, frontier = algo_instance.search(game)
            elapsed_time = time.time() - start_time
            
            steps = len(path) if path else 0
            
            # Guardar métricas
            results.append({
                "Map": map_name,
                "Algorithm": algo_name,
                "Heuristic": heuristic,
                "Time (s)": elapsed_time,
                "Expanded Nodes": expanded,
                "Frontier Nodes": frontier,
                "Steps": steps,
                "Full_Name": display_name
            })
            
            # Generar el GIF pasando el camino precalculado (solo si encontró solución)
            if path:
                print(f"Generando GIF: {gif_name}")
                game_for_viz = SokobanGame(load_map(map_path)) # Resetear mapa para el visualizador
                run_visualization(
                    game_for_viz, 
                    precomputed_path=path, 
                    save_video=True, 
                    output_filename=gif_name, 
                    auto_close=True # Se cierra solo al terminar de grabar
                )
            else:
                print("No se encontró solución (Omitiendo GIF).")

    # Guardar CSV con los datos crudos
    df = pd.DataFrame(results)
    df.to_csv("resultados/metricas_completas.csv", index=False)
    print("\nBenchmark terminado. Generando gráficos...")
    generate_plots(df)

# --- FUNCIONES DE GRAFICADO ---

def plot_4_metrics(data, x_col, hue_col, title, filename):
    """Función auxiliar para crear un panel de 4 gráficos (2x2) y guardarlo."""
    if data.empty:
        return
        
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    metrics = ["Time (s)", "Expanded Nodes", "Frontier Nodes", "Steps"]
    titles = ["Tiempo de Resolución", "Nodos Expandidos", "Nodos Frontera", "Pasos (Costo de Solución)"]
    
    for i, ax in enumerate(axes.flatten()):
        metric = metrics[i]
        sns.barplot(data=data, x=x_col, y=metric, hue=hue_col, ax=ax, palette="viridis")
        ax.set_title(titles[i])
        ax.set_ylabel(metric)
        ax.set_xlabel(x_col)
        # Mostrar valores encima de las barras
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f' if metric == "Time (s)" else '%d', padding=3, size=9)
            
    plt.tight_layout()
    plt.savefig(f"resultados/graficos/{filename}.png")
    plt.close()

def generate_plots(df):
    # 1. A* vs Greedy (Manhattan) por Mapa
    data_1 = df[(df["Algorithm"].isin(["A*", "Greedy"])) & (df["Heuristic"] == "manhattan")]
    plot_4_metrics(data_1, "Map", "Algorithm", "A* vs Greedy (Heurística: Manhattan)", "1_AStar_vs_Greedy_Manhattan")

    # 2. A* vs Greedy (Manhattan Player) por Mapa
    data_2 = df[(df["Algorithm"].isin(["A*", "Greedy"])) & (df["Heuristic"] == "manhattan_player")]
    plot_4_metrics(data_2, "Map", "Algorithm", "A* vs Greedy (Heurística: Manhattan Player)", "2_AStar_vs_Greedy_ManhattanPlayer")

    # 3. BFS vs DFS por Mapa
    data_3 = df[df["Algorithm"].isin(["BFS", "DFS"])]
    plot_4_metrics(data_3, "Map", "Algorithm", "BFS vs DFS (No Informados)", "3_BFS_vs_DFS")

    # 4. A* (Manhattan Player) en todos los mapas
    data_4 = df[(df["Algorithm"] == "A*") & (df["Heuristic"] == "manhattan_player")].copy()
    data_4["Algo_Hue"] = "A* (Manhattan Player)" # Hue dummy para formato de barras
    plot_4_metrics(data_4, "Map", "Algo_Hue", "Evolución A* (Manhattan Player) según Mapa", "4_AStar_ManhattanPlayer_Evolution")

    # 5. A* (Manhattan) en todos los mapas
    data_5 = df[(df["Algorithm"] == "A*") & (df["Heuristic"] == "manhattan")].copy()
    data_5["Algo_Hue"] = "A* (Manhattan)"
    plot_4_metrics(data_5, "Map", "Algo_Hue", "Evolución A* (Manhattan) según Mapa", "5_AStar_Manhattan_Evolution")

    # 6. Greedy (Manhattan Player) en todos los mapas
    data_6 = df[(df["Algorithm"] == "Greedy") & (df["Heuristic"] == "manhattan_player")].copy()
    data_6["Algo_Hue"] = "Greedy (Manhattan Player)"
    plot_4_metrics(data_6, "Map", "Algo_Hue", "Evolución Greedy (Manhattan Player) según Mapa", "6_Greedy_ManhattanPlayer_Evolution")

    # 7. Greedy (Manhattan) en todos los mapas
    data_7 = df[(df["Algorithm"] == "Greedy") & (df["Heuristic"] == "manhattan")].copy()
    data_7["Algo_Hue"] = "Greedy (Manhattan)"
    plot_4_metrics(data_7, "Map", "Algo_Hue", "Evolución Greedy (Manhattan) según Mapa", "7_Greedy_Manhattan_Evolution")

    # 8. DFS en todos los mapas
    data_8 = df[df["Algorithm"] == "DFS"].copy()
    data_8["Algo_Hue"] = "DFS"
    plot_4_metrics(data_8, "Map", "Algo_Hue", "Evolución DFS según Mapa", "8_DFS_Evolution")

    # 9. BFS en todos los mapas
    data_9 = df[df["Algorithm"] == "BFS"].copy()
    data_9["Algo_Hue"] = "BFS"
    plot_4_metrics(data_9, "Map", "Algo_Hue", "Evolución BFS según Mapa", "9_BFS_Evolution")

    print("¡Todos los gráficos han sido generados en la carpeta 'resultados/graficos'!")

if __name__ == "__main__":
    run_benchmarks()