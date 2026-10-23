"""GestorInventario: reglas de negocio y gestión de la colección de productos
y movimientos (registrar, actualizar, buscar, entradas y salidas)."""


import almacenamiento
from modelos.producto import Producto


class GestorInventario:
    def __init__(self):
        datos = almacenamiento.cargar()

        self.productos = []

        for dato in datos:
            self.productos.append(Producto.from_dict(dato))

        codigos = []

        for producto in self.productos:
            if producto.codigo in codigos:
                raise ValueError(
                    "El archivo contiene códigos duplicados."
                )

            codigos.append(producto.codigo)

    def registrar_producto(
        self, codigo, nombre, categoria, precio, cantidad_inicial
    ):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código es obligatorio.")

        codigo = codigo.strip()

        for producto in self.productos:
            if producto.codigo == codigo:
                raise ValueError("El código ya está registrado.")

        nuevo_producto = Producto(
            codigo, nombre, categoria, precio, cantidad_inicial
        )

        nuevos_productos = self.productos + [nuevo_producto]

        datos = []

        for producto in nuevos_productos:
            datos.append(producto.to_dict())

        almacenamiento.guardar(datos)

        self.productos = nuevos_productos

        return nuevo_producto

    def consultar_productos(self):
        return self.productos.copy()

    def buscar_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo.strip():
                return producto

        return None
