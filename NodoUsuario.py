"""
Nodo para la lista enlazada de cada índice de la Tabla Hash.
Cada índice del arreglo interno guarda una cadena de estos nodos
(manejo de colisiones por encadenamiento).
"""

class NodoUsuario:
    def __init__(self, usuario, contrasena):
        self.usuario = usuario
        self.contrasena = contrasena
        self.siguiente = None
