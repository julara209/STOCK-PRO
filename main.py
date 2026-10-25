"""Interfaz de consola: menús, input() y print().
Solo llama a los demás módulos."""
from consola.menu_actualizar import menu_actualizar
from consola.menu_buscar import menu_buscar
from consola.menu_entrada import menu_entrada
from consola.menu_exportar import menu_exportar
from consola.menu_historial import menu_historial
from consola.menu_reportes import menu_reportes
from consola.menu_salidas import menu_registrar_salida
from servicios.inventario import GestorInventario


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
        print("5. Registrar entrada de mercancía")
        print("6. Registrar salida de mercancía")
        print("7. Consultar historial de movimientos")
        print("8. Reportes de inventario")
        print("9. Exportar a CSV")
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

        elif opcion == "4":
            menu_actualizar(inventario)

        elif opcion == "5":
            menu_entrada(inventario)

        elif opcion == "6":
            menu_registrar_salida(inventario)

        elif opcion == "7":
            menu_historial(inventario)

        elif opcion == "8":
            menu_reportes(inventario)

        elif opcion == "9":
            menu_exportar(inventario)

        elif opcion == "0":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()