import unittest
from unittest.mock import patch

from servicios.inventario import GestorInventario

PRODUCTOS = [
    {"codigo": "A01", "nombre": "Arroz", "categoria": "Granos",
     "precio": 4500, "cantidad": 10},
    {"codigo": "B01", "nombre": "Leche", "categoria": "Lácteos",
     "precio": 3800, "cantidad": 20},
]


class TestGestorSalida(unittest.TestCase):
    """Prueba GestorInventario.registrar_salida sin tocar los JSON reales."""

    def setUp(self):
        with patch("almacenamiento.cargar", return_value=[dict(p) for p in PRODUCTOS]), \
             patch("almacenamiento.cargar_movimientos", return_value=[]):
            self.gestor = GestorInventario()

    def stock(self, codigo):
        return next(p for p in self.gestor.productos if p.codigo == codigo).cantidad

    def intentar_rechazada(self, *args):
        with patch("almacenamiento.guardar") as g1, \
             patch("almacenamiento.guardar_movimientos") as g2:
            with self.assertRaises(ValueError):
                self.gestor.registrar_salida(*args)
            g1.assert_not_called()
            g2.assert_not_called()
        self.assertEqual(self.stock("A01"), 10)
        self.assertEqual(self.gestor.movimientos, [])

    def test_salida_valida_descuenta_y_registra_el_movimiento(self):
        with patch("almacenamiento.guardar") as g1, \
             patch("almacenamiento.guardar_movimientos") as g2:
            mov = self.gestor.registrar_salida("A01", 4, "maria")
        self.assertEqual(self.stock("A01"), 6)
        self.assertEqual(self.stock("B01"), 20)
        self.assertEqual(len(self.gestor.movimientos), 1)
        self.assertEqual((mov.tipo, mov.codigo_producto, mov.cantidad, mov.usuario),
                         ("Salida", "A01", 4, "maria"))
        guardado = {d["codigo"]: d["cantidad"] for d in g1.call_args[0][0]}
        self.assertEqual(guardado, {"A01": 6, "B01": 20})
        self.assertEqual(g2.call_args[0][0][0]["id_movimiento"], mov.id_movimiento)

    def test_ids_unicos_y_consecutivos(self):
        with patch("almacenamiento.guardar"), patch("almacenamiento.guardar_movimientos"):
            m1 = self.gestor.registrar_salida("A01", 1, "maria")
            m2 = self.gestor.registrar_salida("B01", 2, "maria")
        self.assertEqual((m1.id_movimiento, m2.id_movimiento), ("MOV-0001", "MOV-0002"))

    def test_producto_inexistente_es_rechazado(self):
        self.intentar_rechazada("ZZZ", 1, "maria")

    def test_cantidad_mayor_a_existencias_es_rechazada(self):
        self.intentar_rechazada("A01", 11, "maria")

    def test_cantidad_cero_o_negativa_es_rechazada(self):
        self.intentar_rechazada("A01", 0, "maria")
        self.intentar_rechazada("A01", -3, "maria")

    def test_usuario_vacio_es_rechazado(self):
        self.intentar_rechazada("A01", 1, "  ")

    def test_si_falla_el_historial_se_revierten_las_existencias(self):
        with patch("almacenamiento.guardar") as g1, \
             patch("almacenamiento.guardar_movimientos", side_effect=OSError("disco lleno")):
            with self.assertRaises(OSError):
                self.gestor.registrar_salida("A01", 4, "maria")
        # primera llamada: stock nuevo; segunda: se restauran los datos anteriores
        self.assertEqual(g1.call_count, 2)
        restaurado = {d["codigo"]: d["cantidad"] for d in g1.call_args[0][0]}
        self.assertEqual(restaurado["A01"], 10)
        self.assertEqual(self.stock("A01"), 10)
        self.assertEqual(self.gestor.movimientos, [])

    def test_si_falla_el_guardado_de_productos_no_cambia_nada(self):
        with patch("almacenamiento.guardar", side_effect=OSError("sin permisos")), \
             patch("almacenamiento.guardar_movimientos") as g2:
            with self.assertRaises(OSError):
                self.gestor.registrar_salida("A01", 4, "maria")
            g2.assert_not_called()
        self.assertEqual(self.stock("A01"), 10)
        self.assertEqual(self.gestor.movimientos, [])


if __name__ == "__main__":
    unittest.main()
