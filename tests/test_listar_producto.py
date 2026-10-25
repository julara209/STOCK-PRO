import unittest
from unittest.mock import patch

from consola.menu_inventario import mostrar_inventario
from consola.menu_sesion import flujo_sesion
from modelos.producto import Producto
from modelos.usuario import ROL_ADMINISTRADOR, ROL_EMPLEADO
from servicios.autenticacion import Autenticacion
from servicios.inventario import GestorInventario
from servicios.usuarios import registrar_usuario


def crear_gestor(productos):
    """GestorInventario en memoria: no lee ni escribe los archivos reales."""
    with patch("almacenamiento.cargar", return_value=[]), \
         patch("almacenamiento.cargar_movimientos", return_value=[]):
        gestor = GestorInventario()
    gestor.productos = list(productos)
    return gestor


class TestListarProductos(unittest.TestCase):
    def setUp(self):
        self.arroz = Producto("A001", "Arroz", "Granos", 3500, 10)
        self.sal = Producto("C003", "Sal", "Condimentos", 1200, 4)
        self.gestor = crear_gestor([self.arroz, self.sal])

    def test_incluye_todos_los_productos_registrados(self):
        self.assertEqual(self.gestor.listar_productos(), [self.arroz, self.sal])

    def test_sin_productos_devuelve_lista_vacia(self):
        self.assertEqual(crear_gestor([]).listar_productos(), [])

    def test_refleja_entradas_y_salidas(self):
        with patch("almacenamiento.guardar"), \
             patch("almacenamiento.guardar_movimientos"):
            self.gestor.registrar_entrada("A001", 5, "ana")
            self.gestor.registrar_salida("A001", 3, "ana")
        arroz = next(p for p in self.gestor.listar_productos() if p.codigo == "A001")
        self.assertEqual(arroz.cantidad, 12)

    def test_consulta_no_modifica_el_inventario(self):
        antes = [(p.codigo, p.cantidad) for p in self.gestor.productos]
        self.gestor.listar_productos().clear()   # alterar el resultado no afecta al gestor
        self.assertEqual([(p.codigo, p.cantidad) for p in self.gestor.productos], antes)
        self.assertEqual(len(self.gestor.productos), 2)


class TestPantallaInventario(unittest.TestCase):
    def test_muestra_codigo_nombre_categoria_precio_y_existencias(self):
        log = []
        mostrar_inventario(crear_gestor([Producto("A001", "Arroz", "Granos", 3500, 10)]),
                           log.append)
        texto = "\n".join(log)
        for dato in ("Código", "Nombre", "Categoría", "Precio", "Existencias",
                     "A001", "Arroz", "Granos", "$3,500.00", "10"):
            self.assertIn(dato, texto)

    def test_mensaje_cuando_no_hay_productos(self):
        log = []
        mostrar_inventario(crear_gestor([]), log.append)
        self.assertTrue(any("No hay productos registrados" in m for m in log))


class TestMenusAmbosRoles(unittest.TestCase):
    def _consultar_como(self, nombre, tecla):
        usuarios = []
        admin = registrar_usuario(usuarios, "admin", "Segura123", ROL_ADMINISTRADOR)
        registrar_usuario(usuarios, "ana", "Segura123", ROL_EMPLEADO, admin)
        gestor = crear_gestor([Producto("A001", "Arroz", "Granos", 3500, 10)])
        log = []
        respuestas = iter([nombre, "Segura123", tecla, "0"])
        flujo_sesion(
            Autenticacion(usuarios),
            {"consultar_inventario": lambda: mostrar_inventario(gestor, log.append)},
            lambda _="": next(respuestas), log.append,
        )
        return "\n".join(log)

    def test_administrador_consulta_inventario(self):
        self.assertIn("A001", self._consultar_como("admin", "4"))

    def test_empleado_consulta_inventario(self):
        self.assertIn("A001", self._consultar_como("ana", "3"))


if __name__ == "__main__":
    unittest.main()