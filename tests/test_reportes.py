import unittest
from types import SimpleNamespace

import reportes
from constantes import STOCK_BAJO, TIPO_ENTRADA, TIPO_SALIDA
from modelos.producto import Producto


def mov(tipo, cantidad):
    """Movimiento simulado: los reportes solo leen 'tipo' y 'cantidad'."""
    return SimpleNamespace(tipo=tipo, cantidad=cantidad)


class TestReportesConDatos(unittest.TestCase):
    def setUp(self):
        self.productos = [
            Producto("B01", "Leche", "Lácteos", 3800, 20),
            Producto("A02", "Fríjol", "Granos", 6000, 0),
            Producto("A01", "Arroz", "Granos", 4500, STOCK_BAJO),
            Producto("C01", "Sal", "Condimentos", 1000, 1),
            Producto("C02", "Azúcar", "Granos", 3000, 0),
        ]
        self.movimientos = [
            mov(TIPO_ENTRADA, 10), mov(TIPO_SALIDA, 4),
            mov(TIPO_SALIDA, 1), mov(TIPO_ENTRADA, 5),
        ]

    def codigos(self, productos):
        return [p.codigo for p in productos]

    def test_agotados_solo_con_cero_y_ordenados(self):
        self.assertEqual(self.codigos(reportes.productos_agotados(self.productos)),
                         ["A02", "C02"])

    def test_stock_bajo_incluye_el_limite_y_excluye_agotados(self):
        self.assertEqual(
            self.codigos(reportes.productos_con_stock_bajo(self.productos)),
            ["A01", "C01"])

    def test_stock_bajo_con_umbral_propio(self):
        self.assertEqual(
            self.codigos(reportes.productos_con_stock_bajo(self.productos, umbral=1)),
            ["C01"])

    def test_producto_sobre_el_umbral_no_es_bajo(self):
        self.assertNotIn("B01", self.codigos(
            reportes.productos_con_stock_bajo(self.productos)))

    def test_resumen_calcula_totales(self):
        r = reportes.resumen_inventario(self.productos, self.movimientos)
        self.assertEqual(r["total_productos"], 5)
        self.assertEqual(r["unidades_totales"], 20 + 0 + STOCK_BAJO + 1 + 0)
        self.assertEqual(r["valor_total"], 3800 * 20 + 4500 * STOCK_BAJO + 1000)

    def test_resumen_cuenta_movimientos(self):
        r = reportes.resumen_inventario(self.productos, self.movimientos)
        self.assertEqual((r["total_entradas"], r["unidades_entradas"]), (2, 15))
        self.assertEqual((r["total_salidas"], r["unidades_salidas"]), (2, 5))

    def test_resumen_incluye_listas_de_alerta(self):
        r = reportes.resumen_inventario(self.productos)
        self.assertEqual(self.codigos(r["agotados"]), ["A02", "C02"])
        self.assertEqual(self.codigos(r["stock_bajo"]), ["A01", "C01"])

    def test_filtrar_movimientos_por_tipo(self):
        entradas = reportes.filtrar_movimientos(self.movimientos, TIPO_ENTRADA)
        self.assertEqual([m.cantidad for m in entradas], [10, 5])
        self.assertEqual(len(reportes.filtrar_movimientos(self.movimientos)), 4)

    def test_filtrar_con_tipo_invalido(self):
        with self.assertRaises(ValueError):
            reportes.filtrar_movimientos(self.movimientos, "Traslado")

    def test_los_reportes_no_modifican_los_datos(self):
        antes = [(p.codigo, p.cantidad) for p in self.productos]
        reportes.resumen_inventario(self.productos, self.movimientos)
        self.assertEqual(antes, [(p.codigo, p.cantidad) for p in self.productos])
        self.assertEqual(len(self.movimientos), 4)


class TestReportesSinDatos(unittest.TestCase):
    def test_resumen_sin_productos_ni_movimientos(self):
        r = reportes.resumen_inventario([], [])
        self.assertEqual((r["total_productos"], r["unidades_totales"], r["valor_total"]),
                         (0, 0, 0))
        self.assertEqual((r["stock_bajo"], r["agotados"]), ([], []))
        self.assertEqual((r["total_entradas"], r["total_salidas"]), (0, 0))

    def test_listas_vacias(self):
        self.assertEqual(reportes.productos_agotados([]), [])
        self.assertEqual(reportes.productos_con_stock_bajo([]), [])
        self.assertEqual(reportes.filtrar_movimientos([]), [])


if __name__ == "__main__":
    unittest.main()
