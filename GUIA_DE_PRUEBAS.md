# Guía de pruebas - Sistema de Archivos Distribuido y Enrutador de Red

Esta guía explica cómo verificar que todo el sistema funciona: primero con las
pruebas automáticas y después con un recorrido manual por cada menú.

## Requisitos

- Python 3.x instalado (`python --version`).
- Ejecutar todos los comandos desde la **raíz del proyecto** (la carpeta que
  contiene `main.py`).
- Sistema operativo Windows (el programa usa `cls` y `msvcrt` para ocultar la
  contraseña; en otros SO la limpieza de pantalla y los asteriscos no funcionan).

---

## 1. Prueba automática (la más rápida)

```bash
python test_integracion.py
```

**Resultado esperado:** `Ran 25 tests ... OK` (en rojo diría `FAILED` si algo falla).

Lo que cubre:

| Grupo | Qué verifica |
|---|---|
| `TestSistemaArchivos` (M1) | Crear/buscar/listar/eliminar el árbol y sus errores (ruta inexistente, nombre duplicado, borrar la raíz). |
| `TestTablaHash` (M2) | Registro, login OK/fallido, colisiones, **rehash** al superar 0.75 de carga y capacidad inválida. |
| `TestGrafo` (M3) | Servidores/conexiones válidos e inválidos, **Dijkstra** (ruta óptima, sin ruta), **Ping BFS** (detecta aislados) y bajas sin aristas huérfanas. |
| `TestAuditoria` (M4) | Formato `fecha | hora | detalle` del log, append sin pisar y consulta en vivo. |
| `TestFlujoCompleto` | Recorre **todos** los menús de `main.py` simulando el teclado: registro → login fallido → login OK → directorios → red → log → cerrar sesión → salir; y verifica los eventos de auditoría. |

Notas:
- Esta prueba **no escribe** en `network_audit_log.txt` (la auditoría se simula en memoria).
- La contraseña con asteriscos (`_leer_contrasena`) lee el teclado directo con
  `msvcrt`, por eso se prueba manualmente (paso 2).

---

## 2. Prueba manual paso a paso

```bash
python main.py
```

### 2.1 Pantalla de ACCESO

| # | Teclea | Resultado esperado |
|---|---|---|
| 1 | `9` | `>> Opción inválida.` y pausa. |
| 2 | `1` → servidor `NoExiste` | `>> Ese servidor no existe. Créelo primero con la opción 3.` |
| 3 | `3` → servidor `Server1` | `>> Servidor 'Server1' creado con árbol y tabla de credenciales propios.` |
| 4 | `3` → `Server1` otra vez | `Error: el servidor 'Server1' ya existe en la red.` (no duplica). |
| 5 | `2` → `Server1` → usuario `mariano` → clave `secreto123` | `>> Registrado.` (**la clave se ve al registrar, es intencional**). |
| 6 | Repite el paso 5 | `>> Ese usuario ya existe.` |
| 7 | `1` → `Server1` → `mariano` → clave `mala` | **Cada carácter se dibuja como `*`** y borra con Retroceso; luego `>> Acceso denegado.` |
| 8 | `1` → `Server1` → usuario vacío → clave `x` | `>> Usuario y contraseña no pueden estar vacíos.` |
| 9 | `1` → `Server1` → `mariano` → `secreto123` | `>> Bienvenido, mariano.` → entra al **MENÚ PRINCIPAL**. |

### 2.2 Menú principal → 1) Directorios

| # | Teclea | Resultado esperado |
|---|---|---|
| 1 | `1` → `1` → `Server1` → `/` → `Documentos` → `1` (Carpeta) | `>> Creado.` |
| 2 | `1` → `1` → `Server1` → `/Documentos` → `nota.txt` → `2` (Archivo) | `>> Creado.` |
| 3 | `1` → `1` → `Server1` → `/Documentos` → `nota.txt` → `1` | `>> Error: Ya existe un nodo llamado 'nota.txt'...` |
| 4 | `2` → `Server1` → `nota.txt` | `Encontrado: /Documentos/nota.txt` |
| 5 | `3` → `Server1` | Árbol indentado: `- /`, `- Documentos/`, `- nota.txt` |
| 6 | `4` → `Server1` → `/NoExiste` | `>> Error: La ruta '/NoExiste' no existe.` |
| 7 | `4` → `Server1` → `/Documentos` | `>> Eliminado.` (borra en cascada carpeta + archivo) |
| 8 | `3` → `Server1` | Solo queda `- /` |
| 9 | `1` → `2` (servidor que no existe) | `>> El servidor no existe en la red.` |
| 10 | `5` | Regresa al menú principal. |

### 2.3 Menú principal → 2) Red

| # | Teclea | Resultado esperado |
|---|---|---|
| 1 | `1` → `Server2` | `>> Servidor 'Server2' agregado correctamente.` |
| 2 | `2` → `Server1` → `Server2` → `10` | `>> Conexión 'Server1 <-> Server2' establecida (10.0 ms).` |
| 3 | `2` → `Server1` → `Server2` → `abc` | `>> Latencia inválida.` |
| 4 | `2` → `Server1` → `Server1` → `5` | `Error: no se puede conectar un servidor consigo mismo.` |
| 5 | `5` → `Server1` → `Server2` | `Ruta óptima de 'Server1' a 'Server2'` con `Costo total: 10.0 ms` (se guarda como `float`). |
| 6 | `6` → Enter (automático) | `Alcanzables: 2/2 servidores` y `Todos los servidores están comunicados.` |
| 7 | Agrega `Server3` (`1`) y repite `6` | `ATENCIÓN - SERVIDORES AISLADOS: Server3` (BFS lo detecta). |
| 8 | `5` → `Server1` → `Server3` | `No existe ruta de 'Server1' a 'Server3' (red desconectada).` |
| 9 | `7` | Topología completa: `Server1 -> Server2 (10.0 ms)`, etc. |
| 10 | `3` → `Server1` → `Server2` | `>> Conexión 'Server1 <-> Server2' eliminada correctamente.` (en ambas direcciones). |
| 11 | `4` → `Server3` | `>> Servidor 'Server3' eliminado correctamente.` (junto con sus enlaces). |
| 12 | `8` | Regresa al menú principal. |

### 2.4 Menú principal → 3) y 4)

| # | Teclea | Resultado esperado |
|---|---|---|
| 1 | `3` | Vuelca todo `network_audit_log.txt` en pantalla. |
| 2 | `4` | `>> Sesión cerrada.` → vuelve a la pantalla de ACCESO. |
| 3 | `1` y entra de nuevo con `mariano`/`secreto123` | Login sigue funcionando (la tabla vive en memoria de la sesión). |
| 4 | `4` | Cierra el programa. |

---

## 3. Verificar el log de auditoría (M4)

Al terminar la prueba manual, revisa `network_audit_log.txt`. Cada línea debe
tener el formato `AAAA-MM-DD | HH:MM:SS | detalle` y aparecerán eventos como:

```
Servidor agregado a la red: Server1
[Servidor Server1] Usuario registrado exitosamente: mariano
[Servidor Server1] Login EXITOSO: mariano
[Árbol] mariano creó Carpeta 'Documentos' en '/' del servidor 'Server1'
Conexión establecida: Server1 <-> Server2 (10.0 ms)
Cálculo de ruta: Server1 -> Server2 | Saltos: Server1 -> Server2 | Costo total: 10.0 ms
Ping General desde Server1: 2/2 alcanzables | Red completa
[Sesión] Mariano cerró sesión
```

También puedes verlo en vivo desde el menú principal, opción `3`.

---

## 4. Prueba extra: rehash de la tabla con 40 usuarios

La bitácora menciona esta prueba. Opción rápida sin pasar por los menús:

```bash
python -c "from TablaHash import TablaHash; t = TablaHash(); [t.registrar_usuario(f'u{i}', f'p{i}') for i in range(40)]; print('capacidad:', t.capacidad, '| usuarios:', t.cantidad); print('login u39:', t.validar_login('u39', 'p39'))"
```

**Resultado esperado:** capacidad `64` (duplicó 16 → 32 → 64 según el factor de
carga 0.75), `usuarios: 40` y `login u39: True` (nadie se perdió en el rehash).

---

## 5. Si algo falla

| Síntoma | Causa probable |
|---|---|
| `ModuleNotFoundError` | No estás en la raíz del proyecto; entra a la carpeta con `main.py`. |
| `python` no se reconoce | Instala Python 3 o usa `py main.py`. |
| La pantalla no se limpia | Es Windows-only (`os.system("cls")`); no afecta el resultado. |
| Los asteriscos no aparecen al escribir la clave | Estás en una terminal que no es la consola estándar de Windows (`msvcrt` no lee teclas ahí). Usa una CMD o PowerShell normal. |
| `test_recorrido_completo` falla | El orden de los `input()` de `main.py` cambió; ajusta la lista `respuestas` en `test_integracion.py` al nuevo orden de prompts. |


