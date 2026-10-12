"""Programa principal: une directorios (M1), autenticación (M2), red (M3) y auditoría (M4)."""

# Módulo 4: funciones de auditoría (escribir y ver el log de la red).
from auditoria import registrar_log, consulta_en_vivo
# Módulo 3: la red de servidores (grafo) que conecta árboles y tablas.
from Grafo import Grafo
# os: permite limpiar la pantalla (cls) entre pantallas de los menús.
import os

try:
    import msvcrt  # Solo disponible en Windows: permite ocultar la contraseña
except ImportError:
    msvcrt = None  # fuera de Windows se usará getpass como respaldo


def _leer_contrasena(prompt="Contraseña: "):
    """Lee una contraseña mostrando un asterisco (*) por cada carácter.

    En Windows usa msvcrt, que captura las teclas sin eco y dibuja un '*'
    por cada carácter, de modo que nadie ve la contraseña mientras se
    escribe. En otras plataformas (sin msvcrt) usa getpass, que oculta la
    entrada por completo como respaldo.
    """
    # Respaldo fuera de Windows: getpass oculta la entrada por completo.
    if msvcrt is None:
        import getpass
        return getpass.getpass(prompt)

    import sys
    # Se imprime el aviso manualmente porque no habrá eco del teclado.
    sys.stdout.write(prompt)
    sys.stdout.flush()

    # Caracteres reales tecleados hasta el momento (se unen al final).
    contrasena = []
    while True:
        tecla = msvcrt.getwch()
        # Las teclas especiales (flechas, F1, etc.) llegan como doble código.
        if tecla in ("\x00", "\xe0"):
            msvcrt.getwch()  # se descarta el resto de la tecla especial
            continue
        if tecla in ("\r", "\n"):  # Enter finaliza la captura
            sys.stdout.write("\n")
            break
        if tecla == "\b":  # Retroceso borra el último asterisco
            if contrasena:
                contrasena.pop()
                sys.stdout.write("\b \b")  # borra el '*' de la pantalla
                sys.stdout.flush()
            continue
        if tecla == "\x03":  # Ctrl+C aborta la captura
            raise KeyboardInterrupt
        contrasena.append(tecla)  # guardar el carácter real en la lista
        sys.stdout.write("*")  # mostrar solo un asterisco en pantalla
        sys.stdout.flush()

    # Se unen todos los caracteres capturados en la cadena final.
    return "".join(contrasena)


def login(grafo):
    """Pantalla de acceso. Devuelve el usuario autenticado o None si sale."""
    while True:
        # Menú de acceso: se repite hasta autenticarse o elegir "Salir".
        print("\n=== ACCESO AL SERVIDOR ===\n1. Iniciar sesión\n2. Registrar usuario\n"
              "3. Agregar servidor\n4. Eliminar usuario\n5. Salir")
        op = input("Elija una opción: ").strip()
        os.system("cls")  # limpiar pantalla tras leer la opción

        # Opción 5: salir del programa (se devuelve None al llamador).
        if op == "5":
            return None
        # Opción 3: crear un servidor nuevo (nace con árbol y tabla propios).
        if op == "3":
            nombre_servidor = input("Nuevo servidor: ").strip()
        
            if grafo.agregar_servidor(nombre_servidor):
                print(f">> Servidor '{nombre_servidor}' creado con árbol y tabla de credenciales propios.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            continue
        # Opción 4: eliminar un usuario de la tabla hash del servidor.
        if op == "4":
            # Se pide el servidor donde está la cuenta a eliminar.
            servidor = input("Servidor: ").strip()
            # Tabla hash de ese servidor; None si el servidor no existe.
            usuarios = grafo.obtener_tabla_credenciales(servidor)
            if usuarios is None:
                print(">> Ese servidor no existe. Créelo primero con la opción 3.")
            else:
                usuario = input("Usuario a eliminar: ").strip()
                if not usuario:
                    print(">> El usuario no puede estar vacío.")
                elif usuarios.eliminar_usuario(usuario):
                    print(">> Usuario eliminado.")
                else:
                    print(">> Ese usuario no existe.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            continue
        # Cualquier otra tecla fuera de 1 y 2 se rechaza.
        if op not in ("1", "2"):
            print("Opción inválida.")
            input("Presiona ENTER para continuar...")
            os.system("cls")

            continue
        # Se pide el servidor donde está (o estará) la cuenta del usuario.
        servidor = input("Servidor: ").strip()
        # Tabla hash de ese servidor; None si el servidor no existe aún.
        usuarios = grafo.obtener_tabla_credenciales(servidor)
        if usuarios is None:
            print(">> Ese servidor no existe. Créelo primero con la opción 3.")
            input("Presiona ENTER para continuar...")
            os.system("cls")

            continue
        usuario = input("Usuario: ").strip()
        # El enmascaramiento (asteriscos) solo aplica al inicio de sesión;
        # al registrar el usuario la contraseña se muestra con normalidad.
        if op == "1":
            contrasena = _leer_contrasena().strip()
        else:
            contrasena = input("Contraseña: ").strip()
        # Ambos campos son obligatorios.
        if not usuario or not contrasena:
            print(">> Usuario y contraseña no pueden estar vacíos.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            continue

        # Rama de REGISTRO: intenta crear la cuenta en la tabla hash.
        elif op == "2":
            print(">> Registrado." if usuarios.registrar_usuario(usuario, contrasena) else ">> Ese usuario ya existe.")
            input("Presiona ENTER para continuar...")
            os.system("cls")

        # Rama de LOGIN: valida credenciales contra la tabla hash.
        elif usuarios.validar_login(usuario, contrasena):
            print(f">> Bienvenido, {usuario}.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            return usuario  # autenticado: se sale del menú de acceso
        # Credenciales incorrectas (el detalle ya quedó en la bitácora).
        else:
            print(">> Acceso denegado.")
            input("Presiona ENTER para continuar...")
            os.system("cls")


def menu_directorios(grafo, usuario):
    """Menú del Módulo 1: crear, buscar, listar y borrar nodos del árbol."""
    while True:
        # Opciones del subsistema de directorios (árbol del servidor).
        print("\n--- DIRECTORIOS ---\n1. Crear\n2. Buscar\n3. Listar árbol\n4. Eliminar\n5. Volver")
        op = input("Elija una opción: ").strip()
        os.system("cls")  # limpiar pantalla tras leer la opción

        # Opción 5: regresar al menú principal (return sale de la función).
        if op == "5":
            print("Regresando al menu anterior...")
            return
        # Solo se aceptan las opciones 1 a 4.
        if op not in ("1", "2", "3", "4"):
            print("Opción inválida.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            continue
        # Se elige sobre qué servidor se trabajará su árbol de archivos.
        servidor = input("Servidor cuyo sistema de archivos desea usar: ").strip()
        # FileSystem del servidor; None si ese servidor no existe en la red.
        fs = grafo.obtener_sistema_archivos(servidor)
        if fs is None:
            print(">> El servidor no existe en la red.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            continue
        # Las operaciones del árbol lanzan ValueError con mensajes claros;
        # aquí se capturan para mostrarlos sin romper el programa.
        try:
            # Opción 1: crear un nodo (carpeta o archivo) dentro de una ruta.
            if op == "1":
                padre = input("Ruta de la carpeta padre (ej: /): ")
                nombre = input("Nombre: ")
                # 1 = Carpeta; cualquier otra tecla = Archivo.
                tipo = "Carpeta" if input("1=Carpeta, 2=Archivo: ").strip() == "1" else "Archivo"
                nodo = fs.crear_nodo(padre, nombre, tipo)  # valida y enlaza
                # Auditoría del Módulo 4: quién creó qué y dónde.
                registrar_log(f"[Árbol] {usuario} creó {nodo.tipo} '{nodo.nombre}' en '{padre}' del servidor '{servidor}'")
                print(">> Creado.")
                input("Presiona ENTER para continuar...")
                os.system("cls")

            # Opción 2: buscar por nombre y mostrar la ruta encontrada.
            elif op == "2":
                ruta = fs.buscar_nodo(input("Nombre a buscar: "))
                print(f"Encontrado: {ruta}" if ruta else "No existe.")
                input("Presiona ENTER para continuar...")
                os.system("cls")
            # Opción 3: imprimir el árbol completo con indentación.
            elif op == "3":
                fs.mostrar_arbol()
                input("Presiona ENTER para continuar...")
                os.system("cls")

            # Opción 4: eliminar la ruta indicada (en cascada si es carpeta).
            elif op == "4":
                ruta = input("Ruta a eliminar: ")
                fs.eliminar_nodo(ruta)  # lanza ValueError si la ruta no existe
                # Auditoría del Módulo 4 sobre la eliminación.
                registrar_log(f"[Árbol] {usuario} eliminó '{ruta}' (en cascada) del servidor '{servidor}'")
                print(">> Eliminado.")
                input("Presiona ENTER para continuar...")
                os.system("cls")
                
            else:
                print("Opción inválida.")
                input("Presiona ENTER para continuar...")
                os.system("cls")
        # Cualquier ValueError lanzado por el árbol se muestra con su mensaje.
        except ValueError as e:
            print(f">> Error: {e}")
            input("Presiona ENTER para continuar...")
            os.system("cls")


def menu_red(grafo):
    """Las operaciones del grafo ya se auditan solas vía funcion_log."""
    while True:
        # Opciones del Módulo 3 (red/enrutamiento); el log lo hace Grafo solo.
        print("\n--- RED ---\n1. Agregar servidor\n2. Agregar conexión\n3. Eliminar conexión\n"
             "4. Eliminar servidor\n5. Ruta más corta (Dijkstra)\n6. Ping general (BFS)\n7. Ver red\n8. Volver")
        op = input("Elija una opción: ").strip()
        os.system("cls")  # limpiar pantalla tras leer la opción

        # 1) Crear un servidor (vértice) nuevo en la red.
        if op == "1":
            nombre = input("Servidor: ").strip()
            # agregar_servidor imprime sus errores; aquí se confirma el éxito.
            if grafo.agregar_servidor(nombre):
                print(f">> Servidor '{nombre}' agregado correctamente.")
            input("Presiona ENTER para continuar...")
            os.system("cls")

        # 2) Conectar dos servidores; la latencia debe ser un número.
        elif op == "2":
            a, b = input("Origen: ").strip(), input("Destino: ").strip()
            latencia = None
            try:
                latencia = float(input("Latencia ms: "))
            except ValueError:
                # float() falló: se tecleó algo que no es un número.
                print(">> Latencia inválida.")
            # Con la latencia convertida se intenta crear la conexión;
            # agregar_conexion imprime sus propios errores si devuelve False.
            if latencia is not None and grafo.agregar_conexion(a, b, latencia):
                print(f">> Conexión '{a} <-> {b}' establecida ({latencia} ms).")
            input("Presiona ENTER para continuar...")
            os.system("cls")
        # 3) Eliminar el enlace (arista) entre dos servidores.
        elif op == "3":
            a, b = input("Origen: ").strip(), input("Destino: ").strip()
            # eliminar_conexion imprime sus errores; aquí se confirma el éxito.
            if grafo.eliminar_conexion(a, b):
                print(f">> Conexión '{a} <-> {b}' eliminada correctamente.")
            input("Presiona ENTER para continuar...")
            os.system("cls")

        elif op == "4":
            nombre = input("Servidor: ").strip()
            # eliminar_servidor imprime sus errores; aquí se confirma el éxito.
            if grafo.eliminar_servidor(nombre):
                print(f">> Servidor '{nombre}' eliminado correctamente.")
            input("Presiona ENTER para continuar...")
            os.system("cls")


        elif op == "5":
            grafo.dijkstra(input("Origen: ").strip(), input("Destino: ").strip())
            input("Presiona ENTER para continuar...")
            os.system("cls")

        elif op == "6":
            inicio = input("Servidor inicial (Enter = automático): ").strip()
            grafo.ping_general(inicio or None)
            input("Presiona ENTER para continuar...")
            os.system("cls")


        elif op == "7":
            grafo.mostrar_red()
            input("Presiona ENTER para continuar...")
            os.system("cls")

        elif op == "8":
            print("Regresando al menu anterior...")
            return
        else:
            print("Opción inválida.")
            input("Presiona ENTER para continuar...")
            os.system("cls")


def main():
    grafo = Grafo(funcion_log=registrar_log)
    # Ciclo de sesiones: 'Cerrar sesión' devuelve al menú de acceso; el
    # programa solo termina cuando en el menú de acceso se elige 'Salir'.
    while True:
        usuario = login(grafo)
        if usuario is None:
            break  # el usuario eligió 'Salir' en el menú de acceso
        while True:
            print("\n=== MENÚ PRINCIPAL ===\n1. Directorios\n2. Red\n3. Consulta en vivo (log)\n4. Cerrar sesión")
            op = input("Elija una opción: ").strip()
            os.system("cls")

            if op == "1":
                menu_directorios(grafo, usuario)
                input("Presiona ENTER para continuar...")
                os.system("cls")
            elif op == "2":
                menu_red(grafo)
                input("Presiona ENTER para continuar...")
                os.system("cls")
            elif op == "3":
                consulta_en_vivo()
                input("Presiona ENTER para continuar...")
                os.system("cls")
            elif op == "4":
                registrar_log(f"[Sesión] {usuario} cerró sesión")
                print(">> Sesión cerrada. Regresando al menú de acceso...")
                input("Presiona ENTER para continuar...")
                os.system("cls")
                break  # vuelve al menú de acceso para iniciar sesión de nuevo
            else:
                print("Opción inválida.")
                input("Presiona ENTER para continuar...")
                os.system("cls")

if __name__ == "__main__":
    main()
