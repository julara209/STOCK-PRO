import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import almacenamiento


class TestAlmacenamientoMovimientos(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(self.carpeta.cleanup)
        self.ruta = Path(self.carpeta.name) / "datos" / "movimientos.json"
        parche = patch("almacenamiento.ARCHIVO_MOVIMIENTOS", self.ruta)
        parche.start()
        self.addCleanup(parche.stop)

    def test_archivo_inexistente_devuelve_lista_vacia(self):
        self.assertEqual(almacenamiento.cargar_movimientos(), [])

    def test_guardar_crea_la_carpeta_y_se_puede_cargar(self):
        datos = [{"id_movimiento": "MOV-0001", "cantidad": 3}]
        almacenamiento.guardar_movimientos(datos)
        self.assertTrue(self.ruta.exists())
        self.assertEqual(almacenamiento.cargar_movimientos(), datos)

    def test_archivo_danado_lanza_error_y_no_se_sobrescribe(self):
        self.ruta.parent.mkdir(parents=True)
        self.ruta.write_text("{esto no es json", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            almacenamiento.cargar_movimientos()
        self.assertEqual(self.ruta.read_text(encoding="utf-8"), "{esto no es json")


if __name__ == "__main__":
    unittest.main()
