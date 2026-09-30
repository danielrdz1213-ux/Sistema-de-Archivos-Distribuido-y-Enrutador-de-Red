# Bitácora - Módulo 4 (Auditoría e integración)

- `auditoria.py`: `registrar_log` (append a `network_audit_log.txt`, formato `fecha | hora | detalle`) y `consulta_en_vivo`.
- `main.py`: login (M2) -> menú principal con Directorios (M1), Red (M3) y Consulta en vivo.
- Enganches: M2 y M3 reciben `funcion_log=registrar_log` (login exitoso/fallido, rutas, conexiones); el árbol se audita desde `main.py` (crear/eliminar) sin modificar el código de M1.
- Revisión de M1-M3: sin cambios necesarios; probados Dijkstra, ping con servidor aislado y rehash de la tabla (40 usuarios).
- Prueba: `python test_integracion.py`.
- Sprints semanales: anotar aquí cada ampliación del profesor y qué módulo tocó.
