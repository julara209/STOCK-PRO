"""Interfaz de consola: menús, input() y print().
Solo llama a los demás módulos."""
from consola.menu_buscar import menu_buscar
from servicios.inventario import GestorInventario
from consola.menu_salidas import menu_registrar_salida

def main():
    try:
        inventario = GestorInventario()
    except (ValueError, OSError) as error:
        print("Error al cargar el inventario:", error)
        return

    while True:
        print("\n===== REGISTRAR PRODUCTO =====")
        print("1. Registrar producto")
        print("2. Consultar productos")
        print("3. Buscar productos (código, nombre o categoría)")        
        print("4. Actualizar producto")
        print("5. Registrar salida de mercancía")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                codigo = input("Código: ")
                nombre = input("Nombre: ")
                categoria = input("Categoría: ")
                precio = input("Precio: ").replace(",", ".")
                cantidad = int(input("Cantidad inicial: "))

                producto = inventario.registrar_producto(
                    codigo,
                    nombre,
                    categoria,
                    precio,
                    cantidad
                )

                print("\nProducto registrado correctamente.")
                print(producto)

            except ValueError as error:
                print("\nRegistro rechazado:", error)
            except OSError as error:
                print("\nError al guardar:", error)

        elif opcion == "2":
            productos = inventario.consultar_productos()

            if len(productos) == 0:
                print("\nNo hay productos registrados.")
            else:
                for producto in productos:
                    print(producto)

        elif opcion == "3":
            menu_buscar(inventario)

            if producto is None:
                print("Producto no encontrado.")
            else:
                print(producto)

        elif opcion == "5":
            menu_registrar_salida(inventario)

        elif opcion == "0":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
