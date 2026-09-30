"""Prueba de punta a punta: python test_integracion.py"""
import os, tempfile
import auditoria
from Grafo import Grafo
from TablaHash import TablaHash

auditoria.ARCHIVO_LOG = os.path.join(tempfile.mkdtemp(), "log.txt")
log = auditoria.registrar_log
t = TablaHash(funcion_log=log); g = Grafo(funcion_log=log)
t.registrar_usuario("ana", "1"); t.validar_login("ana", "1"); t.validar_login("ana", "x")
g.agregar_servidor("A"); g.agregar_servidor("B"); g.agregar_conexion("A", "B", 5); g.dijkstra("A", "B")
texto = open(auditoria.ARCHIVO_LOG, encoding="utf-8").read()
for esperado in ("Login EXITOSO", "Login FALLIDO", "Cálculo de ruta"):
    assert esperado in texto, esperado
assert all(l.count(" | ") >= 2 for l in texto.splitlines())
print("OK:", len(texto.splitlines()), "líneas de auditoría")
