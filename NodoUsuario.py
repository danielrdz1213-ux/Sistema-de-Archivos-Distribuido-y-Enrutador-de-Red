"""
Nodo para la lista enlazada de cada índice de la Tabla Hash.
Cada índice del arreglo interno guarda una cadena de estos nodos
(manejo de colisiones por encadenamiento).
"""

class NodoUsuario:
    def __init__(self, usuario, contrasena):
        # Nombre de usuario: es la llave con la que se calcula el hash.
        self.usuario = usuario
        # Contraseña asociada: se compara en el login para validar el acceso.
        self.contrasena = contrasena
        # Enlace al siguiente nodo de la cadena; None = último de la lista.
        self.siguiente = None
