"""Programa principal: une directorios (M1), autenticación (M2), red (M3) y auditoría (M4)."""

from auditoria import registrar_log, consulta_en_vivo
from Grafo import Grafo
from TablaHash import TablaHash
from sistema_archivos import FileSystem


def login(usuarios):
    """Pantalla de acceso. Devuelve el usuario autenticado o None si sale."""
    while True:
        print("\n=== ACCESO AL SERVIDOR ===\n1. Iniciar sesión\n2. Registrar usuario\n3. Salir")
        op = input("Elija una opción: ").strip()
        if op == "3":
            return None
        if op not in ("1", "2"):
            print("Opción inválida.")
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


def menu_directorios(fs, usuario):
    while True:
        print("\n--- DIRECTORIOS ---\n1. Crear\n2. Buscar\n3. Listar árbol\n4. Eliminar\n5. Volver")
        op = input("Elija una opción: ").strip()
        try:
            if op == "1":
                padre = input("Ruta de la carpeta padre (ej: /): ")
                nombre = input("Nombre: ")
                tipo = "Carpeta" if input("1=Carpeta, 2=Archivo: ").strip() == "1" else "Archivo"
                nodo = fs.crear_nodo(padre, nombre, tipo)
                registrar_log(f"[Árbol] {usuario} creó {nodo.tipo} '{nodo.nombre}' en '{padre}'")
                print(">> Creado.")
            elif op == "2":
                ruta = fs.buscar_nodo(input("Nombre a buscar: "))
                print(f"Encontrado: {ruta}" if ruta else "No existe.")
            elif op == "3":
                fs.mostrar_arbol()
            elif op == "4":
                ruta = input("Ruta a eliminar: ")
                fs.eliminar_nodo(ruta)
                registrar_log(f"[Árbol] {usuario} eliminó '{ruta}' (en cascada)")
                print(">> Eliminado.")
            elif op == "5":
                return
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
    usuarios = TablaHash(funcion_log=registrar_log)
    usuario = login(usuarios)
    if usuario is None:
        return
    fs, grafo = FileSystem(), Grafo(funcion_log=registrar_log)
    while True:
        print("\n=== MENÚ PRINCIPAL ===\n1. Directorios\n2. Red\n3. Consulta en vivo (log)\n4. Cerrar sesión")
        op = input("Elija una opción: ").strip()
        if op == "1":
            menu_directorios(fs, usuario)
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
