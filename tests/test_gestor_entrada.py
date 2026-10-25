
import unittest
from unittest.mock import patch

from servicios.actualizacion import ProductoNoEncontradoError
from servicios.inventario import GestorInventario


DATOS = [
    {
        "codigo": "A01",
        "nombre": "Arroz",
        "categoria": "Granos",
        "precio": 4500,
        "cantidad": 10
    },
    {
        "codigo": "B01",
        "nombre": "Leche",
        "categoria": "Lácteos",
        "precio": 3800,
        "cantidad": 20
    }
]


class TestGestorEntrada(unittest.TestCase):
    """Pruebas para registrar entradas de mercancía."""

    def setUp(self):
        with patch(
            "almacenamiento.cargar",
            return_value=[dict(d) for d in DATOS]
        ):
            self.gestor = GestorInventario()

    def producto(self, codigo):
        return next(
            p for p in self.gestor.productos
            if p.codigo == codigo
        )

    def test_entrada_valida_suma_existencias_y_guarda(self):
        with (
            patch("almacenamiento.guardar") as guardar,
            patch(
                "almacenamiento.cargar_movimientos",
                return_value=[]
            ),
            patch(
                "almacenamiento.guardar_movimientos"
            ) as guardar_movimientos
        ):
            producto = self.gestor.registrar_entrada(
                "A01", 5, "empleado1"
            )

        self.assertEqual(producto.cantidad, 15)
        self.assertEqual(self.producto("A01").cantidad, 15)
        self.assertEqual(self.producto("B01").cantidad, 20)

        guardar.assert_called_once()
        datos_guardados = guardar.call_args[0][0]
        arroz = next(
            d for d in datos_guardados
            if d["codigo"] == "A01"
        )
        self.assertEqual(arroz["cantidad"], 15)

        guardar_movimientos.assert_called_once()
        historial = guardar_movimientos.call_args[0][0]

        self.assertEqual(len(historial), 1)
        self.assertEqual(historial[0]["tipo"], "Entrada")
        self.assertEqual(historial[0]["codigo_producto"], "A01")
        self.assertEqual(historial[0]["id_movimiento"], "MOV-0001")
        self.assertEqual(historial[0]["cantidad"], 5)
        self.assertEqual(
            historial[0]["usuario"], "empleado1"
        )
        self.assertIn("fecha", historial[0])

    def test_producto_inexistente_no_modifica_inventario(self):
        with (
            patch("almacenamiento.guardar") as guardar,
            patch(
                "almacenamiento.cargar_movimientos",
                return_value=[]
            ),
            patch(
                "almacenamiento.guardar_movimientos"
            ) as guardar_movimientos
        ):
            with self.assertRaises(ProductoNoEncontradoError):
                self.gestor.registrar_entrada(
                    "ZZZ", 5, "empleado1"
                )

        guardar.assert_not_called()
        guardar_movimientos.assert_not_called()
        self.assertEqual(self.producto("A01").cantidad, 10)

    def test_cantidades_invalidas_son_rechazadas(self):
        cantidades = [0, -1, 1.5, "cinco", None, True]

        for cantidad in cantidades:
            with self.subTest(cantidad=cantidad):
                with (
                    patch("almacenamiento.guardar") as guardar,
                    patch(
                        "almacenamiento.cargar_movimientos",
                        return_value=[]
                    ),
                    patch(
                        "almacenamiento.guardar_movimientos"
                    ) as guardar_movimientos
                ):
                    with self.assertRaises(ValueError):
                        self.gestor.registrar_entrada(
                            "A01", cantidad, "empleado1"
                        )

                guardar.assert_not_called()
                guardar_movimientos.assert_not_called()
                self.assertEqual(
                    self.producto("A01").cantidad, 10
                )

    def test_usuario_vacio_es_rechazado(self):
        with (
            patch("almacenamiento.guardar") as guardar,
            patch(
                "almacenamiento.cargar_movimientos",
                return_value=[]
            ),
            patch(
                "almacenamiento.guardar_movimientos"
            ) as guardar_movimientos
        ):
            with self.assertRaises(ValueError):
                self.gestor.registrar_entrada("A01", 5, " ")

        guardar.assert_not_called()
        guardar_movimientos.assert_not_called()
        self.assertEqual(self.producto("A01").cantidad, 10)

    def test_si_falla_guardar_inventario_no_cambia_memoria(self):
        with (
            patch(
                "almacenamiento.guardar",
                side_effect=OSError("disco lleno")
            ),
            patch(
                "almacenamiento.cargar_movimientos",
                return_value=[]
            ),
            patch(
                "almacenamiento.guardar_movimientos"
            ) as guardar_movimientos
        ):
            with self.assertRaises(OSError):
                self.gestor.registrar_entrada(
                    "A01", 5, "empleado1"
                )

        self.assertEqual(self.producto("A01").cantidad, 10)
        guardar_movimientos.assert_not_called()


if __name__ == "__main__":
    unittest.main()
