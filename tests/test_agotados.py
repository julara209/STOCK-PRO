import unittest
from unittest.mock import patch

from consola.menu_agotados import mostrar_agotados
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


class TestProductosAgotados(unittest.TestCase):
    def setUp(self):
        self.agotado1 = Producto("A001", "Arroz", "Granos", 3500, 0)
        self.disponible = Producto("B002", "Aceite", "Aceites", 9000, 10)
        self.agotado2 = Producto("C003", "Sal", "Condimentos", 1200, 0)
        self.poco = Producto("D004", "Azúcar", "Granos", 2800, 1)
        self.gestor = crear_gestor(
            [self.agotado1, self.disponible, self.agotado2, self.poco]
        )

    def test_solo_existencias_en_cero(self):
        self.assertEqual(self.gestor.productos_agotados(),
                         [self.agotado1, self.agotado2])

    def test_no_incluye_disponibles(self):
        agotados = self.gestor.productos_agotados()
        self.assertNotIn(self.disponible, agotados)
        self.assertNotIn(self.poco, agotados)

    def test_sin_agotados_devuelve_lista_vacia(self):
        self.assertEqual(crear_gestor([self.disponible]).productos_agotados(), [])

    def test_inventario_vacio(self):
        self.assertEqual(crear_gestor([]).productos_agotados(), [])

    def test_consulta_no_modifica_existencias(self):
        antes = [(p.codigo, p.cantidad) for p in self.gestor.productos]
        self.gestor.productos_agotados()
        self.assertEqual([(p.codigo, p.cantidad) for p in self.gestor.productos], antes)


class TestPantallaAgotados(unittest.TestCase):
    def test_muestra_codigo_nombre_y_categoria(self):
        log = []
        mostrar_agotados(crear_gestor([Producto("A001", "Arroz", "Granos", 3500, 0)]),
                         log.append)
        texto = "\n".join(log)
        for dato in ("Código", "Nombre", "Categoría", "A001", "Arroz", "Granos"):
            self.assertIn(dato, texto)

    def test_informa_cuando_no_hay_agotados(self):
        log = []
        mostrar_agotados(crear_gestor([Producto("B002", "Aceite", "Aceites", 9000, 5)]),
                         log.append)
        self.assertTrue(any("No hay productos agotados" in m for m in log))


class TestMenuEmpleado(unittest.TestCase):
    def test_empleado_consulta_agotados_desde_su_menu(self):
        usuarios = []
        admin = registrar_usuario(usuarios, "admin", "Segura123", ROL_ADMINISTRADOR)
        registrar_usuario(usuarios, "ana", "Segura123", ROL_EMPLEADO, admin)
        gestor = crear_gestor([Producto("A001", "Arroz", "Granos", 3500, 0)])
        log = []
        respuestas = iter(["ana", "Segura123", "2", "0"])
        flujo_sesion(
            Autenticacion(usuarios),
            {"consultar_agotados": lambda: mostrar_agotados(gestor, log.append)},
            lambda _="": next(respuestas), log.append,
        )
        self.assertTrue(any("A001" in m for m in log))


if __name__ == "__main__":
    unittest.main()