"""Módulo 4 - Auditoría: log central en network_audit_log.txt."""

import os
from datetime import datetime

ARCHIVO_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "network_audit_log.txt")


def registrar_log(detalle, archivo=None):
    """Hace append de 'AAAA-MM-DD | HH:MM:SS | detalle' al log de auditoría."""
    ahora = datetime.now()
    linea = f"{ahora:%Y-%m-%d} | {ahora:%H:%M:%S} | {detalle}\n"
    with open(archivo or ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(linea)


def consulta_en_vivo(archivo=None):
    """Lee el log completo y lo vuelca en pantalla."""
    try:
        with open(archivo or ARCHIVO_LOG, encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        contenido = ""
    print("\n--- network_audit_log.txt ---")
    print(contenido if contenido else "(el log está vacío)")
