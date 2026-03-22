import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuramos el estilo de los gráficos
sns.set_theme(style="whitegrid")

def plot_4_metrics(data, x_col, hue_col, title, filename):
    if data.empty:
        print("--- [AVISO] El DataFrame está vacío. No hay nada que graficar. ---")
        return
        
    plot_data = data.copy()
    
    # Limpieza de datos para el gráfico: convertimos textos de error a NaN
    cols_to_clean = ["Expanded Nodes", "Frontier Nodes", "Steps"]
    for col in cols_to_clean:
        plot_data[col] = pd.to_numeric(plot_data[col].replace(["LIMIT", "TIMEOUT", "OOM", "ERROR"], np.nan), errors='coerce')
        
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(title, fontsize=18, fontweight='bold')
    metrics = ["Time (s)", "Expanded Nodes", "Frontier Nodes", "Steps"]
    
    for i, ax in enumerate(axes.flatten()):
        metric = metrics[i]
        
        # Generamos el barplot
        sns.barplot(data=plot_data, x=x_col, y=metric, hue=hue_col, ax=ax, palette="viridis")
        ax.set_title(f"Comparativa de {metric}", fontsize=14)
        ax.set_xlabel("Mapa", fontsize=12)
        ax.set_ylabel(metric, fontsize=12)
        
        # Movemos la leyenda afuera para que no tape las barras
        if i == 1: # Solo la ponemos en el gráfico superior derecho para no repetir
            ax.legend(title="Algoritmo", bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            ax.get_legend().remove()
            
        # Agregamos las etiquetas de valores arriba de las barras
        for container in ax.containers:
            labels = []
            for v in container.datavalues:
                if pd.isna(v):
                    labels.append('Fallo\n(Límite)') # Cartel si llegó a 12M nodos
                else:
                    if metric == "Time (s)":
                        labels.append(f'{v:.2f}s')
                    elif v >= 1000000:
                        labels.append(f'{v/1000000:.1f}M') # Formato para millones
                    elif v >= 1000:
                        labels.append(f'{v/1000:.1f}k') # Formato para miles
                    else:
                        labels.append(f'{int(v)}')
                        
            ax.bar_label(container, labels=labels, padding=3, size=8)
            
    plt.tight_layout()
    plt.savefig(f"resultados/graficos/{filename}.png", bbox_inches='tight')
    plt.close()

def generate_plots():
    csv_path = "resultados/metricas_completas.csv"
    
    # Verificamos si hay datos para leer
    if not os.path.exists(csv_path):
        print(f"--- [ERROR] No se encontró el archivo {csv_path}. Corré el benchmark primero. ---")
        return
        
    # Aseguramos que exista la carpeta de gráficos
    os.makedirs("resultados/graficos", exist_ok=True)
    
    print(f"--- Leyendo datos desde {csv_path}... ---")
    df = pd.read_csv(csv_path)
    
    print("--- Generando gráfico 10_Global_Overview.png... ---")
    plot_4_metrics(df, "Map", "Full_Name", "Comparativa Global de Algoritmos (Sokoban)", "10_Global_Overview")
    
    print("==================================================")
    print(" ¡Gráficos generados con éxito en 'resultados/graficos'! ")
    print("==================================================")

if __name__ == "__main__":
    generate_plots()