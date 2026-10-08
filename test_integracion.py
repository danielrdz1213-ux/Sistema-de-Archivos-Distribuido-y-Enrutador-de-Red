"""Pruebas de integración y regresión: python test_integracion.py"""
import os
import tempfile
import gc
import weakref
from unittest.mock import patch
import auditoria
from Grafo import Grafo
from TablaHash import TablaHash
from main import login
from sistema_archivos import FileSystem
from sistema_archivos.nodo import Nodo

auditoria.ARCHIVO_LOG = os.path.join(tempfile.mkdtemp(), "log.txt")
log = auditoria.registrar_log
t = TablaHash(funcion_log=log); g = Grafo(funcion_log=log)
t.registrar_usuario("ana", "1"); t.validar_login("ana", "1"); t.validar_login("ana", "x")
g.agregar_servidor("A"); g.agregar_servidor("B"); g.agregar_conexion("A", "B", 5); g.dijkstra("A", "B")
texto = open(auditoria.ARCHIVO_LOG, encoding="utf-8").read()
for esperado in ("Login EXITOSO", "Login FALLIDO", "Cálculo de ruta"):
    assert esperado in texto, esperado
assert all(l.count(" | ") >= 2 for l in texto.splitlines())

# Árbol: creación, búsqueda, eliminación en cascada e integridad de enlaces.
fs = FileSystem()
carpeta = fs.crear_nodo("/", "docs", "Carpeta")
fs.crear_nodo("/docs", "sub", "Carpeta")
fs.crear_nodo("/docs/sub", "nota.txt", "Archivo")
assert fs.buscar_nodo("nota.txt") == "/docs/sub/nota.txt"
assert fs.buscar_nodo("no-existe") is None
referencia_archivo = weakref.ref(fs.raiz.hijos[0].hijos[0].hijos[0])
fs.eliminar_nodo("/docs")
assert fs.buscar_nodo("nota.txt") is None
assert carpeta.padre is None and carpeta.hijos == []
gc.collect()
assert referencia_archivo() is None

# Nodo: no se permiten autoenlaces, ciclos ni reparentación silenciosa.
raiz = Nodo("Carpeta", "raiz")
hijo = Nodo("Carpeta", "hijo")
raiz.agregar_hijo(hijo)
for padre, nuevo_hijo in ((hijo, hijo), (hijo, raiz), (Nodo("Carpeta", "otro"), hijo)):
    try:
        padre.agregar_hijo(nuevo_hijo)
    except ValueError:
        pass
    else:
        raise AssertionError("Se aceptó un enlace inconsistente en el árbol")

# Hash: colisión, cadenas múltiples y rehash.
tabla = TablaHash(capacidad=4, funcion_log=lambda detalle: None)
for capacidad_invalida in (0, -1, 1.5, True):
    try:
        TablaHash(capacidad=capacidad_invalida)
    except ValueError:
        pass
    else:
        raise AssertionError("Se aceptó una capacidad hash inválida")
colision = {}
for nombre in ("u1", "u2", "u3", "u4", "u5", "u6", "u7", "u8"):
    indice = tabla._hash(nombre)
    if indice in colision:
        nombres_colision = (colision[indice], nombre)
        break
    colision[indice] = nombre
else:
    raise AssertionError("No se encontró colisión para la prueba")
for i, nombre in enumerate(nombres_colision):
    assert tabla.registrar_usuario(nombre, f"clave{i}")
    assert tabla.validar_login(nombre, f"clave{i}")
assert not tabla.validar_login(nombres_colision[0], "incorrecta")
for i in range(10):
    tabla.registrar_usuario(f"extra{i}", "p")
assert tabla.capacidad > 4
for i, nombre in enumerate(nombres_colision):
    assert tabla.validar_login(nombre, f"clave{i}")

# Grafo: asociación de árbol por servidor, ruta, desconexión y borrado.
assert g.obtener_sistema_archivos("A") is not None
assert g.obtener_sistema_archivos("A") is not g.obtener_sistema_archivos("B")
assert g.obtener_sistema_archivos("A").raiz.nombre == "/"
assert g.obtener_tabla_credenciales("A") is not None
assert g.obtener_tabla_credenciales("A") is not g.obtener_tabla_credenciales("B")
credenciales_a = g.obtener_tabla_credenciales("A")
credenciales_b = g.obtener_tabla_credenciales("B")
referencia_tabla_b = weakref.ref(credenciales_b)
assert credenciales_a.registrar_usuario("local", "clave")
assert credenciales_a.validar_login("local", "clave")
assert not credenciales_b.validar_login("local", "clave")
with patch("builtins.input", side_effect=("3", "Inicio", "2", "Inicio", "ana", "pw",
                                            "1", "Inicio", "ana", "pw")):
    assert login(Grafo(funcion_log=lambda detalle: None)) == "ana"
assert not g.agregar_conexion("A", "B", float("nan"))
g.agregar_servidor("C")
assert g.ping_general("A") == ["C"]
camino_sin_ruta, costo_sin_ruta = g.dijkstra("A", "C")
assert camino_sin_ruta == [] and costo_sin_ruta == float("inf")
assert g.eliminar_conexion("A", "B")
assert not g.eliminar_conexion("A", "B")
assert g.eliminar_servidor("B")
assert g.obtener_sistema_archivos("B") is None
assert g.obtener_tabla_credenciales("B") is None
del credenciales_b
gc.collect()
assert referencia_tabla_b() is None

# BFS termina al recorrer ciclos y reporta solo los vértices no alcanzables.
ciclico = Grafo(funcion_log=lambda detalle: None)
for nombre in ("X", "Y", "Z", "W"):
    ciclico.agregar_servidor(nombre)
ciclico.agregar_conexion("X", "Y", 1)
ciclico.agregar_conexion("Y", "Z", 1)
ciclico.agregar_conexion("Z", "X", 1)
assert ciclico.ping_general("X") == ["W"]

# Auditoría: append conserva el registro previo.
auditoria.registrar_log("segundo evento")
texto = open(auditoria.ARCHIVO_LOG, encoding="utf-8").read()
assert "Login EXITOSO" in texto and "segundo evento" in texto
print("OK:", len(texto.splitlines()), "líneas de auditoría")
