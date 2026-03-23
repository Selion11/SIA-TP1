import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_theme(style="whitegrid")

def plot_4_metrics(data, x_col, hue_col, title, filename):
    if data.empty:
        print(f"  -> Omitiendo {filename} (No hay datos para estos filtros)")
        return
        
    plot_data = data.copy()
    
    cols_to_clean = ["Expanded Nodes", "Frontier Nodes", "Steps", "Time (s)"]
    for col in cols_to_clean:
        plot_data[col] = pd.to_numeric(plot_data[col].replace(["OOM", "LIMIT", "TIMEOUT", "ERROR"], np.nan), errors='coerce')
        
    # 1. Agrandamos el tamaño de la figura (de 14x10 a 18x12)
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle(title, fontsize=18, fontweight='bold')
    
    metrics = ["Time (s)", "Expanded Nodes", "Frontier Nodes", "Steps"]
    titles = ["Tiempo de Resolución", "Nodos Expandidos", "Nodos Frontera", "Pasos (Costo de Solución)"]
    
    for i, ax in enumerate(axes.flatten()):
        metric = metrics[i]
        
        sns.barplot(data=plot_data, x=x_col, y=metric, hue=hue_col, ax=ax, palette="viridis")
        ax.set_title(titles[i], fontsize=14)
        ax.set_ylabel(metric, fontsize=12)
        ax.set_xlabel("Mapa", fontsize=12)
        
        for container in ax.containers:
            labels = []
            for v in container.datavalues:
                if pd.isna(v):
                    labels.append('FALLÓ')
                else:
                    labels.append(f'{v:.2f}' if metric == "Time (s)" else f'{int(v)}')
            
            # 2. Achicamos la letra (size=7) y rotamos el texto 90 grados
            ax.bar_label(container, labels=labels, padding=4, size=7, rotation=90)
            
        # 3. Movemos la leyenda afuera del gráfico superior derecho, borramos las demás
        if i == 1: 
            ax.legend(title="Algoritmo", bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            if ax.get_legend() is not None:
                ax.get_legend().remove()
            
    plt.tight_layout()
    os.makedirs("resultados/graficos", exist_ok=True)
    # Usamos bbox_inches='tight' para que al guardar no recorte la leyenda que movimos afuera
    plt.savefig(f"resultados/graficos/{filename}.png", bbox_inches='tight')
    plt.close()
    print(f"  -> Generado: {filename}.png")

def generate_plots(df):
    print("Generando gráficos con formato anti-superposición...")
    
    # 1. A* vs Greedy (Manhattan)
    data_1 = df[(df["Algorithm"].isin(["A*", "Greedy"])) & (df["Heuristic"] == "manhattan")]
    plot_4_metrics(data_1, "Map", "Algorithm", "A* vs Greedy (Heurística: Manhattan)", "1_AStar_vs_Greedy_Manhattan")

    # 2. A* vs Greedy (Manhattan Player)
    data_2 = df[(df["Algorithm"].isin(["A*", "Greedy"])) & (df["Heuristic"] == "manhattan_player")]
    plot_4_metrics(data_2, "Map", "Algorithm", "A* vs Greedy (Heurística: Manhattan Player)", "2_AStar_vs_Greedy_ManhattanPlayer")

    # 3. BFS vs DFS
    data_3 = df[df["Algorithm"].isin(["BFS", "DFS"])]
    plot_4_metrics(data_3, "Map", "Algorithm", "BFS vs DFS (No Informados)", "3_BFS_vs_DFS")

    # 4. A* (Manhattan Player)
    data_4 = df[(df["Algorithm"] == "A*") & (df["Heuristic"] == "manhattan_player")].copy()
    data_4["Algo_Hue"] = "A* (Manhattan Player)"
    plot_4_metrics(data_4, "Map", "Algo_Hue", "Evolución A* (Manhattan Player)", "4_AStar_ManhattanPlayer_Evolution")

    # 5. A* (Manhattan)
    data_5 = df[(df["Algorithm"] == "A*") & (df["Heuristic"] == "manhattan")].copy()
    data_5["Algo_Hue"] = "A* (Manhattan)"
    plot_4_metrics(data_5, "Map", "Algo_Hue", "Evolución A* (Manhattan)", "5_AStar_Manhattan_Evolution")

    # 6. Greedy (Manhattan Player)
    data_6 = df[(df["Algorithm"] == "Greedy") & (df["Heuristic"] == "manhattan_player")].copy()
    data_6["Algo_Hue"] = "Greedy (Manhattan Player)"
    plot_4_metrics(data_6, "Map", "Algo_Hue", "Evolución Greedy (Manhattan Player)", "6_Greedy_ManhattanPlayer_Evolution")

    # 7. Greedy (Manhattan)
    data_7 = df[(df["Algorithm"] == "Greedy") & (df["Heuristic"] == "manhattan")].copy()
    data_7["Algo_Hue"] = "Greedy (Manhattan)"
    plot_4_metrics(data_7, "Map", "Algo_Hue", "Evolución Greedy (Manhattan)", "7_Greedy_Manhattan_Evolution")

    # 8. DFS
    data_8 = df[df["Algorithm"] == "DFS"].copy()
    data_8["Algo_Hue"] = "DFS"
    plot_4_metrics(data_8, "Map", "Algo_Hue", "Evolución DFS", "8_DFS_Evolution")

    # 9. BFS
    data_9 = df[df["Algorithm"] == "BFS"].copy()
    data_9["Algo_Hue"] = "BFS"
    plot_4_metrics(data_9, "Map", "Algo_Hue", "Evolución BFS", "9_BFS_Evolution")

    # 10. Global
    plot_4_metrics(df, "Map", "Full_Name", "Comparativa Global de Todos los Algoritmos", "10_Global_Overview")

if __name__ == "__main__":
    csv_path = "resultados/metricas_completas.csv"
    if os.path.exists(csv_path):
        print("Leyendo y limpiando datos del benchmark...")
        df_resultados = pd.read_csv(csv_path)
        
        # Limpieza de espacios en blanco
        df_resultados['Algorithm'] = df_resultados['Algorithm'].str.strip()
        df_resultados['Heuristic'] = df_resultados['Heuristic'].str.strip()
        df_resultados['Map'] = df_resultados['Map'].str.strip()
        
        generate_plots(df_resultados)
        print("\n¡Proceso finalizado! Revisá la carpeta 'resultados/graficos'")
    else:
        print(f"ERROR: No se encontró el archivo {csv_path}.")