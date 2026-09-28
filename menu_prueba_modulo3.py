"""Menú de prueba aislado del Módulo 3 (Topología y Enrutamiento - Grafos).
Se ejecuta solo, sin depender de los otros módulos
"""

from Grafo import Grafo


def menu_prueba():
    grafo = Grafo()

    while True:
        print("\n=== MÓDULO 3: Red de Servidores (Grafo) - Menú de prueba ===")
        print("1. Agregar servidor")
        print("2. Agregar conexión (fibra)")
        print("3. Eliminar conexión")
        print("4. Eliminar servidor")
        print("5. Calcular ruta más corta (Dijkstra)")
        print("6. Ping general (BFS)")
        print("7. Ver red actual")
        print("8. Salir")
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre del servidor: ").strip()
            if grafo.agregar_servidor(nombre):
                print(f">> Servidor '{nombre.strip()}' agregado a la red.")

        elif opcion == "2":
            origen = input("Servidor origen: ").strip()
            destino = input("Servidor destino: ").strip()
            try:
                latencia = float(input("Latencia en ms: ").strip())
            except ValueError:
                print(">> Latencia inválida: debe ser un número.")
                continue
            if grafo.agregar_conexion(origen, destino, latencia):
                print(f">> Conexión establecida: {origen} <-> {destino} ({latencia} ms).")

        elif opcion == "3":
            origen = input("Servidor origen: ").strip()
            destino = input("Servidor destino: ").strip()
            if grafo.eliminar_conexion(origen, destino):
                print(f">> Conexión eliminada: {origen} <-> {destino}.")

        elif opcion == "4":
            nombre = input("Servidor a eliminar: ").strip()
            if grafo.eliminar_servidor(nombre):
                print(f">> Servidor '{nombre}' eliminado junto con sus conexiones.")

        elif opcion == "5":
            origen = input("Servidor origen: ").strip()
            destino = input("Servidor destino: ").strip()
            grafo.dijkstra(origen, destino)

        elif opcion == "6":
            inicio = input("Servidor desde el que lanzar el ping (Enter = automático): ").strip()
            grafo.ping_general(inicio if inicio else None)

        elif opcion == "7":
            grafo.mostrar_red()

        elif opcion == "8":
            print("Saliendo del módulo de prueba...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_prueba()
