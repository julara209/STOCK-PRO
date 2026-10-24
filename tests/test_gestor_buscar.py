import unittest
from unittest.mock import patch

from servicios.inventario import GestorInventario


class TestGestorBuscar(unittest.TestCase):
    """Prueba GestorInventario.buscar_productos sin tocar data/inventario.json."""

    def setUp(self):
        datos = [
            {"codigo": "A01", "nombre": "Arroz", "categoria": "Granos",
             "precio": 4500, "cantidad": 10},
            {"codigo": "B01", "nombre": "Leche", "categoria": "Lácteos",
             "precio": 3800, "cantidad": 20},
        ]
        with patch("almacenamiento.cargar", return_value=datos):
            self.gestor = GestorInventario()

    def test_buscar_por_categoria(self):
        r = self.gestor.buscar_productos(categoria="lácteos")
        self.assertEqual([p.codigo for p in r], ["B01"])

    def test_buscar_no_guarda_en_disco(self):
        with patch("almacenamiento.guardar") as guardar:
            self.gestor.buscar_productos(nombre="arroz")
            guardar.assert_not_called()

    def test_buscar_sin_resultados(self):
        self.assertEqual(self.gestor.buscar_productos(nombre="zzz"), [])


if __name__ == "__main__":
    unittest.main()
