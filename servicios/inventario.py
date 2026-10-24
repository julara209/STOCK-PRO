"""GestorInventario: reglas de negocio y gestión de la colección de productos
y movimientos (registrar, actualizar, buscar, entradas y salidas)."""


import almacenamiento
from modelos.producto import Producto
from servicios.busqueda import buscar_productos as _buscar
from servicios.actualizacion import (
    ProductoNoEncontradoError,
    construir_producto_actualizado,
)

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

        return None

    def actualizar_producto(self, codigo, nombre=None, categoria=None,
                            precio=None, entrada=None):
        codigo = codigo.strip()

        posicion = None
        for i, producto in enumerate(self.productos):
            if producto.codigo == codigo:
                posicion = i
                break

        if posicion is None:
            raise ProductoNoEncontradoError(f"El producto '{codigo}' no existe.")

        # Si algún dato es inválido, esta línea lanza ValueError y no se
        # modifica ni la memoria ni el archivo.
        actualizado = construir_producto_actualizado(
            self.productos[posicion], nombre, categoria, precio, entrada
        )

        nuevos_productos = self.productos.copy()
        nuevos_productos[posicion] = actualizado

        datos = [producto.to_dict() for producto in nuevos_productos]
        almacenamiento.guardar(datos)

        self.productos = nuevos_productos
        return actualizado