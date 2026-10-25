"""Interacción de consola para registrar entradas de mercancía."""
from servicios.actualizacion import ProductoNoEncontradoError


def _pedir_cantidad():
    while True:
        texto = input("Cantidad recibida: ").strip()

        try:
            cantidad = int(texto)
        except ValueError:
            print("La cantidad debe ser un número entero.")
            continue

        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            continue

        return cantidad


def menu_entrada(gestor, usuario=None):
    print("\n--- Registrar entrada de mercancía ---")

    codigo = input("Código del producto: ").strip()
    cantidad = _pedir_cantidad()
    if usuario is None:
        usuario = input("Usuario responsable: ").strip()

    try:
        producto = gestor.registrar_entrada(
            codigo,
            cantidad,
            usuario
        )
    except (ProductoNoEncontradoError, ValueError) as error:
        print(f"\nEntrada rechazada: {error}")
    except OSError as error:
        print(f"\nError al guardar la entrada: {error}")
    else:
        print("\nEntrada registrada correctamente.")
        print(producto)
