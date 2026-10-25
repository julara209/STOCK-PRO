import io
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from consola import menu_reportes
from modelos.producto import Producto


class MovimientoSimulado:
    """Movimiento de mentira: solo necesita 'tipo', 'cantidad' y cómo se imprime."""

    def __init__(self, tipo, cantidad):
        self.tipo = tipo
        self.cantidad = cantidad

    def __str__(self):
        return f"MOVIMIENTO {self.tipo} x{self.cantidad}"


def gestor(productos, movimientos=None):
    datos = {"consultar_productos": lambda: list(productos)}
    if movimientos is not None:
        datos["movimientos"] = movimientos
    return SimpleNamespace(**datos)


def salida(funcion, *args, entradas=()):
    buffer = io.StringIO()
    with patch("builtins.input", side_effect=list(entradas)), redirect_stdout(buffer):
        funcion(*args)
    return buffer.getvalue()


class TestMenuReportes(unittest.TestCase):
    def setUp(self):
        self.productos = [
            Producto("A01", "Arroz", "Granos", 4500, 3),
            Producto("A02", "Fríjol", "Granos", 6000, 0),
            Producto("B01", "Leche", "Lácteos", 3800, 20),
        ]

    def test_resumen_con_datos(self):
        texto = salida(menu_reportes.mostrar_resumen, gestor(self.productos, []))
        self.assertIn("Productos registrados: 3", texto)
        self.assertIn("Arroz", texto)      # stock bajo
        self.assertIn("Fríjol", texto)     # agotado

    def test_resumen_sin_productos_no_falla(self):
        texto = salida(menu_reportes.mostrar_resumen, gestor([], []))
        self.assertIn("No hay productos registrados.", texto)

    def test_agotados_sin_ninguno(self):
        solo_disponibles = [self.productos[2]]
        texto = salida(menu_reportes.mostrar_agotados, gestor(solo_disponibles))
        self.assertIn("No hay productos agotados.", texto)

    def test_stock_bajo_sin_ninguno(self):
        texto = salida(menu_reportes.mostrar_stock_bajo, gestor([self.productos[2]]))
        self.assertIn("No hay productos con existencias bajas.", texto)

    def test_movimientos_vacios(self):
        texto = salida(menu_reportes.mostrar_movimientos, gestor(self.productos, []))
        self.assertIn("No hay movimientos registrados.", texto)

    def test_gestor_sin_historial_se_trata_como_vacio(self):
        texto = salida(menu_reportes.mostrar_movimientos, gestor(self.productos))
        self.assertIn("No hay movimientos registrados.", texto)

    def test_movimientos_filtrados_por_tipo(self):
        movs = [MovimientoSimulado("Entrada", 5), MovimientoSimulado("Salida", 2)]
        texto = salida(menu_reportes.mostrar_movimientos,
                       gestor(self.productos, movs), entradas=["3"])
        self.assertIn("MOVIMIENTO Salida x2", texto)
        self.assertNotIn("MOVIMIENTO Entrada", texto)

    def test_movimientos_todos(self):
        movs = [MovimientoSimulado("Entrada", 5), MovimientoSimulado("Salida", 2)]
        texto = salida(menu_reportes.mostrar_movimientos,
                       gestor(self.productos, movs), entradas=["1"])
        self.assertIn("MOVIMIENTO Entrada x5", texto)
        self.assertIn("MOVIMIENTO Salida x2", texto)

    def test_menu_opcion_invalida_y_volver(self):
        texto = salida(menu_reportes.menu_reportes, gestor(self.productos, []),
                       entradas=["9", "0"])
        self.assertIn("Opción inválida.", texto)


if __name__ == "__main__":
    unittest.main()
