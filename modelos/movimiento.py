"""Entidad Movimiento: entradas y salidas de mercancía (HU-005, HU-006)."""
from datetime import datetime

from constantes import TIPO_ENTRADA, TIPO_SALIDA


class Movimiento:
    def __init__(self, id_movimiento, tipo, codigo_producto, cantidad,
                 usuario, fecha=None):
        if not isinstance(id_movimiento, str) or not id_movimiento.strip():
            raise ValueError("El movimiento necesita un identificador.")

        if tipo not in (TIPO_ENTRADA, TIPO_SALIDA):
            raise ValueError(
                f"El tipo de movimiento debe ser '{TIPO_ENTRADA}' o '{TIPO_SALIDA}'."
            )

        if not isinstance(codigo_producto, str) or not codigo_producto.strip():
            raise ValueError("El código del producto es obligatorio.")

        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero mayor que cero.")

        if not isinstance(usuario, str) or not usuario.strip():
            raise ValueError("El usuario responsable es obligatorio.")

        self.id_movimiento = id_movimiento.strip()
        self.tipo = tipo
        self.codigo_producto = codigo_producto.strip()
        self.cantidad = cantidad
        self.usuario = usuario.strip()
        self.fecha = fecha or datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return {
            "id_movimiento": self.id_movimiento,
            "tipo": self.tipo,
            "codigo_producto": self.codigo_producto,
            "cantidad": self.cantidad,
            "usuario": self.usuario,
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos["id_movimiento"],
            datos["tipo"],
            datos["codigo_producto"],
            datos["cantidad"],
            datos["usuario"],
            datos["fecha"],
        )

    def __str__(self):
        return (
            f"{self.id_movimiento} | {self.fecha} | {self.tipo} | "
            f"Producto: {self.codigo_producto} | Cantidad: {self.cantidad} | "
            f"Usuario: {self.usuario}"
        )