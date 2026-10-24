import unittest
from unittest.mock import patch

from servicios.actualizacion import ProductoNoEncontradoError
from servicios.inventario import GestorInventario

DATOS = [
    {"codigo": "A01", "nombre": "Arroz", "categoria": "Granos",
     "precio": 4500, "cantidad": 10},
    {"codigo": "B01", "nombre": "Leche", "categoria": "Lácteos",
     "precio": 3800, "cantidad": 20},
]


class TestGestorActualizar(unittest.TestCase):
    """Prueba GestorInventario.actualizar_producto sin tocar el JSON real."""

    def setUp(self):
        with patch("almacenamiento.cargar", return_value=[dict(d) for d in DATOS]):
            self.gestor = GestorInventario()

    def producto(self, codigo):
        return next(p for p in self.gestor.productos if p.codigo == codigo)

    def test_actualizacion_valida_cambia_y_guarda(self):
        with patch("almacenamiento.guardar") as guardar:
            self.gestor.actualizar_producto("A01", precio=5000, entrada=5)
        self.assertEqual(self.producto("A01").precio, 5000)
        self.assertEqual(self.producto("A01").cantidad, 15)
        guardar.assert_called_once()
        guardado = {d["codigo"]: d for d in guardar.call_args[0][0]}
        self.assertEqual(guardado["A01"]["cantidad"], 15)
        self.assertEqual(guardado["B01"]["cantidad"], 20)

    def test_producto_inexistente_no_guarda(self):
        with patch("almacenamiento.guardar") as guardar:
            with self.assertRaises(ProductoNoEncontradoError):
                self.gestor.actualizar_producto("ZZZ", precio=100)
            guardar.assert_not_called()

    def test_rechazo_no_modifica_ni_guarda(self):
        with patch("almacenamiento.guardar") as guardar:
            with self.assertRaises(ValueError):
                self.gestor.actualizar_producto("A01", nombre=" ", precio=9999)
            guardar.assert_not_called()
        self.assertEqual((self.producto("A01").nombre, self.producto("A01").precio),
                         ("Arroz", 4500))

    def test_si_falla_el_guardado_no_cambia_la_memoria(self):
        with patch("almacenamiento.guardar", side_effect=OSError("disco lleno")):
            with self.assertRaises(OSError):
                self.gestor.actualizar_producto("A01", precio=5000)
        self.assertEqual(self.producto("A01").precio, 4500)

    def test_mantiene_el_orden_y_no_toca_otros_productos(self):
        with patch("almacenamiento.guardar"):
            self.gestor.actualizar_producto("A01", entrada=1)
        self.assertEqual([p.codigo for p in self.gestor.productos], ["A01", "B01"])
        self.assertEqual(self.producto("B01").cantidad, 20)


if __name__ == "__main__":
    unittest.main()
