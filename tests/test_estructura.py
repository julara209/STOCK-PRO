import importlib
import unittest

MODULOS = (
    "constantes",
    "almacenamiento",
    "reportes",
    "modelos.producto",
    "modelos.usuario",
    "modelos.movimiento",
    "servicios.inventario",
    "servicios.autenticacion",
    "consola.menu_productos",
    "consola.menu_usuarios",
    "consola.menu_principal",
)


class TestEstructura(unittest.TestCase):
    def test_todos_los_modulos_se_pueden_importar(self):
        for nombre in MODULOS:
            with self.subTest(modulo=nombre):
                importlib.import_module(nombre)


if __name__ == "__main__":
    unittest.main()
