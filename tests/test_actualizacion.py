import unittest

from modelos.producto import Producto
from servicios.actualizacion import construir_producto_actualizado


class TestConstruirProductoActualizado(unittest.TestCase):
    def setUp(self):
        self.original = Producto("A01", "Arroz Diana", "Granos", 4500, 10)

    def datos(self, p):
        return (p.codigo, p.nombre, p.categoria, p.precio, p.cantidad)

    def test_actualiza_precio(self):
        nuevo = construir_producto_actualizado(self.original, precio=5000)
        self.assertEqual(nuevo.precio, 5000)

    def test_actualiza_nombre_y_categoria(self):
        nuevo = construir_producto_actualizado(
            self.original, nombre="Arroz Roa", categoria="Cereales")
        self.assertEqual((nuevo.nombre, nuevo.categoria), ("Arroz Roa", "Cereales"))

    def test_entrada_aumenta_existencias(self):
        nuevo = construir_producto_actualizado(self.original, entrada=5)
        self.assertEqual(nuevo.cantidad, 15)

    def test_campos_no_indicados_se_conservan(self):
        nuevo = construir_producto_actualizado(self.original, precio=5000)
        self.assertEqual(self.datos(nuevo), ("A01", "Arroz Diana", "Granos", 5000, 10))

    def test_no_modifica_el_original(self):
        construir_producto_actualizado(self.original, precio=5000, entrada=5)
        self.assertEqual(self.datos(self.original),
                         ("A01", "Arroz Diana", "Granos", 4500, 10))

    def test_precio_cero_rechazado(self):
        with self.assertRaises(ValueError):
            construir_producto_actualizado(self.original, precio=0)

    def test_precio_negativo_rechazado(self):
        with self.assertRaises(ValueError):
            construir_producto_actualizado(self.original, precio=-10)

    def test_nombre_vacio_rechazado(self):
        with self.assertRaises(ValueError):
            construir_producto_actualizado(self.original, nombre="   ")

    def test_entrada_cero_o_negativa_rechazada(self):
        for valor in (-3, 0):
            with self.subTest(entrada=valor):
                with self.assertRaises(ValueError):
                    construir_producto_actualizado(self.original, entrada=valor)

    def test_entrada_decimal_rechazada(self):
        with self.assertRaises(ValueError):
            construir_producto_actualizado(self.original, entrada=2.5)

    def test_rechazo_parcial_no_cambia_nada(self):
        # precio válido + nombre vacío: se rechaza todo
        with self.assertRaises(ValueError):
            construir_producto_actualizado(self.original, nombre=" ", precio=9999)
        self.assertEqual(self.datos(self.original),
                         ("A01", "Arroz Diana", "Granos", 4500, 10))


if __name__ == "__main__":
    unittest.main()
