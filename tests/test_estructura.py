import importlib
import unittest

MODULOS = (
    "constantes",
    "almacenamiento",
    "reportes",
    "exportacion",
    "modelos.producto",
    "modelos.usuario",
    "modelos.movimiento",
    "servicios.inventario",
    "servicios.autenticacion",
    "servicios.usuarios",
    "servicios.busqueda",
    "servicios.actualizacion",
    "servicios.salidas",
    "consola.menu_actualizar",
    "consola.menu_agotados",
    "consola.menu_buscar",
    "consola.menu_entrada",
    "consola.menu_exportar",
    "consola.menu_historial",
    "consola.menu_inventario",
    "consola.menu_principal",
    "consola.menu_productos",
    "consola.menu_reportes",
    "consola.menu_salidas",
    "consola.menu_sesion",
    "consola.menu_usuarios",
)


class TestEstructura(unittest.TestCase):
    def test_todos_los_modulos_se_pueden_importar(self):
        for nombre in MODULOS:
            with self.subTest(modulo=nombre):
                importlib.import_module(nombre)


if __name__ == "__main__":
    unittest.main()
