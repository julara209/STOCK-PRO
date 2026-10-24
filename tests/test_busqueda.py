import unittest

from modelos.producto import Producto
from servicios.busqueda import buscar_productos


class TestBuscarProductos(unittest.TestCase):
    def setUp(self):
        self.productos = [
            Producto("A01", "Arroz Diana", "Granos", 4500, 10),
            Producto("A02", "Fríjol", "Granos", 6000, 0),
            Producto("B01", "Leche", "Lácteos", 3800, 20),
        ]

    def codigos(self, **criterios):
        return [p.codigo for p in buscar_productos(self.productos, **criterios)]

    def test_busca_por_codigo_exacto(self):
        self.assertEqual(self.codigos(codigo="A01"), ["A01"])

    def test_codigo_parcial_no_coincide(self):
        self.assertEqual(self.codigos(codigo="A0"), [])

    def test_nombre_sin_distinguir_mayusculas(self):
        self.assertEqual(self.codigos(nombre="aRRoz"), ["A01"])

    def test_nombre_parcial(self):
        self.assertEqual(self.codigos(nombre="che"), ["B01"])

    def test_filtra_por_categoria(self):
        self.assertEqual(self.codigos(categoria="granos"), ["A01", "A02"])

    def test_criterios_combinados(self):
        self.assertEqual(self.codigos(categoria="Granos", nombre="fr"), ["A02"])

    def test_sin_resultados_devuelve_lista_vacia(self):
        self.assertEqual(self.codigos(nombre="zzz"), [])

    def test_sin_criterios_es_rechazado(self):
        with self.assertRaises(ValueError):
            buscar_productos(self.productos)

    def test_buscar_no_modifica_inventario(self):
        antes = [(p.codigo, p.nombre, p.precio, p.cantidad) for p in self.productos]
        buscar_productos(self.productos, nombre="a")
        buscar_productos(self.productos, categoria="granos")
        despues = [(p.codigo, p.nombre, p.precio, p.cantidad) for p in self.productos]
        self.assertEqual(antes, despues)

    def test_inventario_vacio(self):
        self.assertEqual(buscar_productos([], nombre="a"), [])


if __name__ == "__main__":
    unittest.main()
