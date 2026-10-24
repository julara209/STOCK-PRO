import unittest

from constantes import TIPO_ENTRADA, TIPO_SALIDA
from modelos.movimiento import Movimiento


class TestMovimiento(unittest.TestCase):
    def crear(self, **cambios):
        datos = dict(id_movimiento="MOV-0001", tipo=TIPO_SALIDA,
                     codigo_producto="A01", cantidad=3, usuario="maria")
        datos.update(cambios)
        return Movimiento(**datos)

    def test_movimiento_valido(self):
        m = self.crear()
        self.assertEqual((m.tipo, m.codigo_producto, m.cantidad, m.usuario),
                         (TIPO_SALIDA, "A01", 3, "maria"))

    def test_registra_la_fecha_automaticamente(self):
        self.assertRegex(self.crear().fecha, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

    def test_acepta_tipo_entrada(self):
        self.assertEqual(self.crear(tipo=TIPO_ENTRADA).tipo, TIPO_ENTRADA)

    def test_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.crear(tipo="Traslado")

    def test_cantidad_invalida(self):
        for valor in (0, -1, 2.5, "3", True):
            with self.subTest(cantidad=valor):
                with self.assertRaises(ValueError):
                    self.crear(cantidad=valor)

    def test_usuario_obligatorio(self):
        for valor in ("", "   ", None):
            with self.subTest(usuario=valor):
                with self.assertRaises(ValueError):
                    self.crear(usuario=valor)

    def test_producto_y_id_obligatorios(self):
        with self.assertRaises(ValueError):
            self.crear(codigo_producto=" ")
        with self.assertRaises(ValueError):
            self.crear(id_movimiento="")

    def test_to_dict_y_from_dict(self):
        original = self.crear()
        copia = Movimiento.from_dict(original.to_dict())
        self.assertEqual(copia.to_dict(), original.to_dict())


if __name__ == "__main__":
    unittest.main()
