"""
Módulo 3 - Topología y Enrutamiento de Red (Grafos)
Proyecto: Sistema de Archivos Distribuido y Enrutador de Red
EIF207 Estructuras de Datos - UNA

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

Este archivo (Paso 1) contiene solo la estructura base: vértices, aristas
y visualización. Dijkstra y el Ping General (BFS) se agregan en pasos
posteriores sobre esta misma clase.
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

    # ---------------- Logger local (solo para pruebas aisladas) ----------------
    def _log_local(self, detalle):
        from datetime import datetime
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG local] {marca} - {detalle}")
        # En la integración final, Persona D (Módulo 4) reemplaza este
        # callback por su función real que hace append a
        # network_audit_log.txt con fecha, hora y detalle.
