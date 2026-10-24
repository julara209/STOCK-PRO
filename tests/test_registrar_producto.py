import unittest
from unittest.mock import patch

from servicios.inventario import GestorInventario

DATOS_INICIALES = [
    {
        "codigo": "A01",
        "nombre": "Arroz",
        "categoria": "Granos",
        "precio": 4500,
        "cantidad": 10
    }
]


class TestGestorRegistrarProducto(unittest.TestCase):

    def setUp(self):
        with patch(
            "almacenamiento.cargar",
            return_value=[dict(d) for d in DATOS_INICIALES]
        ):
            self.gestor = GestorInventario()

    def test_registrar_producto_correctamente(self):
        with patch("almacenamiento.guardar") as guardar:
            self.gestor.registrar_producto(
                "B01", "Leche", "Lácteos", 3800, 5
            )

        producto = self.gestor.buscar_producto("B01")

        self.assertIsNotNone(producto)
        self.assertEqual(producto.codigo, "B01")
        self.assertEqual(producto.nombre, "Leche")
        self.assertEqual(producto.categoria, "Lácteos")
        self.assertEqual(producto.precio, 3800)
        self.assertEqual(producto.cantidad, 5)
        guardar.assert_called_once()

    def test_rechazar_codigo_repetido(self):
        with patch("almacenamiento.guardar") as guardar:
            with self.assertRaises(ValueError):
                self.gestor.registrar_producto(
                    "A01", "Arroz nuevo", "Granos", 5000, 3
                )

        guardar.assert_not_called()
        self.assertEqual(len(self.gestor.productos), 1)

    def test_rechazar_nombre_vacio(self):
        with patch("almacenamiento.guardar") as guardar:
            with self.assertRaises(ValueError):
                self.gestor.registrar_producto(
                    "B01", " ", "Lácteos", 3800, 5
                )

        guardar.assert_not_called()
        self.assertIsNone(self.gestor.buscar_producto("B01"))

    def test_rechazar_precio_cero_o_negativo(self):
        for precio in [0, -100]:
            with self.subTest(precio=precio):
                with patch("almacenamiento.guardar") as guardar:
                    with self.assertRaises(ValueError):
                        self.gestor.registrar_producto(
                            "B01", "Leche", "Lácteos", precio, 5
                        )

                guardar.assert_not_called()
                self.assertIsNone(self.gestor.buscar_producto("B01"))

    def test_rechazar_cantidad_negativa(self):
        with patch("almacenamiento.guardar") as guardar:
            with self.assertRaises(ValueError):
                self.gestor.registrar_producto(
                    "B01", "Leche", "Lácteos", 3800, -1
                )

        guardar.assert_not_called()
        self.assertIsNone(self.gestor.buscar_producto("B01"))

    def test_aceptar_cantidad_inicial_cero(self):
        with patch("almacenamiento.guardar") as guardar:
            self.gestor.registrar_producto(
                "B01", "Leche", "Lácteos", 3800, 0
            )

        producto = self.gestor.buscar_producto("B01")

        self.assertIsNotNone(producto)
        self.assertEqual(producto.cantidad, 0)
        guardar.assert_called_once()

    def test_rechazar_codigo_vacio(self):
        with patch("almacenamiento.guardar") as guardar:
            with self.assertRaises(ValueError):
                self.gestor.registrar_producto(
                    " ", "Leche", "Lácteos", 3800, 5
                )

        guardar.assert_not_called()
        self.assertEqual(len(self.gestor.productos), 1)

    def test_rechazar_categoria_vacia(self):
        with patch("almacenamiento.guardar") as guardar:
            with self.assertRaises(ValueError):
                self.gestor.registrar_producto(
                    "B01", "Leche", " ", 3800, 5
                )

        guardar.assert_not_called()
        self.assertIsNone(self.gestor.buscar_producto("B01"))

    def test_rechazar_datos_invalidos_no_modifica_inventario(self):
        casos = [
            ("B01", "Leche", "Lácteos", "abc", 5),
            ("B01", "Leche", "Lácteos", 3800, "abc"),
            ("B01", "", "Lácteos", 3800, 5),
        ]

        for datos in casos:
            with self.subTest(datos=datos):
                with patch("almacenamiento.guardar") as guardar:
                    with self.assertRaises((ValueError, TypeError)):
                        self.gestor.registrar_producto(*datos)

                guardar.assert_not_called()
                self.assertIsNone(self.gestor.buscar_producto("B01"))
                self.assertEqual(len(self.gestor.productos), 1)


if __name__ == "__main__":
    unittest.main()