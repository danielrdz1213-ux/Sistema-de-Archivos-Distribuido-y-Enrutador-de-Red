"""Menú Provisional - Árbol de directorios.

Permite demostrar de forma aislada las operaciones del sistema de archivos
sin necesidad del módulo de red:

    1. Crear          -> crear_nodo()
    2. Buscar         -> buscar_nodo()
    3. Listar árbol   -> mostrar_arbol()
    4. Eliminar       -> eliminar_nodo()
    5. Salir

Ejecución:
    python menu_provisional.py
"""

from sistema_archivos import FileSystem


def mostrar_menu():
    """Imprime en consola las opciones disponibles del menú."""
    print()
    print("=" * 52)
    print("   SISTEMA DE ARCHIVOS DISTRIBUIDO - Menú Provisional")
    print("   Prueba aislada del árbol de directorios")
    print("=" * 52)
    print("   1. Crear")
    print("   2. Buscar")
    print("   3. Listar árbol")
    print("   4. Eliminar")
    print("   5. Salir")
    print("=" * 52)


if __name__ == '__main__':
    # Árbol vacío: el constructor crea automáticamente la raíz "/"
    fs = FileSystem()
    print("Sistema de archivos iniciado. La raíz '/' ya está disponible.")

    while True:
        mostrar_menu()

        try:
            opcion = input("Seleccione una opción (1-5): ").strip()
        except EOFError:
            # Se agotó la entrada (por ejemplo, sin teclado disponible)
            print("\nEntrada finalizada. Cerrando el menú de pruebas.")
            break

        # ------------------------- 1. Crear -------------------------
        if opcion == "1":
            if fs.esta_vacio():
                # Disco vacío: el primer nodo solo puede ir en la raíz
                print(
                    "Nota: Como el disco duro está vacío, este primer elemento "
                    "se guardará automáticamente en la raíz (/)."
                )
                ruta_padre = "/"
            else:
                ruta_padre = input(
                    'Ruta de la carpeta padre (Recuerde empezar con / , ej: /hola): '
                )

            nombre_nuevo = input("Nombre del nodo (ej. 'nota.txt'): ")

            # Submenú numérico rápido: evita que el usuario escriba el tipo
            opcion_tipo = input("Ingrese 1 para Carpeta o 2 para Archivo: ").strip()
            if opcion_tipo == "1":
                tipo_nuevo = "Carpeta"
            elif opcion_tipo == "2":
                tipo_nuevo = "Archivo"
            else:
                print(
                    f"Tipo inválido: '{opcion_tipo}'. "
                    "Debe escribir 1 (Carpeta) o 2 (Archivo)."
                )
                print("Se canceló la creación de este nodo.")
                continue

            try:
                nuevo_nodo = fs.crear_nodo(ruta_padre, nombre_nuevo, tipo_nuevo)
                print(
                    f"Listo: se creó el nodo '{nuevo_nodo.nombre}' "
                    f"({nuevo_nodo.tipo}) dentro de '{ruta_padre}'."
                )
            except ValueError as error:
                print("No se pudo crear el nodo.")
                print(f"Detalle: {error}")

        # ------------------------- 2. Buscar -------------------------
        elif opcion == "2":
            nombre_objetivo = input("Nombre a buscar (sin ruta): ")
            ruta_encontrada = fs.buscar_nodo(nombre_objetivo)

            if ruta_encontrada is None:
                print(
                    "No existe ningún archivo o carpeta llamado "
                    f"'{nombre_objetivo.strip()}' en todo el sistema."
                )
            else:
                print(f"Encontrado: {ruta_encontrada}")

        # ---------------------- 3. Listar árbol ----------------------
        elif opcion == "3":
            print("Estructura actual del sistema de archivos:")
            fs.mostrar_arbol()
            if fs.esta_vacio():
                print("(la raíz '/' todavía no tiene nodos dentro)")

        # ------------------------ 4. Eliminar ------------------------
        elif opcion == "4":
            ruta_objetivo = input("Ruta a eliminar (ej. '/Documentos/nota.txt'): ")

            try:
                fs.eliminar_nodo(ruta_objetivo)
                print(f"Listo: se eliminó '{ruta_objetivo}'.")
                if not fs.esta_vacio():
                    print("Árbol después de la eliminación:")
                    fs.mostrar_arbol()
            except ValueError as error:
                print("No se pudo eliminar.")
                print(f"Detalle: {error}")

        # -------------------------- 5. Salir --------------------------
        elif opcion == "5":
            print("Saliendo del Menú Provisional. ¡Hasta luego!")
            break

        else:
            print(f"Opción inválida: '{opcion}'. Debe elegir un número del 1 al 5.")
