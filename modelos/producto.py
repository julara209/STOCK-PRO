"""Entidad Producto: datos y validaciones de un producto del inventario."""


class Producto:
    def __init__(self, codigo, nombre, categoria, precio, cantidad_inicial):

        if not codigo.strip():
            raise ValueError("El código es obligatorio.")

        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if not categoria.strip():
            raise ValueError("La categoría es obligatoria.")

        try:
            precio = float(precio)
        except ValueError:
            raise ValueError("El precio debe ser un número válido.")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        if cantidad_inicial < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        self.codigo = codigo.strip()
        self.nombre = nombre.strip()
        self.categoria = categoria.strip()
        self.precio = precio
        self.cantidad = cantidad_inicial

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "cantidad": self.cantidad
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos["codigo"],
            datos["nombre"],
            datos["categoria"],
            datos["precio"],
            datos["cantidad"]
        )

    def __str__(self):
        return (
            f"Código: {self.codigo} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Precio: ${self.precio:.2f} | "
            f"Cantidad: {self.cantidad}"
        )
