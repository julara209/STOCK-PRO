import unittest

import constantes


class TestConstantes(unittest.TestCase):
    def test_stock_bajo_es_positivo(self):
        self.assertGreater(constantes.STOCK_BAJO, 0)

    def test_roles_validos(self):
        self.assertIn(constantes.ROL_ADMINISTRADOR, constantes.ROLES_VALIDOS)
        self.assertIn(constantes.ROL_EMPLEADO, constantes.ROLES_VALIDOS)


if __name__ == "__main__":
    unittest.main()