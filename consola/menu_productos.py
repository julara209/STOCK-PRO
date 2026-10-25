"""Pantalla de consola: registrar un producto (HU-001)."""


def menu_registrar_producto(gestor):
    print("\n--- Registrar producto ---")
    try:
        codigo = input("Código: ")
        nombre = input("Nombre: ")
        categoria = input("Categoría: ")
        precio = input("Precio: ").replace(",", ".")
        cantidad = int(input("Cantidad inicial: "))

        producto = gestor.registrar_producto(
            codigo, nombre, categoria, precio, cantidad
        )
    except ValueError as error:
        print("\nRegistro rechazado:", error)
    except OSError as error:
        print("\nError al guardar:", error)
    else:
        print("\nProducto registrado correctamente.")
        print(producto)
