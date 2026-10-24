
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import almacenamiento


class TestAlmacenamiento(unittest.TestCase):

    def setUp(self):
        self.directorio = tempfile.TemporaryDirectory()
        self.archivo = Path(self.directorio.name) / "data" / "inventario.json"

        self.patch_archivo = patch(
            "almacenamiento.ARCHIVO_DATOS",
            self.archivo
        )
        self.patch_archivo.start()

        self.addCleanup(self.patch_archivo.stop)
        self.addCleanup(self.directorio.cleanup)

    def test_archivo_inexistente_inicia_con_datos_vacios(self):
        self.assertEqual(almacenamiento.cargar(), [])
        self.assertEqual(almacenamiento.cargar_usuarios(), [])
        self.assertEqual(almacenamiento.cargar_movimientos(), [])
        self.assertFalse(self.archivo.exists())

    def test_guardar_crea_la_carpeta_y_el_archivo(self):
        productos = [
            {
                "codigo": "A01",
                "nombre": "Arroz",
                "categoria": "Granos",
                "precio": 4500.0,
                "cantidad": 10
            }
        ]

        almacenamiento.guardar(productos)

        self.assertTrue(self.archivo.exists())
        self.assertEqual(almacenamiento.cargar(), productos)

    def test_datos_se_conservan_entre_cargas(self):
        productos = [
            {
                "codigo": "A01",
                "nombre": "Arroz",
                "categoria": "Granos",
                "precio": 4500.0,
                "cantidad": 10
            }
        ]

        almacenamiento.guardar(productos)

        # Simula una nueva lectura, como al iniciar el programa.
        productos_cargados = almacenamiento.cargar()

        self.assertEqual(productos_cargados, productos)

    def test_usuarios_y_movimientos_comparten_el_mismo_archivo(self):
        productos = [
            {
                "codigo": "A01",
                "nombre": "Arroz",
                "categoria": "Granos",
                "precio": 4500.0,
                "cantidad": 10
            }
        ]
        usuarios = [
            {
                "usuario": "empleado1",
                "rol": "Empleado"
            }
        ]
        movimientos = [
            {
                "tipo": "Entrada",
                "codigo_producto": "A01",
                "cantidad": 5,
                "usuario_responsable": "empleado1",
                "fecha": "2026-10-24 10:00:00"
            }
        ]

        almacenamiento.guardar(productos)
        almacenamiento.guardar_usuarios(usuarios)
        almacenamiento.guardar_movimientos(movimientos)

        self.assertEqual(almacenamiento.cargar(), productos)
        self.assertEqual(almacenamiento.cargar_usuarios(), usuarios)
        self.assertEqual(almacenamiento.cargar_movimientos(), movimientos)

        with open(self.archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        self.assertEqual(
            set(datos.keys()),
            {"productos", "usuarios", "movimientos"}
        )

    def test_formato_anterior_se_mantiene_compatible(self):
        productos = [
            {
                "codigo": "A01",
                "nombre": "Arroz",
                "categoria": "Granos",
                "precio": 4500.0,
                "cantidad": 10
            }
        ]

        self.archivo.parent.mkdir(parents=True, exist_ok=True)

        with open(self.archivo, "w", encoding="utf-8") as archivo:
            json.dump(productos, archivo)

        self.assertEqual(almacenamiento.cargar(), productos)
        self.assertEqual(almacenamiento.cargar_usuarios(), [])
        self.assertEqual(almacenamiento.cargar_movimientos(), [])

    def test_archivo_danado_no_se_sobrescribe(self):
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        contenido_danado = '{"productos": [datos incorrectos'

        with open(self.archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido_danado)

        with self.assertRaises(ValueError):
            almacenamiento.cargar()

        with self.assertRaises(ValueError):
            almacenamiento.guardar([])

        with open(self.archivo, "r", encoding="utf-8") as archivo:
            contenido_despues = archivo.read()

        self.assertEqual(contenido_despues, contenido_danado)

    def test_estructura_invalida_no_se_sobrescribe(self):
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        contenido_invalido = '{"productos": []}'

        with open(self.archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido_invalido)

        with self.assertRaises(ValueError):
            almacenamiento.guardar([])

        with open(self.archivo, "r", encoding="utf-8") as archivo:
            self.assertEqual(archivo.read(), contenido_invalido)

    def test_datos_invalidos_no_se_guardan(self):
        with self.assertRaises(ValueError):
            almacenamiento.guardar("no es una lista")

        with self.assertRaises(ValueError):
            almacenamiento.guardar_usuarios("no es una lista")

        with self.assertRaises(ValueError):
            almacenamiento.guardar_movimientos("no es una lista")

        self.assertFalse(self.archivo.exists())


if __name__ == "__main__":
    unittest.main()
