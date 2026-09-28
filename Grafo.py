"""
Módulo 3 - Topología y Enrutamiento de Red (Grafos)

Representa la red de servidores como un GRAFO PONDERADO:
  - Vértices: servidores.
  - Aristas: conexiones de fibra óptica entre servidores.
  - Peso de cada arista: latencia en milisegundos.

Representación: LISTA DE ADYACENCIA (diccionario de vértices donde cada
vértice guarda un diccionario {vecino: latencia}). Se eligió lista de
adyacencia porque la red es un grafo disperso (pocos enlaces por servidor),
así solo se guarda memoria por las conexiones que existen de verdad.

Las conexiones de fibra son BIDIRECCIONALES: si A se conecta con B con
latencia de 10 ms, se puede viajar en ambas direcciones con el mismo costo.

Este archivo incluye la estructura base (vértices y aristas), el algoritmo
de Dijkstra para la ruta óptima y el Ping General con BFS.
"""


class Grafo:
    def __init__(self, funcion_log=None):
        """
        adyacencia: diccionario de la forma
            { "ServidorA": {"ServidorB": 10, "ServidorC": 25}, ... }
        funcion_log: callback que el Módulo 4 (Persona D) inyectará para
            escribir en network_audit_log.txt. Si no se pasa (modo
            standalone/pruebas), se usa un logger local que solo imprime
            en consola, igual que en el Módulo 2.
        """
        self.adyacencia = {}
        self.funcion_log = funcion_log or self._log_local

    # ---------------- Vértices (servidores) ----------------
    def agregar_servidor(self, nombre):
        """Agrega un vértice nuevo al grafo.

        Returns:
            True si se agregó, False si ya existía o el nombre es inválido.
        """
        if not isinstance(nombre, str) or not nombre.strip():
            print("El nombre del servidor debe ser un texto no vacío.")
            return False

        nombre = nombre.strip()
        if nombre in self.adyacencia:
            self.funcion_log(f"Registro de servidor FALLIDO (ya existe): {nombre}")
            return False

        self.adyacencia[nombre] = {}
        self.funcion_log(f"Servidor agregado a la red: {nombre}")
        return True

    def eliminar_servidor(self, nombre):
        """Elimina un vértice y todas las conexiones que llegan a él.

        Un vértice puede aparecer en dos lugares: como llave de la lista de
        adyacencia y como vecino dentro de las listas de otros vértices.
        Si no se borra de ambos, quedarían aristas "huérfanas" apuntando a
        un servidor que ya no existe.

        Returns:
            True si se eliminó, False si no existía.
        """
        if nombre not in self.adyacencia:
            print(f"Error: el servidor '{nombre}' no existe en la red.")
            return False

        # Quitar todas las aristas de otros servidores que apuntan a este
        for vecinos in self.adyacencia.values():
            if nombre in vecinos:
                del vecinos[nombre]

        # Quitar el vértice mismo (sus conexiones salientes se van con él)
        del self.adyacencia[nombre]
        self.funcion_log(f"Servidor eliminado de la red: {nombre}")
        return True

    # ---------------- Aristas (conexiones de fibra) ----------------
    def agregar_conexion(self, origen, destino, latencia_ms):
        """Conecta dos servidores con fibra (arista bidireccional ponderada).

        Args:
            origen: Nombre del primer servidor.
            destino: Nombre del segundo servidor.
            latencia_ms: Peso de la arista, en milisegundos (debe ser > 0).

        Returns:
            True si se creó/actualizó la conexión, False si hubo error.
        """
        if origen not in self.adyacencia:
            print(f"Error: el servidor '{origen}' no existe en la red.")
            return False
        if destino not in self.adyacencia:
            print(f"Error: el servidor '{destino}' no existe en la red.")
            return False
        if origen == destino:
            print("Error: no se puede conectar un servidor consigo mismo.")
            return False
        if not isinstance(latencia_ms, (int, float)) or latencia_ms <= 0:
            print("Error: la latencia debe ser un número mayor que 0 ms.")
            return False

        # Fibra bidireccional: se registra la arista en ambas direcciones
        self.adyacencia[origen][destino] = latencia_ms
        self.adyacencia[destino][origen] = latencia_ms
        self.funcion_log(
            f"Conexión establecida: {origen} <-> {destino} ({latencia_ms} ms)"
        )
        return True

    def eliminar_conexion(self, origen, destino):
        """Elimina la arista entre dos servidores (en ambas direcciones).

        Returns:
            True si la conexión existía y se eliminó, False en caso contrario.
        """
        if origen not in self.adyacencia:
            print(f"Error: el servidor '{origen}' no existe en la red.")
            return False
        if destino not in self.adyacencia[origen]:
            print(f"Error: no hay conexión entre '{origen}' y '{destino}'.")
            return False

        del self.adyacencia[origen][destino]
        del self.adyacencia[destino][origen]  # quitar también la vuelta
        self.funcion_log(f"Conexión eliminada: {origen} <-> {destino}")
        return True

    # ---------------- Utilidades ----------------
    def obtener_servidores(self):
        """Devuelve la lista de nombres de todos los vértices del grafo."""
        return list(self.adyacencia.keys())

    def mostrar_red(self):
        """Imprime la topología completa: cada servidor y sus conexiones."""
        print(f"\n--- Red actual ({len(self.adyacencia)} servidores) ---")
        if not self.adyacencia:
            print("(red vacía: no hay servidores registrados)")
            return
        for servidor in self.adyacencia:
            vecinos = self.adyacencia[servidor]
            if vecinos:
                enlaces = ", ".join(
                    f"{vecino} ({latencia} ms)" for vecino, latencia in vecinos.items()
                )
                print(f"{servidor} -> {enlaces}")
            else:
                print(f"{servidor} -> (sin conexiones)")

    # ---------------- Diagnóstico: Ping General (BFS) ----------------
    def ping_general(self, servidor_inicio=None):
        """Recorre el grafo con BFS y reporta si hay servidores aislados.

        BFS (búsqueda en anchura): se parte de un servidor 'inicio' y se
        recorre el grafo por niveles usando una cola FIFO: se visita el
        servidor actual, se encolan todos sus vecinos no visitados y se
        repite. Al terminar, los vértices alcanzados son todos los que están
        comunicados con el inicio; cualquier servidor que NO fue visitado
        está "aislado" (sin camino que lo conecte con el resto).

        Args:
            servidor_inicio: Vértice desde el que se lanza el ping. Si no
                se indica, se usa el primer servidor registrado.

        Returns:
            Lista con los nombres de los servidores aislados (vacía si la
            red está completamente comunicada), o None si la red está vacía
            o el inicio no existe.
        """
        if not self.adyacencia:
            print("La red está vacía: no hay servidores que revisar.")
            return None

        inicio = servidor_inicio if servidor_inicio else self.obtener_servidores()[0]
        if inicio not in self.adyacencia:
            print(f"Error: el servidor '{inicio}' no existe en la red.")
            return None

        # BFS: cola FIFO -> primero se visita todo lo más cercano (en "anchura")
        visitados = set()
        cola = [inicio]
        while cola:
            actual = cola.pop(0)
            if actual in visitados:
                continue
            visitados.add(actual)
            for vecino in self.adyacencia[actual]:
                if vecino not in visitados:
                    cola.append(vecino)

        aislados = [s for s in self.adyacencia if s not in visitados]

        print(f"\n--- Ping General (BFS desde '{inicio}') ---")
        print(f"Alcanzables: {len(visitados)}/{len(self.adyacencia)} servidores")
        if aislados:
            print("ATENCIÓN - SERVIDORES AISLADOS:", ", ".join(aislados))
        else:
            print("Todos los servidores están comunicados. Red sin aislamientos.")

        self.funcion_log(
            f"Ping General desde {inicio}: {len(visitados)}/{len(self.adyacencia)} alcanzables"
            + (f" | Aislados: {', '.join(aislados)}" if aislados else " | Red completa")
        )
        return aislados

    # ---------------- Enrutamiento: Camino más corto (Dijkstra) ----------------
    def dijkstra(self, origen, destino):
        """Calcula la ruta óptima (menor latencia total) entre dos servidores.

        Algoritmo de Dijkstra:
            1. Todas las distancias inician en infinito, excepto la del
               origen, que vale 0.
            2. Se toma siempre el vértice NO visitado con menor distancia
               acumulada y se "relaja" cada una de sus aristas: si ir al
               vecino pasando por ese vértice es más barato que lo conocido
               hasta ahora, se actualiza la distancia y se anota por dónde
               se llegó (para reconstruir el camino al final).
            3. Se repite hasta visitar el destino o agotar los alcanzables.
            Se usa una cola simple en vez de heap para mantener el código
            didáctico; para la escala de la simulación es suficiente.

        Imprime la ruta salto por salto y el costo total acumulado, y
        reporta también el caso en que no existe ninguna ruta (servidores
        en componentes desconectadas).

        Returns:
            Tupla (camino, costo_total) donde camino es la lista de
            servidores desde el origen hasta el destino, o (None, None) si
            no existe ruta o algún servidor no existe.
        """
        if origen not in self.adyacencia:
            print(f"Error: el servidor origen '{origen}' no existe en la red.")
            return None, None
        if destino not in self.adyacencia:
            print(f"Error: el servidor destino '{destino}' no existe en la red.")
            return None, None

        # Paso 1: distancias en infinito, origen en 0, nadie visitado
        infinito = float("inf")
        distancias = {servidor: infinito for servidor in self.adyacencia}
        distancias[origen] = 0
        previos = {servidor: None for servidor in self.adyacencia}
        visitados = set()

        # Paso 2 y 3: extraer el no visitado más cercano y relajar aristas
        while True:
            actual = None
            menor = infinito
            for servidor in self.adyacencia:
                if servidor not in visitados and distancias[servidor] < menor:
                    menor = distancias[servidor]
                    actual = servidor

            if actual is None or actual == destino:
                break  # no quedan alcanzables, o ya llegamos al destino

            visitados.add(actual)
            for vecino, peso in self.adyacencia[actual].items():
                nueva_distancia = distancias[actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    previos[vecino] = actual

        # Si el destino sigue en infinito, está en otra componente del grafo
        if distancias[destino] == infinito:
            print(f"No existe ruta de '{origen}' a '{destino}' (red desconectada).")
            self.funcion_log(
                f"Cálculo de ruta FALLIDO (sin ruta): {origen} -> {destino}"
            )
            return None, None

        # Reconstruir el camino hacia atrás usando los previos
        camino = []
        nodo = destino
        while nodo is not None:
            camino.insert(0, nodo)
            nodo = previos[nodo]

        costo_total = distancias[destino]

        # Imprimir salto por salto con el costo de cada arista y el acumulado
        print(f"\nRuta óptima de '{origen}' a '{destino}':")
        acumulado = 0
        for i in range(len(camino)):
            if i == 0:
                print(f"  Salida: {camino[i]}")
            else:
                tramo = self.adyacencia[camino[i - 1]][camino[i]]
                acumulado += tramo
                print(f"  Salto {i}: {camino[i - 1]} -> {camino[i]} "
                      f"({tramo} ms) | Acumulado: {acumulado} ms")
        print(f"  Costo total: {costo_total} ms")

        self.funcion_log(
            f"Cálculo de ruta: {origen} -> {destino} | "
            f"Saltos: {' -> '.join(camino)} | Costo total: {costo_total} ms"
        )
        return camino, costo_total

    # ---------------- Logger local (solo para pruebas aisladas) ----------------
    def _log_local(self, detalle):
        from datetime import datetime
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG local] {marca} - {detalle}")
        # En la integración final, Daniel reemplaza este
        # callback por su función real que hace append a
        # network_audit_log.txt con fecha, hora y detalle.
