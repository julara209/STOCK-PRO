"""Reglas de la salida de mercancía (HU-005)."""
from modelos.producto import Producto


def calcular_salida(producto, cantidad):
    """Devuelve un Producto NUEVO con las existencias descontadas.

    No modifica el original. Lanza ValueError si la cantidad no es un entero
    mayor que cero o si supera las existencias disponibles.
    """
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un entero mayor que cero.")

    if cantidad > producto.cantidad:
        raise ValueError(
            f"Existencias insuficientes: hay {producto.cantidad} "
            f"y se intentó retirar {cantidad}."
        )

    return Producto(
        producto.codigo,
        producto.nombre,
        producto.categoria,
        producto.precio,
        producto.cantidad - cantidad,
    )
