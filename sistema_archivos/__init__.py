"""Sistema de Archivos Distribuido - Módulo 1 (estructura base).

Expone las clases públicas del árbol de directorios para que los módulos
siguientes (menús, búsqueda, eliminación y enrutador de red) las importen
directamente del paquete:

    from sistema_archivos import FileSystem, Nodo
"""

from .file_system import FileSystem
from .nodo import Nodo

__all__ = ["FileSystem", "Nodo"]
