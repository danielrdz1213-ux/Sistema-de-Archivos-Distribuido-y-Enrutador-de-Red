"""Módulo 1 - Estructura base del Sistema de Archivos Distribuido.

Define la unidad mínima del árbol de directorios: la clase Nodo, capaz de
representar tanto una Carpeta como un Archivo.

Este módulo NO incluye menús, ni algoritmos de búsqueda o eliminación; dichas
operaciones se implementarán en módulos posteriores.
"""


class Nodo:
    """Nodo del árbol de directorios (puede ser una Carpeta o un Archivo).

    Atributos:
        tipo: "Carpeta" o "Archivo".
        nombre: Nombre del nodo. La raíz del árbol siempre se llama "/".
        hijos: Lista de nodos contenidos en este nodo.
        padre: Nodo contenedor; es None únicamente en la raíz.
    """

    def __init__(self, tipo, nombre, padre=None):
        """Inicializa un nodo vacío (sin hijos)."""
        if tipo not in ["Carpeta", "Archivo"]:
            raise ValueError(
                f"'tipo' debe ser 'Carpeta' o 'Archivo', no {tipo!r}."
            )
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("'nombre' debe ser una cadena con al menos un carácter.")

        self.tipo = tipo
        self.nombre = nombre.strip()
        self.hijos = []
        self.padre = padre

    def es_carpeta(self):
        """Devuelve True si el nodo representa una carpeta."""
        return self.tipo == "Carpeta"

    def es_archivo(self):
        """Devuelve True si el nodo representa un archivo."""
        return self.tipo == "Archivo"

    def es_raiz(self):
        """Devuelve True si el nodo es la raíz del árbol (no tiene padre)."""
        return self.padre is None

    def get_cantidad_hijos(self):
        """Devuelve la cantidad de nodos contenidos directamente en este nodo."""
        return len(self.hijos)

    def agregar_hijo(self, hijo):
        """Vincula un nodo hijo manteniendo coherente la referencia al padre.

        Es una utilidad de construcción del árbol (no implementa búsquedas ni
        eliminaciones): garantiza que hijo.padre apunte a este nodo.
        """
        if not isinstance(hijo, Nodo):
            raise ValueError("'hijo' debe ser una instancia de Nodo.")
        if self.es_archivo():
            raise ValueError(
                f"El archivo '{self.nombre}' no puede contener nodos hijos."
            )
        if hijo in self.hijos:
            raise ValueError(
                f"El nodo '{hijo.nombre}' ya está registrado en '{self.nombre}'."
            )

        hijo.padre = self
        self.hijos.append(hijo)

    def __repr__(self):
        """Representación de depuración del nodo y sus relaciones."""
        nombre_padre = self.padre.nombre if self.padre is not None else None
        return (
            f"Nodo(tipo={self.tipo!r}, nombre={self.nombre!r}, "
            f"hijos={self.get_cantidad_hijos()}, padre={nombre_padre!r})"
        )
