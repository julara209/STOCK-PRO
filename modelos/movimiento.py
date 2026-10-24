"""Entidad Movimiento: registra entradas y salidas de mercancía."""
from datetime import datetime


class Movimiento:
    def __init__(
        self,
        codigo_producto,
        nombre_producto,
        cantidad,
        usuario_responsable,
        fecha=None,
        tipo="Entrada"
    ):
        if not isinstance(codigo_producto, str) or not codigo_producto.strip():
            raise ValueError("El código del producto es obligatorio.")

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ValueError(
                "La cantidad debe ser un entero mayor que cero."
            )

        if (
            not isinstance(usuario_responsable, str)
            or not usuario_responsable.strip()
        ):
            raise ValueError("El usuario responsable es obligatorio.")

        self.fecha = fecha or datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.codigo_producto = codigo_producto.strip()
        self.nombre_producto = nombre_producto.strip()
        self.cantidad = cantidad
        self.usuario_responsable = usuario_responsable.strip()
        self.tipo = tipo

    def to_dict(self):
        return {
            "fecha": self.fecha,
            "tipo": self.tipo,
            "codigo_producto": self.codigo_producto,
            "nombre_producto": self.nombre_producto,
            "cantidad": self.cantidad,
            "usuario_responsable": self.usuario_responsable
        }
