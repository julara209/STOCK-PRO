"""Punto de entrada: carga los datos y abre el menú principal.
Solo llama a los demás módulos."""
from consola.menu_principal import menu_principal
from servicios.autenticacion import Autenticacion
from servicios.inventario import GestorInventario
from servicios.usuarios import cargar_usuarios


def main():
    try:
        inventario = GestorInventario()
        usuarios = cargar_usuarios()
    except (ValueError, OSError) as error:
        print("Error al cargar los datos:", error)
        return

    autenticacion = Autenticacion(usuarios)
    menu_principal(inventario, autenticacion, usuarios)
    print("Programa finalizado.")


if __name__ == "__main__":
    main()
