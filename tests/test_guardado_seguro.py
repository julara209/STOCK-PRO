"""Escritura segura del JSON: archivo temporal y bloque finally."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import almacenamiento


class TestGuardadoSeguro(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "data" / "inventario.json"
        self.temporal = self.ruta.with_name("inventario.json.tmp")
        parche = patch("almacenamiento.ARCHIVO_DATOS", self.ruta)
        parche.start()
        self.addCleanup(parche.stop)

    def test_guardar_no_deja_archivo_temporal(self):
        almacenamiento.guardar([{"codigo": "A01"}])
        self.assertTrue(self.ruta.exists())
        self.assertFalse(self.temporal.exists())

    def test_si_falla_la_escritura_se_conserva_el_json_anterior(self):
        almacenamiento.guardar([{"codigo": "A01"}])
        antes = self.ruta.read_text(encoding="utf-8")
        with patch("almacenamiento.json.dump", side_effect=OSError("disco lleno")):
            with self.assertRaises(OSError):
                almacenamiento.guardar([{"codigo": "B02"}])
        self.assertEqual(self.ruta.read_text(encoding="utf-8"), antes)
        self.assertEqual(json.loads(antes)["productos"], [{"codigo": "A01"}])

    def test_si_falla_la_escritura_finally_elimina_el_temporal(self):
        almacenamiento.guardar([])
        with patch("almacenamiento.json.dump", side_effect=OSError("disco lleno")):
            with self.assertRaises(OSError):
                almacenamiento.guardar([{"codigo": "B02"}])
        self.assertFalse(self.temporal.exists())


if __name__ == "__main__":
    unittest.main()
