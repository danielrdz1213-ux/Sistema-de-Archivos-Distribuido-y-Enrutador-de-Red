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

from NodoUsuario import NodoUsuario


class TablaHash:
    def __init__(self, capacidad=16, funcion_log=None):
        """
        capacidad: tamaño inicial del arreglo interno (buckets).
        funcion_log: callback que el Módulo 4 (Persona D) inyectará para
                     escribir en network_audit_log.txt. Si no se pasa
                     (modo standalone/pruebas), se usa un logger local
                     silencioso.
        """
        # Validación: la capacidad debe ser un entero positivo (se excluye
        # bool porque en Python bool es subclase de int).
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise ValueError("'capacidad' debe ser un entero positivo.")

        self.capacidad = capacidad
        self.tabla = [None] * self.capacidad   # arreglo interno de buckets
        # Contador de usuarios registrados (se usa para el factor de carga).
        self.cantidad = 0
        # Si llegó callback de auditoría se usa; si no, el logger silencioso.
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
        # Semilla inicial del algoritmo djb2 (5381 es su número característico).
        h = 5381
        # Cada carácter desplaza el acumulador y suma su valor Unicode.
        for caracter in usuario:
            h = (h * 33 + ord(caracter)) & 0xFFFFFFFF  # evita overflow
        # Se reduce al rango válido de índices: 0 .. capacidad-1.
        return h % self.capacidad

    # ---------------- Registrar usuario ----------------
    def registrar_usuario(self, usuario, contrasena):
        # 1) Índice del arreglo donde "vive" este usuario (según su hash).
        indice = self._hash(usuario)

        # 2) Recorrer la cadena de ese índice buscando un usuario duplicado.
        actual = self.tabla[indice]
        while actual:
            if actual.usuario == usuario:
                self.funcion_log(f"Registro FALLIDO (usuario ya existe): {usuario}")
                return False
            actual = actual.siguiente  # avanzar al siguiente nodo de la cadena

        # 3) No existía: se crea el nodo y se enlaza al inicio (costo O(1)).
        nuevo = NodoUsuario(usuario, contrasena)
        nuevo.siguiente = self.tabla[indice]  # inserta al inicio de la lista
        self.tabla[indice] = nuevo
        self.cantidad += 1  # la tabla ahora tiene un usuario más

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
        # Localizar la cadena donde debería estar el usuario.
        indice = self._hash(usuario)
        # Recorrer la cadena nodo por nodo comparando credenciales.
        actual = self.tabla[indice]
        while actual:
            if actual.usuario == usuario:  # coincidió el nombre de usuario
                if actual.contrasena == contrasena:  # contraseña correcta
                    self.funcion_log(f"Login EXITOSO: {usuario}")
                    return True
                else:
                    self.funcion_log(f"Login FALLIDO (contraseña incorrecta): {usuario}")
                    return False
            actual = actual.siguiente  # probar con el siguiente de la cadena

        # Se agotó la cadena sin coincidencias: el usuario no está registrado.
        self.funcion_log(f"Login FALLIDO (usuario no existe): {usuario}")
        return False

    # ---------------- Eliminar usuario ----------------
    def eliminar_usuario(self, usuario):
        """
        Elimina un usuario de la tabla hash (encadenamiento).

        Recorre únicamente la cadena que le corresponde al índice calculado
        con _hash(usuario), desenlaza el nodo encontrado (ya sea la cabeza
        de la lista o un nodo intermedio) y descuenta el contador de
        usuarios. No deja "tumbas" (tombstones): el nodo se saca por
        completo de la cadena, que es una ventaja del encadenamiento.

        Retorna True si se eliminó; False si el usuario no existía.
        Cada intento (éxito o fallo) queda registrado vía self.funcion_log,
        igual que registrar_usuario y validar_login.
        """
        # 1) Índice del arreglo donde vive la cadena de este usuario.
        indice = self._hash(usuario)

        # 2) Recorrer la cadena guardando el nodo anterior (para desenlazar).
        anterior = None
        actual = self.tabla[indice]
        while actual:
            if actual.usuario == usuario:  # coincidió el nombre de usuario
                if anterior is None:
                    # El nodo a eliminar era el primero de la cadena:
                    # la cabeza pasa a ser su siguiente.
                    self.tabla[indice] = actual.siguiente
                else:
                    # Nodo intermedio o final: se "salta" enlazando al siguiente.
                    anterior.siguiente = actual.siguiente
                self.cantidad -= 1  # la tabla ahora tiene un usuario menos
                self.funcion_log(f"Usuario ELIMINADO: {usuario}")
                return True
            anterior = actual  # antes de avanzar, recordar el nodo previo
            actual = actual.siguiente  # probar con el siguiente de la cadena

        # Se agotó la cadena sin coincidencias: el usuario no estaba registrado.
        self.funcion_log(f"Eliminación FALLIDA (usuario no existe): {usuario}")
        return False

    # ---------------- Redimensionar (rehashing) ----------------
    def _redimensionar(self):
        """Duplica la capacidad y reinserta todo cuando el factor de carga > 0.75."""
        # 1) Guardar la tabla original para releerla después.
        vieja_tabla = self.tabla
        # 2) Duplicar la capacidad y crear la tabla nueva vacía.
        self.capacidad *= 2
        self.tabla = [None] * self.capacidad
        # 3) El contador se reinicia; lo vuelve a subir cada reinserción.
        self.cantidad = 0

        # 4) Reinsertar cada usuario de la tabla vieja en la nueva (rehash).
        for bucket in vieja_tabla:
            # Se recorre cada cadena de la tabla anterior nodo por nodo.
            actual = bucket
            while actual:
                self._insertar_sin_log(actual.usuario, actual.contrasena)
                actual = actual.siguiente

    def _insertar_sin_log(self, usuario, contrasena):
        """Igual que registrar_usuario pero sin loggear (uso interno del rehash)."""
        # Índice calculado contra la capacidad NUEVA (ya duplicada).
        indice = self._hash(usuario)
        # Inserción al inicio de la cadena, idéntica a registrar_usuario,
        # pero sin emitir ningún registro de auditoría.
        nuevo = NodoUsuario(usuario, contrasena)
        nuevo.siguiente = self.tabla[indice]
        self.tabla[indice] = nuevo
        self.cantidad += 1  # el rehash también debe contar a todos

    # ---------------- Mostrar tabla (debug / defensa) ----------------
    def mostrar_tabla(self):
        # Encabezado con las métricas actuales de la tabla.
        print(f"\n--- Tabla Hash (capacidad={self.capacidad}, usuarios={self.cantidad}) ---")
        # Recorrer cada índice del arreglo mostrando lo que contiene su cadena.
        for i, bucket in enumerate(self.tabla):
            # Se acumulan los nombres de la cadena en una lista auxiliar.
            contenido = []
            actual = bucket
            while actual:
                contenido.append(actual.usuario)  # tomar el nombre del nodo
                actual = actual.siguiente  # avanzar dentro de la cadena
            # Índice -> lista de usuarios, o "vacío" si la cadena no tiene nodos.
            print(f"[{i}] -> {contenido if contenido else 'vacío'}")

   # ---------------- Logger local (solo para pruebas aisladas) ----------------
    def _log_local(self, detalle):
        """Logger silencioso para ejecuciones aisladas sin callback."""
        return None