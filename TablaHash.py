"""
Módulo 2 - Autenticación y Caché (Tabla Hash)
Proyecto: Sistema de Archivos Distribuido y Enrutador de Red
EIF207 Estructuras de Datos - UNA

Implementa una Tabla Hash construida desde cero (sin dict/HashMap nativo)
para registrar usuarios y validar logins en tiempo O(1) promedio.

Manejo de colisiones: ENCADENAMIENTO (listas simples en cada índice).
Se eligió encadenamiento porque:
  - Es más simple de implementar y depurar que direccionamiento abierto.
  - No sufre "clustering" (agrupamiento) cuando el factor de carga crece.
  - Permite eliminar usuarios sin dejar "tumbas" (tombstones) como sí
    pasa con direccionamiento abierto.
"""

from datetime import datetime

from NodoUsuario import NodoUsuario


class TablaHash:
    def __init__(self, capacidad=16, funcion_log=None):
        """
        capacidad: tamaño inicial del arreglo interno (buckets).
        funcion_log: callback que el Módulo 4 (Persona D) inyectará para
                     escribir en network_audit_log.txt. Si no se pasa
                     (modo standalone/pruebas), se usa un logger local
                     que solo imprime en consola.
        """
        self.capacidad = capacidad
        self.tabla = [None] * self.capacidad   # arreglo interno de buckets
        self.cantidad = 0
        self.funcion_log = funcion_log or self._log_local

    # ---------------- Función hash propia ----------------
    def _hash(self, usuario):
        """
        Función de dispersión polinomial (estilo djb2).
        Recorre cada carácter del string y acumula:
            h = h * 33 + ord(char)
        y al final se reduce con módulo a la capacidad de la tabla.
        Distribuye bien strings cortos (nombres de usuario) y evita que
        strings parecidos caigan siempre en el mismo índice.
        """
        h = 5381
        for caracter in usuario:
            h = (h * 33 + ord(caracter)) & 0xFFFFFFFF  # evita overflow
        return h % self.capacidad

    # ---------------- Registrar usuario ----------------
    def registrar_usuario(self, usuario, contrasena):
        indice = self._hash(usuario)

        actual = self.tabla[indice]
        while actual:
            if actual.usuario == usuario:
                self.funcion_log(f"Registro FALLIDO (usuario ya existe): {usuario}")
                return False
            actual = actual.siguiente

        nuevo = NodoUsuario(usuario, contrasena)
        nuevo.siguiente = self.tabla[indice]  # inserta al inicio de la lista
        self.tabla[indice] = nuevo
        self.cantidad += 1

        # Si el factor de carga crece demasiado, se redimensiona la tabla
        if self.cantidad / self.capacidad > 0.75:
            self._redimensionar()

        self.funcion_log(f"Usuario registrado exitosamente: {usuario}")
        return True

    # ---------------- Validar login ----------------
    def validar_login(self, usuario, contrasena):
        """
        Retorna True/False. Cada intento (éxito o fallo) se conecta con
        el registro de auditoría del Módulo 4 vía self.funcion_log,
        tal como pide el enunciado.
        """
        indice = self._hash(usuario)
        actual = self.tabla[indice]
        while actual:
            if actual.usuario == usuario:
                if actual.contrasena == contrasena:
                    self.funcion_log(f"Login EXITOSO: {usuario}")
                    return True
                else:
                    self.funcion_log(f"Login FALLIDO (contraseña incorrecta): {usuario}")
                    return False
            actual = actual.siguiente

        self.funcion_log(f"Login FALLIDO (usuario no existe): {usuario}")
        return False

    # ---------------- Redimensionar (rehashing) ----------------
    def _redimensionar(self):
        """Duplica la capacidad y reinserta todo cuando el factor de carga > 0.75."""
        vieja_tabla = self.tabla
        self.capacidad *= 2
        self.tabla = [None] * self.capacidad
        self.cantidad = 0

        for bucket in vieja_tabla:
            actual = bucket
            while actual:
                self._insertar_sin_log(actual.usuario, actual.contrasena)
                actual = actual.siguiente

    def _insertar_sin_log(self, usuario, contrasena):
        """Igual que registrar_usuario pero sin loggear (uso interno del rehash)."""
        indice = self._hash(usuario)
        nuevo = NodoUsuario(usuario, contrasena)
        nuevo.siguiente = self.tabla[indice]
        self.tabla[indice] = nuevo
        self.cantidad += 1

    # ---------------- Mostrar tabla (debug / defensa) ----------------
    def mostrar_tabla(self):
        print(f"\n--- Tabla Hash (capacidad={self.capacidad}, usuarios={self.cantidad}) ---")
        for i, bucket in enumerate(self.tabla):
            contenido = []
            actual = bucket
            while actual:
                contenido.append(actual.usuario)
                actual = actual.siguiente
            print(f"[{i}] -> {contenido if contenido else 'vacío'}")

    # ---------------- Logger local (solo para pruebas aisladas) ----------------
    def _log_local(self, detalle):
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG local] {marca} - {detalle}")
        # En la integración final, Persona D (Módulo 4) reemplaza este
        # callback por su función real que hace append a
        # network_audit_log.txt con fecha, hora y detalle.