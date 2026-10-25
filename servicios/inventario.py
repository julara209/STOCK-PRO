"""GestorInventario: reglas de negocio y gestión de la colección de productos
y movimientos (registrar, actualizar, buscar, entradas y salidas)."""

import almacenamiento
from modelos.movimiento import Movimiento
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

    def registrar_entrada(self, codigo, cantidad, usuario_responsable):
        """Suma existencias y registra la entrada en el historial."""
        if (
            not isinstance(usuario_responsable, str)
            or not usuario_responsable.strip()
            ):
            raise ValueError(
                "El usuario responsable no puede estar vacío."
            )

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ValueError(
                "La cantidad recibida debe ser un entero mayor que cero."
            )

        producto = self.buscar_producto(codigo)

        if producto is None:
            raise ProductoNoEncontradoError(
                f"El producto '{codigo}' no existe."
            )

        movimiento = Movimiento(
            "Entrada",
            producto.codigo,
            cantidad,
            usuario_responsable.strip(),
            nombre_producto=producto.nombre
            )

        actualizado = Producto(
            producto.codigo,
            producto.nombre,
            producto.categoria,
            producto.precio,
            producto.cantidad + cantidad
        )

        nuevos_productos = self.productos.copy()
        posicion = nuevos_productos.index(producto)
        nuevos_productos[posicion] = actualizado

        movimientos = almacenamiento.cargar_movimientos()
        nuevos_movimientos = movimientos + [movimiento.to_dict()]

        # Guardar antes de actualizar la colección en memoria.
        almacenamiento.guardar(
            [p.to_dict() for p in nuevos_productos]
        )

        almacenamiento.guardar_movimientos(nuevos_movimientos)

        self.productos = nuevos_productos

        return actualizado

    def consultar_historial_movimientos(self, codigo_producto=None, tipo=None):
        """Consulta el historial sin modificar el inventario ni los archivos."""
        movimientos = almacenamiento.cargar_movimientos()

        resultado = []

        if codigo_producto is not None:
            codigo_producto = codigo_producto.strip()

        if tipo is not None:
            tipo = tipo.strip().lower()

        for movimiento in movimientos:
            codigo = movimiento.get(
                "codigo_producto",
                movimiento.get("codigo", "")
            )
            tipo_movimiento = movimiento.get("tipo", "")

            if (
                codigo_producto is not None
                and codigo != codigo_producto
            ):
                continue

            if (
                tipo is not None
                and tipo_movimiento.strip().lower() != tipo
            ):
                continue

            resultado.append(movimiento.copy())

        return resultado
