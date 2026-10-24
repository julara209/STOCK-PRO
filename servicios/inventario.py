"""GestorInventario: reglas de negocio y gestión de la colección de productos
y movimientos (registrar, actualizar, buscar, entradas y salidas)."""


import almacenamiento
from modelos.producto import Producto
from servicios.busqueda import buscar_productos as _buscar
from constantes import TIPO_SALIDA
from modelos.movimiento import Movimiento
from servicios.salidas import calcular_salida

class GestorInventario:
    def __init__(self):
        datos = almacenamiento.cargar()

        self.productos = []

        self.movimientos = [
            Movimiento.from_dict(dato)
            for dato in almacenamiento.cargar_movimientos()
        ]

        for dato in datos:
            self.productos.append(Producto.from_dict(dato))

        codigos = []

        for producto in self.productos:
            if producto.codigo in codigos:
                raise ValueError(
                    "El archivo contiene códigos duplicados."
                )

            codigos.append(producto.codigo)

    def buscar_productos(self, codigo=None, nombre=None, categoria=None):
        return _buscar(self.productos, codigo, nombre, categoria)

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
    def registrar_salida(self, codigo, cantidad, usuario):
        codigo = codigo.strip()

        posicion = None
        for i, producto in enumerate(self.productos):
            if producto.codigo == codigo:
                posicion = i
                break

        if posicion is None:
            raise ValueError(f"El producto '{codigo}' no existe.")

        # Estas dos líneas validan todo (cantidad, existencias, usuario).
        producto_actualizado = calcular_salida(self.productos[posicion], cantidad)
        movimiento = Movimiento(
            f"MOV-{len(self.movimientos) + 1:04d}",
            TIPO_SALIDA,
            codigo,
            cantidad,
            usuario,
        )

        nuevos_productos = self.productos.copy()
        nuevos_productos[posicion] = producto_actualizado
        nuevos_movimientos = self.movimientos + [movimiento]

        datos_anteriores = [producto.to_dict() for producto in self.productos]

        almacenamiento.guardar([p.to_dict() for p in nuevos_productos])
        try:
            almacenamiento.guardar_movimientos(
                [m.to_dict() for m in nuevos_movimientos]
            )
        except OSError:
            # Si falla el historial, se devuelven las existencias anteriores.
            almacenamiento.guardar(datos_anteriores)
            raise

        self.productos = nuevos_productos
        self.movimientos = nuevos_movimientos
        return movimiento
        return None
