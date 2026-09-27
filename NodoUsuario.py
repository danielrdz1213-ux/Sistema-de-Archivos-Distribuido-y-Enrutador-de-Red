"""
Nodo para la lista enlazada de cada índice de la Tabla Hash.
Cada índice del arreglo interno guarda una cadena de estos nodos
(manejo de colisiones por encadenamiento).
"""

#definición inicial del nodo usuario
class NodoUsuario: #los dos puntos son para indicar que el siguiente tab pertenece a esta clase
    def __init__(self, usuario, contrasena): #el self se hace siempre al incio de la creación de clase en el constructor
        self.usuario = usuario
        self.contrasena = contrasena
        self.siguiente = None