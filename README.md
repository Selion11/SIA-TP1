# Sokoban Solver

Este proyecto es una implementación de un solucionador para el juego Sokoban. Actualmente incluye motores de búsqueda BFS, DFS,A* y Greedy.

## Configuración

El comportamiento del programa puede ser modificado utilizando el archivo `config.yaml`:

```yaml
board: "maps/level_3.txt"
algorithm: "dfs"
heuristic: "manhattan"
visualize: true
save_video: false
output_filename: "sokoban_map3.gif"
```

- **board**: Ruta al archivo del nivel que se desea resolver. Los niveles disponibles están en el directorio `maps/`.
- **algorithm**: Algoritmo de búsqueda a utilizar (actualmente soportados: `bfs`, `dfs`, `greedy`o `a*`).
- **visualize**: Booleano (`true`/`false`). Si es `true` el programa abrirá una ventana en 2D mostrando el estado de la búsqueda en tiempo real ("Searching...") y luego animará la solución encontrada.
- **heuristic**: Función heurística a utilizar (solo requerida si el algoritmo es `greedy` o `a*`). Opciones disponibles:
  - `manhattan`: Calcula la distancia Manhattan pura desde cada caja hasta su objetivo más cercano.
  - `manhattan_player`: Combina la distancia Manhattan de las cajas con la distancia del jugador a la caja más cercana.

> **PUNTO DE ENTRADA DUAL:** El proyecto cuenta con dos puntos de entrada. `main.py` intenta ejecutar la visualización si se encuentra habilitada, lo cual es ideal para ejecuciones **LOCALES**. En cambio, `main_docker.py` fuerza la desactivación de la visualización (ignorando el archivo de configuración) para evitar crasheos en entornos sin interfaz gráfica nativa como **DOCKER** (es llamado automáticamente por el archivo `Dockerfile`).

---

## 🖥 Ejecución Local en Windows usando WSL (Para Animaciones UI)

Se puede correr este proyecto en Python de forma local dentro de WSL para interactuar cómodamente con el sistema y ver los recorridos del robot en pantalla.

Si utilizás WSL (preferentemente WSL2 con WSLg habilitado, que trae soporte gráfico nativo):

1. Abrí tu terminal de Ubuntu/Debian en WSL y navegá hasta la carpeta del proyecto.
2. Instalar el gestor de paquetes de python (si no lo tenés) y dependencias del sistema requeridas por pygame en Linux:

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv x11-apps -y
```

3. (Opcional pero recomendado) Crear y activar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Instalar `PyYAML` y la librería gráfica `pygame`:

```bash
pip install -r requirements.txt
```

5. Correr el programa principal:

```bash
python3 main.py
```

---

## 🐳 Ejecución mediante Docker (Procesamiento Batch)

No es necesario instalar las dependencias localmente; se puede ejecutar el proyecto directamente utilizando Docker.

### 1. Construir la imagen de Docker

Abrir una terminal en la raíz del proyecto y correr el siguiente comando para construir la imagen:

```bash
docker build -t sokoban-solver .
```

### 2. Correr el contenedor

Una vez construida la imagen, se puede ejecutar el programa con:

```bash
docker run --rm sokoban-solver
```

### 3. Ejecutar aplicando cambios en caliente (Opcional)

Si se desea modificar el archivo `config.yaml` o los mapas en la carpeta `maps/` y probar los cambios sin tener que reconstruir la imagen completa de Docker cada vez, se puede montar los archivos locales dentro del contenedor de la siguiente forma:

**En Windows (PowerShell):**

```powershell
docker run --rm -v ${PWD}:/app sokoban-solver
```

**En Linux o Mac:**

```bash
docker run --rm -v $(pwd):/app sokoban-solver
```


### 4. Ejecutar en modo 'batch'

Si se desea generar una ejecucion en modo batch es necesario modificar el archivo `benchmark.py`. En la linea 23 del archivo se encontrara el comienzo de un array llamado `runs_plan`. Este array contendra todas las corridas de la siguiente manera:

```bash
"map_name":{
   {"algo_name": "Algorithm_name", "algo_obj": Algorithm_function, "heuristic": "heurisitc_name"},
}
```
- **heuristic_name**: Es el nobre de la heuristica mencionada en el paso de configuracion.
- **algorithm_name**: Es el algoritmo a utilizar BFS,DFS,A* o Greedy.
- **algorithm_function**: Funcion que utiliza el algoritmo seleccionado. BFS(), DFS(), 
AStar(heuristic_name="heurisitc_name"), Greedy(heuristic_name="heurisitc_name").

Una vez seteadas las corridas deseadas se debe correr el siguiente comando desde la raiz del proyecto

```bash
python ./benchmark.py 
```

### 5. Generar los graficos para estudiar los resultados del benchmark

Esto se puede realizar unicamente despues de generado el benchmark del punto anterior. Desde la raiz del proyecto se debe correr el siguiente comando

```bash
python ./plotter.py 
```

Esto generara los siguientes graficos:

- Comparacion entre a* y greedy con manhattan para cada mapa comparando (un grafico por punto):

  1) Tiempo que tarda en llegar a la solucion

  2) Nodos totales expanidos

  3) Nodos frontera

  4) Pasos de la solucion optima

- Comparacion entre a* y greedy con manhattan_player para cada mapa (un grafico por punto):

  1) Tiempo que tarda en llegar a la solucion

  2) Nodos totales expanidos

  3) Nodos frontera

  4) Pasos de la solucion optima

- Comparacion entre bfs y dfs para cada mapa (un grafico por punto):

  1) Tiempo que tarda en llegar a la solucion

  2) Nodos totales expanidos

  3) Nodos frontera

  4) Pasos de la solucion optima

- Comparacion entre a* con manhattan_player analizando las corridas de todos los mapas comparando (un grafico por punto) para poder comarar la eficiencia de esto segun la complejidad del mapa:

  1) Tiempo que tarda en llegar a la solucion

  2) Nodos totales expanidos

  3) Nodos frontera

  4) Pasos de la solucion optima

- Comparacion entre a* con manhattan analizando las corridas de todos los mapas comparando (un grafico por punto) para poder comarar la eficiencia de esto segun la complejidad del mapa:

  1) Tiempo que tarda en llegar a la solucion

  2) Nodos totales expanidos

  3) Nodos frontera

  4) Pasos de la solucion optima

- Comparacion entre greedy con manhattan_player analizando las corridas de todos los mapas comparando (un grafico por punto) para poder comarar la eficiencia de esto segun la complejidad del mapa:

  1) Tiempo que tarda en llegar a la solucion

  2) Nodos totales expanidos

  3) Nodos frontera

  4) Pasos de la solucion optima

- Comparacion entre greedy con manhattan analizando las corridas de todos los mapas comparando (un grafico por punto) para poder comarar la eficiencia de esto segun la complejidad del mapa:

  1) Tiempo que tarda en llegar a la solucion

  2) Nodos totales expanidos

  3) Nodos frontera

  4) Pasos de la solucion optima

- Comparacion entre dfs analizando las corridas de todos los mapas comparando (un grafico por punto) para poder comarar la eficiencia de esto segun la complejidad del mapa:

  1) Tiempo que tarda en llegar a la solucion

  2) Nodos totales expanidos

  3) Nodos frontera

  4) Pasos de la solucion optima

- Comparacion entre bfs analizando las corridas de todos los mapas comparando (un grafico por punto) para poder comarar la eficiencia de esto segun la complejidad del mapa:

  1) Tiempo que tarda en llegar a la solucion

  2) Nodos totales expanidos

  3) Nodos frontera

  4) Pasos de la solucion optima