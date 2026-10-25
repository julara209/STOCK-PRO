"""GestorInventario: reglas de negocio y gestión de la colección de productos
y movimientos (registrar, actualizar, buscar, entradas, salidas e historial)."""

import almacenamiento
from constantes import TIPO_ENTRADA, TIPO_SALIDA
from modelos.movimiento import Movimiento
from modelos.producto import Producto
from servicios.busqueda import buscar_productos as _buscar
from servicios.salidas import calcular_salida
from servicios.actualizacion import (
    ProductoNoEncontradoError,
    construir_producto_actualizado,
)


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

    def buscar_productos(self, codigo=None, nombre=None, categoria=None):
        return _buscar(self.productos, codigo, nombre, categoria)

    def registrar_entrada(self, codigo, cantidad, usuario_responsable):
        """Suma existencias y registra la entrada en el historial."""
        if (
            not isinstance(usuario_responsable, str)
            or not usuario_responsable.strip()
        ):
            raise ValueError(
                "El usuario responsable no puede estar vacío."
            )

        codigo = codigo.strip()

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ValueError(
                "La cantidad recibida debe ser un entero mayor que cero."
            )

        posicion = None
        for i, producto in enumerate(self.productos):
            if producto.codigo == codigo:
                posicion = i
                break

        if posicion is None:
            raise ProductoNoEncontradoError(
                f"El producto '{codigo}' no existe."
            )

        producto = self.productos[posicion]

        # Si algún dato es inválido, Movimiento lanza ValueError y no se
        # modifica ni la memoria ni los archivos.
        movimiento = Movimiento(
            f"MOV-{len(self.movimientos) + 1:04d}",
            TIPO_ENTRADA,
            codigo,
            cantidad,
            usuario_responsable,
        )

        actualizado = Producto(
            producto.codigo,
            producto.nombre,
            producto.categoria,
            producto.precio,
            producto.cantidad + cantidad,
        )

        nuevos_productos = self.productos.copy()
        nuevos_productos[posicion] = actualizado
        nuevos_movimientos = self.movimientos + [movimiento]

        datos_anteriores = [p.to_dict() for p in self.productos]

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
        return actualizado

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
        # Si algo falla, no se modifica ni la memoria ni los archivos.
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

            copia = movimiento.copy()

            # Compatibilidad con el formato anterior de HU-012: el historial
            # ahora guarda "usuario" y no guarda "nombre_producto".
            copia.setdefault("usuario_responsable", copia.get("usuario", ""))

            if "nombre_producto" not in copia:
                producto = self.buscar_producto(codigo) if codigo else None
                copia["nombre_producto"] = (
                    producto.nombre if producto is not None else ""
                )

            resultado.append(copia)

        return resultado