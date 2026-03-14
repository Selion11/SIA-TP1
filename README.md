# Sokoban Solver

Este proyecto es una implementación de un solucionador para el juego Sokoban. Actualmente incluye motores de búsqueda BFS, DFS y Greedy.

## Configuración

El comportamiento del programa puede ser modificado utilizando el archivo `config.yaml`:

```yaml
board: "maps/level_1.txt"
algorithm: "bfs"
visualize: true
```

- **board**: Ruta al archivo del nivel que se desea resolver. Los niveles disponibles están en el directorio `maps/`.
- **algorithm**: Algoritmo de búsqueda a utilizar (actualmente soportados: `bfs`, `dfs`, `greedy`).
- **visualize**: Booleano (`true`/`false`). Si es `true` el programa intentará abrir una ventana en 2D que animará la solución encontrada en tiempo real.

> **💡 PUNTO DE ENTRADA DUAL:** El proyecto cuenta con dos puntos de entrada. `main.py` intenta ejecutar la visualización si se encuentra habilitada, lo cual es ideal para ejecuciones **LOCALES**. En cambio, `main_docker.py` fuerza la desactivación de la visualización (ignorando el archivo de configuración) para evitar crasheos en entornos sin interfaz gráfica nativa como **DOCKER** (es llamado automáticamente por el archivo `Dockerfile`).

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
