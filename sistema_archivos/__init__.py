"""Sistema de Archivos Distribuido - Módulo 1 (estructura base).

Expone las clases públicas del árbol de directorios para que los módulos
siguientes (menús, búsqueda, eliminación y enrutador de red) las importen
directamente del paquete:

    from sistema_archivos import FileSystem, Nodo
"""

# Se importan las clases "públicas" del paquete para reexportarlas...
from .file_system import FileSystem
from .nodo import Nodo

# ...y se declaran como las únicas que expone el import del paquete.
__all__ = ["FileSystem", "Nodo"]
