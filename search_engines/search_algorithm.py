from abc import ABC, abstractmethod

class SearchAlgorithm(ABC):
    @abstractmethod
    def search(self, game):
        """
        Ejecuta el algoritmo de búsqueda para el juego dado.
        
        Args:
            game: Instancia del juego (ej: SokobanGame).
            
        Returns:
            Una tupla (solucion_camino, nodos_expandidos, nodos_frontera)
            o (None, nodos_expandidos, nodos_frontera) si no se halló solución.
        """
        pass
