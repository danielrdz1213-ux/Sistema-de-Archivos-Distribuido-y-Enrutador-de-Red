"""Módulo 4 - Auditoría: log central en network_audit_log.txt."""

import os
from datetime import datetime

# Ruta absoluta del archivo de log: se calcula junto a este .py para que
# funcione aunque el programa se ejecute desde otro directorio de trabajo.
ARCHIVO_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "network_audit_log.txt")


def registrar_log(detalle, archivo=None):
    """Hace append de 'AAAA-MM-DD | HH:MM:SS | detalle' al log de auditoría."""
    # 1) Momento exacto del evento (fecha y hora del sistema).
    ahora = datetime.now()
    # 2) Línea con el formato: AAAA-MM-DD | HH:MM:SS | detalle del evento.
    linea = f"{ahora:%Y-%m-%d} | {ahora:%H:%M:%S} | {detalle}\n"
    # 3) Modo "a" (append): se agrega al final sin borrar lo ya registrado.
    with open(archivo or ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(linea)  # se escribe la línea completa (incluye salto de línea)


def consulta_en_vivo(archivo=None):
    """Lee el log completo y lo vuelca en pantalla."""
    try:
        # Se intenta leer el archivo completo del log...
        with open(archivo or ARCHIVO_LOG, encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        # ...si aún no existe (nunca se registró nada), se usa vacío.
        contenido = ""
    # Encabezado que identifica la consulta en vivo.
    print("\n--- network_audit_log.txt ---")
    # Se vuelca todo el contenido o un mensaje si está vacío.
    print(contenido if contenido else "(el log está vacío)")
