"""Programa principal: une directorios (M1), autenticación (M2), red (M3) y auditoría (M4)."""

from auditoria import registrar_log, consulta_en_vivo
from Grafo import Grafo


def login(grafo):
    """Pantalla de acceso. Devuelve el usuario autenticado o None si sale."""
    while True:
        print("\n=== ACCESO AL SERVIDOR ===\n1. Iniciar sesión\n2. Registrar usuario\n"
              "3. Agregar servidor\n4. Salir")
        op = input("Elija una opción: ").strip()
        if op == "4":
            return None
        if op == "3":
            nombre_servidor = input("Nuevo servidor: ").strip()
            if grafo.agregar_servidor(nombre_servidor):
                print(f">> Servidor '{nombre_servidor}' creado con árbol y tabla de credenciales propios.")
            continue
        if op not in ("1", "2"):
            print("Opción inválida.")
            continue
        servidor = input("Servidor: ").strip()
        usuarios = grafo.obtener_tabla_credenciales(servidor)
        if usuarios is None:
            print(">> Ese servidor no existe. Créelo primero con la opción 3.")
            continue
        usuario = input("Usuario: ").strip()
        contrasena = input("Contraseña: ").strip()
        if not usuario or not contrasena:
            print(">> Usuario y contraseña no pueden estar vacíos.")
        elif op == "2":
            print(">> Registrado." if usuarios.registrar_usuario(usuario, contrasena) else ">> Ese usuario ya existe.")
        elif usuarios.validar_login(usuario, contrasena):
            print(f">> Bienvenido, {usuario}.")
            return usuario
        else:
            print(">> Acceso denegado.")


def menu_directorios(grafo, usuario):
    while True:
        print("\n--- DIRECTORIOS ---\n1. Crear\n2. Buscar\n3. Listar árbol\n4. Eliminar\n5. Volver")
        op = input("Elija una opción: ").strip()
        if op == "5":
            return
        if op not in ("1", "2", "3", "4"):
            print("Opción inválida.")
            continue
        servidor = input("Servidor cuyo sistema de archivos desea usar: ").strip()
        fs = grafo.obtener_sistema_archivos(servidor)
        if fs is None:
            print(">> El servidor no existe en la red.")
            continue
        try:
            if op == "1":
                padre = input("Ruta de la carpeta padre (ej: /): ")
                nombre = input("Nombre: ")
                tipo = "Carpeta" if input("1=Carpeta, 2=Archivo: ").strip() == "1" else "Archivo"
                nodo = fs.crear_nodo(padre, nombre, tipo)
                registrar_log(f"[Árbol] {usuario} creó {nodo.tipo} '{nodo.nombre}' en '{padre}' del servidor '{servidor}'")
                print(">> Creado.")
            elif op == "2":
                ruta = fs.buscar_nodo(input("Nombre a buscar: "))
                print(f"Encontrado: {ruta}" if ruta else "No existe.")
            elif op == "3":
                fs.mostrar_arbol()
            elif op == "4":
                ruta = input("Ruta a eliminar: ")
                fs.eliminar_nodo(ruta)
                registrar_log(f"[Árbol] {usuario} eliminó '{ruta}' (en cascada) del servidor '{servidor}'")
                print(">> Eliminado.")
            else:
                print("Opción inválida.")
        except ValueError as e:
            print(f">> Error: {e}")


def menu_red(grafo):
    """Las operaciones del grafo ya se auditan solas vía funcion_log."""
    while True:
        print("\n--- RED ---\n1. Agregar servidor\n2. Agregar conexión\n3. Eliminar conexión\n"
              "4. Eliminar servidor\n5. Ruta más corta (Dijkstra)\n6. Ping general (BFS)\n7. Ver red\n8. Volver")
        op = input("Elija una opción: ").strip()
        if op == "1":
            grafo.agregar_servidor(input("Servidor: ").strip())
        elif op == "2":
            a, b = input("Origen: ").strip(), input("Destino: ").strip()
            try:
                grafo.agregar_conexion(a, b, float(input("Latencia ms: ")))
            except ValueError:
                print(">> Latencia inválida.")
        elif op == "3":
            grafo.eliminar_conexion(input("Origen: ").strip(), input("Destino: ").strip())
        elif op == "4":
            grafo.eliminar_servidor(input("Servidor: ").strip())
        elif op == "5":
            grafo.dijkstra(input("Origen: ").strip(), input("Destino: ").strip())
        elif op == "6":
            inicio = input("Servidor inicial (Enter = automático): ").strip()
            grafo.ping_general(inicio or None)
        elif op == "7":
            grafo.mostrar_red()
        elif op == "8":
            return
        else:
            print("Opción inválida.")


def main():
    grafo = Grafo(funcion_log=registrar_log)
    usuario = login(grafo)
    if usuario is None:
        return
    while True:
        print("\n=== MENÚ PRINCIPAL ===\n1. Directorios\n2. Red\n3. Consulta en vivo (log)\n4. Cerrar sesión")
        op = input("Elija una opción: ").strip()
        if op == "1":
            menu_directorios(grafo, usuario)
        elif op == "2":
            menu_red(grafo)
        elif op == "3":
            consulta_en_vivo()
        elif op == "4":
            registrar_log(f"[Sesión] {usuario} cerró sesión")
            return
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
