"""Programa principal: une directorios (M1), autenticación (M2), red (M3) y auditoría (M4)."""

from auditoria import registrar_log, consulta_en_vivo
from Grafo import Grafo
import os

try:
    import msvcrt  # Solo disponible en Windows: permite ocultar la contraseña
except ImportError:
    msvcrt = None


def _leer_contrasena(prompt="Contraseña: "):
    """Lee una contraseña mostrando un asterisco (*) por cada carácter.

    En Windows usa msvcrt, que captura las teclas sin eco y dibuja un '*'
    por cada carácter, de modo que nadie ve la contraseña mientras se
    escribe. En otras plataformas (sin msvcrt) usa getpass, que oculta la
    entrada por completo como respaldo.
    """
    if msvcrt is None:
        import getpass
        return getpass.getpass(prompt)

    import sys
    sys.stdout.write(prompt)
    sys.stdout.flush()

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
        contrasena.append(tecla)
        sys.stdout.write("*")
        sys.stdout.flush()

    return "".join(contrasena)


def login(grafo):
    """Pantalla de acceso. Devuelve el usuario autenticado o None si sale."""
    while True:
        print("\n=== ACCESO AL SERVIDOR ===\n1. Iniciar sesión\n2. Registrar usuario\n"
              "3. Agregar servidor\n4. Salir")
        op = input("Elija una opción: ").strip()
        os.system("cls")

        if op == "4":
            return None
        if op == "3":
            nombre_servidor = input("Nuevo servidor: ").strip()
        
            if grafo.agregar_servidor(nombre_servidor):
                print(f">> Servidor '{nombre_servidor}' creado con árbol y tabla de credenciales propios.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            continue
        if op not in ("1", "2"):
            print("Opción inválida.")
            input("Presiona ENTER para continuar...")
            os.system("cls")

            continue
        servidor = input("Servidor: ").strip()
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
        if not usuario or not contrasena:
            print(">> Usuario y contraseña no pueden estar vacíos.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            continue

        elif op == "2":
            print(">> Registrado." if usuarios.registrar_usuario(usuario, contrasena) else ">> Ese usuario ya existe.")
            input("Presiona ENTER para continuar...")
            os.system("cls")

        elif usuarios.validar_login(usuario, contrasena):
            print(f">> Bienvenido, {usuario}.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            return usuario
        else:
            print(">> Acceso denegado.")
            input("Presiona ENTER para continuar...")
            os.system("cls")


def menu_directorios(grafo, usuario):
    while True:
        print("\n--- DIRECTORIOS ---\n1. Crear\n2. Buscar\n3. Listar árbol\n4. Eliminar\n5. Volver")
        op = input("Elija una opción: ").strip()
        os.system("cls")

        if op == "5":
            print("Regresando al menu anterior...")
            return
        if op not in ("1", "2", "3", "4"):
            print("Opción inválida.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            continue
        servidor = input("Servidor cuyo sistema de archivos desea usar: ").strip()
        fs = grafo.obtener_sistema_archivos(servidor)
        if fs is None:
            print(">> El servidor no existe en la red.")
            input("Presiona ENTER para continuar...")
            os.system("cls")
            continue
        try:
            if op == "1":
                padre = input("Ruta de la carpeta padre (ej: /): ")
                nombre = input("Nombre: ")
                tipo = "Carpeta" if input("1=Carpeta, 2=Archivo: ").strip() == "1" else "Archivo"
                nodo = fs.crear_nodo(padre, nombre, tipo)
                registrar_log(f"[Árbol] {usuario} creó {nodo.tipo} '{nodo.nombre}' en '{padre}' del servidor '{servidor}'")
                print(">> Creado.")
                input("Presiona ENTER para continuar...")
                os.system("cls")

            elif op == "2":
                ruta = fs.buscar_nodo(input("Nombre a buscar: "))
                print(f"Encontrado: {ruta}" if ruta else "No existe.")
                input("Presiona ENTER para continuar...")
                os.system("cls")
            elif op == "3":
                fs.mostrar_arbol()
                input("Presiona ENTER para continuar...")
                os.system("cls")

            elif op == "4":
                ruta = input("Ruta a eliminar: ")
                fs.eliminar_nodo(ruta)
                registrar_log(f"[Árbol] {usuario} eliminó '{ruta}' (en cascada) del servidor '{servidor}'")
                print(">> Eliminado.")
                input("Presiona ENTER para continuar...")
                os.system("cls")
                
            else:
                print("Opción inválida.")
                input("Presiona ENTER para continuar...")
                os.system("cls")
        except ValueError as e:
            print(f">> Error: {e}")
            input("Presiona ENTER para continuar...")
            os.system("cls")


def menu_red(grafo):
    """Las operaciones del grafo ya se auditan solas vía funcion_log."""
    while True:
        print("\n--- RED ---\n1. Agregar servidor\n2. Agregar conexión\n3. Eliminar conexión\n"
              "4. Eliminar servidor\n5. Ruta más corta (Dijkstra)\n6. Ping general (BFS)\n7. Ver red\n8. Volver")
        op = input("Elija una opción: ").strip()
        os.system("cls")

        if op == "1":
            grafo.agregar_servidor(input("Servidor: ").strip())
            input("Presiona ENTER para continuar...")
            os.system("cls")

        elif op == "2":
            a, b = input("Origen: ").strip(), input("Destino: ").strip()
            try:
                grafo.agregar_conexion(a, b, float(input("Latencia ms: ")))
            except ValueError:
                print(">> Latencia inválida.")
                input("Presiona ENTER para continuar...")
                os.system("cls")
        elif op == "3":
            grafo.eliminar_conexion(input("Origen: ").strip(), input("Destino: ").strip())
            input("Presiona ENTER para continuar...")
            os.system("cls")

        elif op == "4":
            grafo.eliminar_servidor(input("Servidor: ").strip())
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
