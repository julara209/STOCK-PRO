"""Entidad Movimiento para el historial de inventario."""

from datetime import datetime
from uuid import uuid4


class Movimiento:
    def __init__(
        self,
        tipo,
        codigo_producto,
        cantidad,
        usuario_responsable,
        nombre_producto="",
        id_movimiento=None,
        fecha=None
    ):
        self.id_movimiento = (
            str(uuid4())
            if id_movimiento is None
            else str(id_movimiento)
        )
        self.tipo = tipo
        self.codigo_producto = codigo_producto
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.fecha = (
            datetime.now().isoformat(timespec="seconds")
            if fecha is None
            else fecha
        )
        self.usuario_responsable = usuario_responsable

    def to_dict(self):
        return {
            "id_movimiento": self.id_movimiento,
            "tipo": self.tipo,
            "codigo_producto": self.codigo_producto,
            "nombre_producto": self.nombre_producto,
            "cantidad": self.cantidad,
            "fecha": self.fecha,
            "usuario_responsable": self.usuario_responsable
        }

    def __str__(self):
        return (
            f"ID: {self.id_movimiento} | "
            f"Tipo: {self.tipo} | "
            f"Producto: {self.nombre_producto or self.codigo_producto} | "
            f"Código: {self.codigo_producto} | "
            f"Cantidad: {self.cantidad} | "
            f"Fecha: {self.fecha} | "
            f"Responsable: {self.usuario_responsable}"
        )