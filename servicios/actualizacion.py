"""Reglas de actualización de productos (HU-002)."""
from modelos.producto import Producto


class ProductoNoEncontradoError(Exception):
    """Se intentó operar sobre un código que no está registrado."""


def construir_producto_actualizado(producto, nombre=None, categoria=None,
                                   precio=None, entrada=None):
    """Devuelve un Producto NUEVO con los cambios pedidos; no modifica el original.

    Los campos en None se conservan. 'entrada' se suma a las existencias.
    Las validaciones las hace el constructor de Producto, así que la regla
    vive en un solo lugar. Si algún dato es inválido lanza ValueError.
    """
    if entrada is not None:
        if isinstance(entrada, bool) or not isinstance(entrada, int) or entrada <= 0:
            raise ValueError("La entrada debe ser un entero mayor que cero.")

    cantidad = producto.cantidad + (entrada or 0)

    return Producto(
        producto.codigo,
        producto.nombre if nombre is None else nombre,
        producto.categoria if categoria is None else categoria,
        producto.precio if precio is None else precio,
        cantidad,
    )
