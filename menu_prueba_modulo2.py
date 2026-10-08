"""
Menú de prueba aislado del Módulo 2 (Autenticación - Tabla Hash).
Se ejecuta solo, sin depender de los otros módulos, para demostrarlo
en la defensa técnica.
"""

from TablaHash import TablaHash


def menu_prueba():
    tabla = TablaHash()

    while True:
        print("\n=== MÓDULO 2: Autenticación (Tabla Hash) - Menú de prueba ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesión (login)")
        print("3. Ver estructura interna de la tabla")
        print("4. Salir")
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            usuario = input("Nuevo usuario: ").strip()
            contrasena = input("Contraseña: ").strip()
            tabla.registrar_usuario(usuario, contrasena)

        elif opcion == "2":
            usuario = input("Usuario: ").strip()
            contrasena = input("Contraseña: ").strip()
            if tabla.validar_login(usuario, contrasena):
                print(">> Acceso concedido.")
            else:
                print(">> Acceso denegado.")

        elif opcion == "3":
            tabla.mostrar_tabla()

        elif opcion == "4":
            print("Saliendo del módulo de prueba...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_prueba()