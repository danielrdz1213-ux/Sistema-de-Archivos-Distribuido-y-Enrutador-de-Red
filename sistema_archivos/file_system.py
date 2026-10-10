"""Módulo 1 - Estructura base del Sistema de Archivos Distribuido.

Define la clase FileSystem, el árbol que simula el disco duro del servidor.
Al construirse crea automáticamente el nodo raíz "/" de tipo Carpeta.

Además permite crear nodos indicando la ruta del padre (por ejemplo
"/Documentos/Universidad"), mostrar el árbol completo con indentación, buscar
un nodo por su nombre en todas las ramas y eliminarlo (en cascada si es una
carpeta). No incluye menús: eso vendrá en módulos posteriores.
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
        # La raíz siempre es una carpeta llamada "/" y nunca se elimina.
        self.raiz = Nodo("Carpeta", "/")
        # El directorio de trabajo arranca ubicado en la raíz.
        self.directorio_actual = self.raiz

    def esta_vacio(self):
        """Devuelve True si la raíz todavía no contiene ningún nodo hijo."""
        # Basta con contar los hijos directos de la raíz.
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
        # La ruta debe ser texto no vacío antes de intentar recorrerla.
        if not isinstance(ruta_padre, str) or not ruta_padre.strip():
            raise ValueError("'ruta_padre' debe ser una ruta como '/' o '/Documentos'.")

        # La ruta se parte por "/": '/Documentos/Universidad' da la lista
        # ['Documentos', 'Universidad'], mientras que la raíz '/' da [].
        partes = []
        for parte in ruta_padre.split("/"):
            if parte != "":
                partes.append(parte)

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

        # Solo las carpetas pueden contener nodos dentro.
        if not actual.es_carpeta():
            raise ValueError(
                f"'{ruta_padre}' es un archivo, no una carpeta: "
                "no puede contener nodos."
            )

        nuevo_nodo = Nodo(tipo_nuevo, nombre_nuevo)  # valida tipo y nombre

        # Verificar que no exista ya un nodo con ese nombre en el destino.
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
            sangria = "    " * nivel  # 4 espacios por nivel de profundidad
            # Las carpetas llevan "/" final; la raíz se imprime sin sufijo.
            sufijo = "/" if nodo.es_carpeta() and not nodo.es_raiz() else ""
            print(f"{sangria}- {nodo.nombre}{sufijo}")
            # Bajar recursivamente a cada hijo (un nivel más adentro).
            for hijo in nodo.hijos:
                dibujar(hijo, nivel + 1)

        # El dibujo comienza en la raíz con nivel de sangría 0.
        dibujar(self.raiz, 0)

    def buscar_nodo(self, nombre_objetivo):
        """Busca un nodo por su nombre en todas las ramas del árbol.

        Recorrido recursivo en preorden: revisa cada hijo y luego baja por su
        subárbol antes de pasar al siguiente hermano. La comparación es exacta
        (sensible a mayúsculas y minúsculas) y, si el mismo nombre existe en
        varias ramas, se devuelve la primera coincidencia encontrada.

        Args:
            nombre_objetivo: Nombre del archivo o carpeta a buscar (sin ruta).

        Returns:
            La ruta completa del nodo, por ejemplo '/Documentos/nota.txt', o
            None si el nombre no existe en todo el árbol. También devuelve None
            si 'nombre_objetivo' no es un texto con al menos un carácter.
        """
        # Si el dato no es texto válido, no hay nada que buscar.
        if not isinstance(nombre_objetivo, str) or not nombre_objetivo.strip():
            return None

        # Se limpian espacios sobrantes antes de comparar nombres.
        nombre_buscado = nombre_objetivo.strip()

        # Recorrido recursivo en preorden (hijo -> subárbol -> siguiente hermano).
        def buscar(nodo, ruta_actual):
            for hijo in nodo.hijos:
                ruta_hijo = ruta_actual + "/" + hijo.nombre  # ruta acumulada
                if hijo.nombre == nombre_buscado:
                    return ruta_hijo  # coincidencia exacta: se devuelve la ruta
                encontrado = buscar(hijo, ruta_hijo)
                if encontrado is not None:
                    return encontrado  # estaba más abajo: subir el resultado
            return None  # en esta rama no está el nombre buscado

        # La búsqueda siempre arranca desde la raíz con ruta vacía.
        return buscar(self.raiz, "")

    def eliminar_nodo(self, ruta_objetivo):
        """Elimina el nodo de la ruta indicada, en cascada si es una carpeta.

        Primero se vacía recursivamente el subárbol del nodo objetivo (cada
        nodo suelta su lista de hijos y su referencia al padre) y al final el
        objetivo se quita de la lista de hijos de su padre, de modo que no
        quede ningún nodo huérfano apuntando a ramas ya eliminadas.

        Args:
            ruta_objetivo: Ruta completa del nodo, por ejemplo '/Documentos' o
                '/Documentos/Universidad/nota.txt'.

        Raises:
            ValueError: Si la ruta es inválida, si no existe o si se intenta
                eliminar el nodo raíz '/', que el árbol siempre necesita.
        """
        # La ruta debe ser texto no vacío antes de procesarla.
        if not isinstance(ruta_objetivo, str) or not ruta_objetivo.strip():
            raise ValueError("'ruta_objetivo' debe ser una ruta como '/Documentos'.")

        # La raíz no se elimina nunca
        partes = []
        for parte in ruta_objetivo.split("/"):
            if parte != "":
                partes.append(parte)

        if len(partes) == 0:
            raise ValueError("No se puede eliminar el nodo raíz '/'.")

        # Navegación desde la raíz hasta el padre del nodo objetivo
        padre = self.raiz
        for nivel in range(len(partes) - 1):
            siguiente = None
            for hijo in padre.hijos:
                if hijo.nombre == partes[nivel]:
                    siguiente = hijo
                    break
            if siguiente is None:
                ruta_parcial = "/" + "/".join(partes[:nivel + 1])
                raise ValueError(
                    f"La ruta '{ruta_objetivo}' no existe: "
                    f"no se encontró '{ruta_parcial}'."
                )
            padre = siguiente

        # El último segmento de la ruta debe ser un hijo directo de ese padre
        objetivo = None
        for hijo in padre.hijos:
            if hijo.nombre == partes[-1]:
                objetivo = hijo
                break
        if objetivo is None:  # el último segmento no es hijo de ese padre
            raise ValueError(f"La ruta '{ruta_objetivo}' no existe.")

        # Si el directorio de trabajo estaba dentro de lo eliminado, se
        # regresa a la raíz para no dejar una referencia colgante.
        cursor = self.directorio_actual
        while cursor is not None:
            if cursor is objetivo:
                self.directorio_actual = self.raiz
                break
            cursor = cursor.padre

        # Eliminación en cascada: se liberan primero las ramas más profundas
        def vaciar_subarbol(nodo):
            # Primero se vacían las ramas más profundas (postorden)...
            for hijo in nodo.hijos:
                vaciar_subarbol(hijo)
            nodo.hijos = []    # se suelta la lista de hijos
            nodo.padre = None  # se rompe el enlace con el padre

        vaciar_subarbol(objetivo)

        # El nodo objetivo sale de la lista de hijos de su propio padre
        padre.hijos.remove(objetivo)

    def __repr__(self):
        """Representación de depuración del sistema de archivos."""
        return (
            f"FileSystem(raiz={self.raiz.nombre!r}, "
            f"directorio_actual={self.directorio_actual.nombre!r}, "
            f"nodos_en_raiz={self.raiz.get_cantidad_hijos()})"
        )

