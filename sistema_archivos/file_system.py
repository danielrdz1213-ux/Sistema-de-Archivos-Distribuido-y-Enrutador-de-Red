"""Módulo 1 - Estructura base del Sistema de Archivos Distribuido.

Define la clase FileSystem, el árbol que simula el disco duro del servidor.
Al construirse crea automáticamente el nodo raíz "/" de tipo Carpeta.
"""

from .nodo import Nodo


class FileSystem:
    """Árbol de directorios que representa el disco duro del servidor.

    Atributos:
        raiz: Nodo raíz, siempre una carpeta llamada "/".
        directorio_actual: Directorio de trabajo actual; inicia en la raíz y
            será usado por los módulos de navegación posteriores.
    """

    def __init__(self):
        """Inicializa el sistema de archivos con su nodo raíz "/"."""
        self.raiz = Nodo("Carpeta", "/")
        self.directorio_actual = self.raiz

    def esta_vacio(self):
        """Devuelve True si la raíz todavía no contiene ningún nodo hijo."""
        return self.raiz.get_cantidad_hijos() == 0

    def __repr__(self):
        """Representación de depuración del sistema de archivos."""
        return (
            f"FileSystem(raiz={self.raiz.nombre!r}, "
            f"directorio_actual={self.directorio_actual.nombre!r}, "
            f"nodos_en_raiz={self.raiz.get_cantidad_hijos()})"
        )
