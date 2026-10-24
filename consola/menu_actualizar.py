"""Consola de actualización de productos (HU-002). Usa input()/print();
las reglas de negocio están en servicios/actualizacion.py."""
from servicios.actualizacion import ProductoNoEncontradoError


def _pedir_numero(mensaje, convertir):
    """Pide un número opcional. Devuelve None si se deja vacío.
    Lanza ValueError si el texto no se puede convertir."""
    texto = input(mensaje).strip().replace(",", ".")
    if texto == "":
        return None
    try:
        return convertir(texto)
    except ValueError:
        raise ValueError(f"'{texto}' no es un número válido.") from None


def menu_actualizar(gestor):
    print("\n--- Actualizar producto (Enter para no cambiar un dato) ---")
    codigo = input("Código del producto: ").strip()
    try:
        nombre = input("Nuevo nombre: ").strip() or None
        categoria = input("Nueva categoría: ").strip() or None
        precio = _pedir_numero("Nuevo precio: ", float)
        entrada = _pedir_numero("Cantidad que ingresa al stock: ", int)
        producto = gestor.actualizar_producto(codigo, nombre, categoria,
                                              precio, entrada)
    except (ProductoNoEncontradoError, ValueError) as error:
        print(f"\nActualización rechazada: {error}")
    except OSError as error:
        print(f"\nError al guardar: {error}")
    else:
        print("\nProducto actualizado correctamente.")
        print(producto)
