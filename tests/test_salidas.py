import unittest

from modelos.producto import Producto
from servicios.salidas import calcular_salida


class TestCalcularSalida(unittest.TestCase):
    def setUp(self):
        self.producto = Producto("A01", "Arroz", "Granos", 4500, 10)

    def test_descuenta_la_cantidad(self):
        self.assertEqual(calcular_salida(self.producto, 4).cantidad, 6)

    def test_permite_retirar_todas_las_existencias(self):
        self.assertEqual(calcular_salida(self.producto, 10).cantidad, 0)

    def test_no_modifica_el_original(self):
        calcular_salida(self.producto, 4)
        self.assertEqual(self.producto.cantidad, 10)

    def test_conserva_los_demas_datos(self):
        nuevo = calcular_salida(self.producto, 4)
        self.assertEqual((nuevo.codigo, nuevo.nombre, nuevo.categoria, nuevo.precio),
                         ("A01", "Arroz", "Granos", 4500.0))

    def test_cantidad_superior_a_las_existencias(self):
        with self.assertRaises(ValueError) as contexto:
            calcular_salida(self.producto, 11)
        self.assertIn("insuficientes", str(contexto.exception))

    def test_cantidad_invalida(self):
        for valor in (0, -2, 1.5, "2", True):
            with self.subTest(cantidad=valor):
                with self.assertRaises(ValueError):
                    calcular_salida(self.producto, valor)


if __name__ == "__main__":
    unittest.main()
