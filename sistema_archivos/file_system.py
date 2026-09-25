"""Módulo 1 - Estructura base del Sistema de Archivos Distribuido.

Define la clase FileSystem, el árbol que simula el disco duro del servidor.
Al construirse crea automáticamente el nodo raíz "/" de tipo Carpeta.

Además permite crear nodos indicando la ruta del padre (por ejemplo
"/Documentos/Universidad") y mostrar el árbol completo con indentación.
No incluye menús ni eliminaciones: eso vendrá en módulos posteriores.
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

    def crear_nodo(self, ruta_padre, nombre_nuevo, tipo_nuevo):
        """Crea un nodo dentro de la carpeta que indica 'ruta_padre'.

        La navegación siempre parte de la raíz. La ruta se separa por "/" y se
        ignoran las barras repetidas, iniciales o finales, así que "Documentos",
        "/Documentos", "//Documentos" y "/Documentos/" apuntan a lo mismo.

        Args:
            ruta_padre: Ruta de la carpeta destino, por ejemplo "/" o
                "/Documentos/Universidad".
            nombre_nuevo: Nombre del nodo que se va a crear.
            tipo_nuevo: "Carpeta" o "Archivo".

        Returns:
            El Nodo recién creado, ya enlazado a su nodo padre.

        Raises:
            ValueError: Si la ruta no existe, si el destino no es una carpeta,
                si 'tipo_nuevo' o 'nombre_nuevo' no son válidos o si ya existe
                un nodo con ese nombre dentro de la carpeta destino.
        """
        if not isinstance(ruta_padre, str) or not ruta_padre.strip():
            raise ValueError("'ruta_padre' debe ser una ruta como '/' o '/Documentos'.")

        # '/Documentos/Universidad' -> ['Documentos', 'Universidad'];  '/' -> []
        partes = [parte for parte in ruta_padre.split("/") if parte != ""]

        # Navegación desde la raíz hasta la carpeta destino
        actual = self.raiz
        for nivel in range(len(partes)):
            siguiente = None
            for hijo in actual.hijos:
                if hijo.nombre == partes[nivel]:
                    siguiente = hijo
                    break
            if siguiente is None:
                ruta_parcial = "/" + "/".join(partes[:nivel + 1])
                raise ValueError(
                    f"La ruta '{ruta_padre}' no existe: "
                    f"no se encontró '{ruta_parcial}'."
                )
            actual = siguiente

        if not actual.es_carpeta():
            raise ValueError(
                f"'{ruta_padre}' es un archivo, no una carpeta: "
                "no puede contener nodos."
            )

        nuevo_nodo = Nodo(tipo_nuevo, nombre_nuevo)  # valida tipo y nombre

        for hijo in actual.hijos:
            if hijo.nombre == nuevo_nodo.nombre:
                raise ValueError(
                    f"Ya existe un nodo llamado '{nuevo_nodo.nombre}' "
                    f"dentro de '{ruta_padre}'."
                )

        actual.agregar_hijo(nuevo_nodo)  # enlaza padre y agrega a la lista
        return nuevo_nodo

    def mostrar_arbol(self):
        """Imprime el árbol completo desde la raíz, indentado por profundidad.

        Cada nivel se desplaza cuatro espacios y las carpetas llevan una barra
        final para distinguirlas de los archivos. Ejemplo:

            - /
                - Documentos/
                    - Universidad/
                    - nota.txt
                - Musica/
        """

        def dibujar(nodo, nivel):
            sangria = "    " * nivel
            sufijo = "/" if nodo.es_carpeta() and not nodo.es_raiz() else ""
            print(f"{sangria}- {nodo.nombre}{sufijo}")
            for hijo in nodo.hijos:
                dibujar(hijo, nivel + 1)

        dibujar(self.raiz, 0)

    def __repr__(self):
        """Representación de depuración del sistema de archivos."""
        return (
            f"FileSystem(raiz={self.raiz.nombre!r}, "
            f"directorio_actual={self.directorio_actual.nombre!r}, "
            f"nodos_en_raiz={self.raiz.get_cantidad_hijos()})"
        )

