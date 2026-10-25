import csv
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import exportacion
from modelos.producto import Producto


def leer_csv(ruta):
    with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
        return list(csv.reader(archivo))


def movimiento(id_, fecha, tipo, codigo, cantidad, usuario):
    """Movimiento simulado: solo se leen estos atributos."""
    return SimpleNamespace(id_movimiento=id_, fecha=fecha, tipo=tipo,
                           codigo_producto=codigo, cantidad=cantidad,
                           usuario=usuario)


class PruebaBase(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.carpeta = Path(carpeta.name) / "exportaciones"   # aún no existe
        self.ahora = datetime(2026, 10, 24, 22, 41, 5)


class TestExportarInventario(PruebaBase):
    def setUp(self):
        super().setUp()
        self.productos = [
            Producto("B01", "Leche", "Lácteos", 3800, 20),
            Producto("A02", "Fríjol", "Granos", 6000, 0),
            Producto("A01", "Arroz", "Granos", 4500, 10),
        ]

    def test_genera_encabezado_y_filas_ordenadas_por_codigo(self):
        ruta = exportacion.exportar_inventario_csv(
            self.productos, self.carpeta, self.ahora)
        filas = leer_csv(ruta)
        self.assertEqual(filas[0], ["codigo", "nombre", "categoria", "precio", "cantidad"])
        self.assertEqual([f[0] for f in filas[1:]], ["A01", "A02", "B01"])
        self.assertEqual(filas[1], ["A01", "Arroz", "Granos", "4500.00", "10"])

    def test_conserva_tildes_y_enes(self):
        ruta = exportacion.exportar_inventario_csv(
            self.productos, self.carpeta, self.ahora)
        texto = ruta.read_text(encoding="utf-8-sig")
        self.assertIn("Fríjol", texto)
        self.assertIn("Lácteos", texto)

    def test_crea_la_carpeta_automaticamente(self):
        self.assertFalse(self.carpeta.exists())
        exportacion.exportar_inventario_csv(self.productos, self.carpeta, self.ahora)
        self.assertTrue(self.carpeta.is_dir())

    def test_el_nombre_incluye_fecha_y_hora(self):
        ruta = exportacion.exportar_inventario_csv(
            self.productos, self.carpeta, self.ahora)
        self.assertEqual(ruta.name, "inventario_20261024_224105.csv")

    def test_dos_exportaciones_no_se_sobrescriben(self):
        r1 = exportacion.exportar_inventario_csv(self.productos, self.carpeta, self.ahora)
        r2 = exportacion.exportar_inventario_csv(self.productos[:1], self.carpeta, self.ahora)
        self.assertNotEqual(r1, r2)
        self.assertEqual(r2.name, "inventario_20261024_224105_2.csv")
        self.assertEqual(len(leer_csv(r1)), 4)
        self.assertEqual(len(leer_csv(r2)), 2)

    def test_sin_productos_se_rechaza_y_no_crea_nada(self):
        with self.assertRaises(ValueError):
            exportacion.exportar_inventario_csv([], self.carpeta, self.ahora)
        self.assertFalse(self.carpeta.exists())

    def test_exportar_no_modifica_los_productos(self):
        antes = [(p.codigo, p.nombre, p.precio, p.cantidad) for p in self.productos]
        exportacion.exportar_inventario_csv(self.productos, self.carpeta, self.ahora)
        despues = [(p.codigo, p.nombre, p.precio, p.cantidad) for p in self.productos]
        self.assertEqual(antes, despues)

    def test_carpeta_imposible_lanza_oserror(self):
        archivo = self.carpeta.parent / "no_es_carpeta"
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text("x", encoding="utf-8")
        with self.assertRaises(OSError):
            exportacion.exportar_inventario_csv(
                self.productos, archivo / "dentro", self.ahora)

    def test_si_falla_la_escritura_no_queda_archivo_incompleto(self):
        with patch("exportacion.csv.writer", side_effect=OSError("disco lleno")):
            with self.assertRaises(OSError):
                exportacion.exportar_inventario_csv(
                    self.productos, self.carpeta, self.ahora)
        self.assertEqual(list(self.carpeta.glob("*.csv")), [])

    def test_usa_la_carpeta_de_constantes_por_defecto(self):
        with patch("exportacion.CARPETA_EXPORTACIONES", self.carpeta):
            ruta = exportacion.exportar_inventario_csv(self.productos, ahora=self.ahora)
        self.assertEqual(ruta.parent, self.carpeta)


class TestExportarMovimientos(PruebaBase):
    def setUp(self):
        super().setUp()
        self.movimientos = [
            movimiento("MOV-0001", "2026-10-24T10:00:00", "Entrada", "A01", 10, "juan"),
            movimiento("MOV-0002", "2026-10-24T11:30:00", "Salida", "A01", 4, "maria"),
        ]

    def test_genera_encabezado_y_conserva_el_orden(self):
        ruta = exportacion.exportar_movimientos_csv(
            self.movimientos, self.carpeta, self.ahora)
        filas = leer_csv(ruta)
        self.assertEqual(filas[0], ["id_movimiento", "fecha", "tipo",
                                    "codigo_producto", "cantidad", "usuario"])
        self.assertEqual(filas[1], ["MOV-0001", "2026-10-24T10:00:00", "Entrada",
                                    "A01", "10", "juan"])
        self.assertEqual([f[0] for f in filas[1:]], ["MOV-0001", "MOV-0002"])

    def test_el_nombre_incluye_fecha_y_hora(self):
        ruta = exportacion.exportar_movimientos_csv(
            self.movimientos, self.carpeta, self.ahora)
        self.assertEqual(ruta.name, "movimientos_20261024_224105.csv")

    def test_sin_movimientos_se_rechaza_y_no_crea_nada(self):
        with self.assertRaises(ValueError):
            exportacion.exportar_movimientos_csv([], self.carpeta, self.ahora)
        self.assertFalse(self.carpeta.exists())

    def test_exportar_no_modifica_los_movimientos(self):
        copia = [vars(m).copy() for m in self.movimientos]
        exportacion.exportar_movimientos_csv(self.movimientos, self.carpeta, self.ahora)
        self.assertEqual(copia, [vars(m) for m in self.movimientos])


if __name__ == "__main__":
    unittest.main()
