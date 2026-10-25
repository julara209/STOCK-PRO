import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from consola import menu_exportar
from modelos.producto import Producto


def gestor(productos, movimientos=None):
    datos = {"consultar_productos": lambda: list(productos)}
    if movimientos is not None:
        datos["movimientos"] = movimientos
    return SimpleNamespace(**datos)


class TestMenuExportar(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.carpeta = Path(carpeta.name) / "exportaciones"
        parche = patch("exportacion.CARPETA_EXPORTACIONES", self.carpeta)
        parche.start()
        self.addCleanup(parche.stop)
        self.productos = [Producto("A01", "Arroz", "Granos", 4500, 10)]

    def ejecutar(self, gestor_, entradas):
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=entradas), redirect_stdout(buffer):
            menu_exportar.menu_exportar(gestor_)
        return buffer.getvalue()

    def test_exporta_el_inventario_y_avisa_la_ruta(self):
        texto = self.ejecutar(gestor(self.productos, []), ["1", "0"])
        self.assertIn("Archivo generado:", texto)
        self.assertIn("Registros exportados: 1", texto)
        self.assertEqual(len(list(self.carpeta.glob("inventario_*.csv"))), 1)

    def test_sin_productos_informa_y_no_genera_archivo(self):
        texto = self.ejecutar(gestor([], []), ["1", "0"])
        self.assertIn("No se generó ningún archivo: No hay productos para exportar.", texto)
        self.assertFalse(self.carpeta.exists())

    def test_sin_movimientos_informa_y_no_genera_archivo(self):
        texto = self.ejecutar(gestor(self.productos, []), ["2", "0"])
        self.assertIn("No hay movimientos para exportar.", texto)
        self.assertFalse(self.carpeta.exists())

    def test_gestor_sin_historial_se_trata_como_vacio(self):
        texto = self.ejecutar(gestor(self.productos), ["2", "0"])
        self.assertIn("No hay movimientos para exportar.", texto)

    def test_error_de_escritura_no_cierra_el_programa(self):
        with patch("exportacion.exportar_inventario_csv",
                   side_effect=OSError("sin permisos")):
            texto = self.ejecutar(gestor(self.productos, []), ["1", "0"])
        self.assertIn("Error al exportar el inventario: sin permisos", texto)

    def test_opcion_invalida_y_volver(self):
        texto = self.ejecutar(gestor(self.productos, []), ["9", "0"])
        self.assertIn("Opción inválida.", texto)


if __name__ == "__main__":
    unittest.main()
