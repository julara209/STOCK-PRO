import unittest
from unittest.mock import patch

from servicios.inventario import GestorInventario


class TestConsultarHistorial(unittest.TestCase):

    def setUp(self):
        self.movimientos = [
            {
                "id_movimiento": "MOV-001",
                "tipo": "Entrada",
                "codigo_producto": "P001",
                "nombre_producto": "Teclado",
                "cantidad": 10,
                "fecha": "2026-10-20T10:00:00",
                "usuario": "Administrador"
            },
            {
                "id_movimiento": "MOV-002",
                "tipo": "Salida",
                "codigo_producto": "P001",
                "nombre_producto": "Teclado",
                "cantidad": 2,
                "fecha": "2026-10-21T11:00:00",
                "usuario": "Empleado"
            },
            {
                "id_movimiento": "MOV-003",
                "tipo": "Entrada",
                "codigo_producto": "P002",
                "nombre_producto": "Mouse",
                "cantidad": 5,
                "fecha": "2026-10-22T12:00:00",
                "usuario": "Administrador"
            }
        ]

        self.patch_cargar = patch(
            "servicios.inventario.almacenamiento.cargar",
            return_value=[]
        )
        self.patch_movimientos = patch(
            "servicios.inventario.almacenamiento.cargar_movimientos",
            return_value=self.movimientos
        )

        self.patch_cargar.start()
        self.mock_movimientos = self.patch_movimientos.start()
        self.addCleanup(self.patch_cargar.stop)
        self.addCleanup(self.patch_movimientos.stop)

        self.inventario = GestorInventario()

    def test_consultar_historial_completo(self):
        resultado = self.inventario.consultar_historial_movimientos()

        self.assertEqual(len(resultado), 3)
        self.assertEqual(resultado[0]["id_movimiento"], "MOV-001")
        self.assertEqual(resultado[1]["tipo"], "Salida")

    def test_filtrar_por_producto(self):
        resultado = self.inventario.consultar_historial_movimientos(
            codigo_producto="P001"
        )

        self.assertEqual(len(resultado), 2)

        for movimiento in resultado:
            self.assertEqual(movimiento["codigo_producto"], "P001")

    def test_filtrar_por_tipo(self):
        resultado = self.inventario.consultar_historial_movimientos(
            tipo="Entrada"
        )

        self.assertEqual(len(resultado), 2)

        for movimiento in resultado:
            self.assertEqual(movimiento["tipo"], "Entrada")

    def test_filtrar_por_producto_y_tipo(self):
        resultado = self.inventario.consultar_historial_movimientos(
            codigo_producto="P001",
            tipo="Salida"
        )

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id_movimiento"], "MOV-002")

    def test_sin_movimientos(self):
        self.mock_movimientos.return_value = []

        resultado = self.inventario.consultar_historial_movimientos()

        self.assertEqual(resultado, [])

    def test_consulta_no_modifica_los_datos(self):
        movimientos_originales = [
            movimiento.copy() for movimiento in self.movimientos
        ]
        productos_originales = self.inventario.productos.copy()

        self.inventario.consultar_historial_movimientos(
            codigo_producto="P001"
        )

        self.assertEqual(self.movimientos, movimientos_originales)
        self.assertEqual(
            self.inventario.productos,
            productos_originales
        )

    def test_movimientos_tienen_identificadores_unicos(self):
        identificadores = [
            movimiento["id_movimiento"]
            for movimiento in self.movimientos
        ]

        self.assertEqual(
            len(identificadores),
            len(set(identificadores))
        )


if __name__ == "__main__":
    unittest.main()