"""Pruebas de aceptación: un método por cada criterio de las historias de usuario.

Usan el gestor y el almacenamiento reales, pero con un archivo JSON temporal,
así que no tocan data/inventario.json. El nombre de cada prueba empieza con el
número de la historia que verifica.
"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import almacenamiento
from modelos.usuario import ROL_ADMINISTRADOR, ROL_EMPLEADO
from servicios.actualizacion import ProductoNoEncontradoError
from servicios.inventario import GestorInventario
from servicios.usuarios import cargar_usuarios, registrar_y_guardar, registrar_usuario
from consola.menu_agotados import mostrar_agotados
from consola.menu_inventario import mostrar_inventario


class Base(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "data" / "inventario.json"
        parche = patch("almacenamiento.ARCHIVO_DATOS", self.ruta)
        parche.start()
        self.addCleanup(parche.stop)
        self.gestor = GestorInventario()

    def texto_json(self):
        return self.ruta.read_text(encoding="utf-8") if self.ruta.exists() else None

    def datos(self, codigo):
        p = self.gestor.buscar_producto(codigo)
        return None if p is None else (p.nombre, p.categoria, p.precio, p.cantidad)

    def cargar(self):
        """Simula cerrar y volver a abrir el programa."""
        return GestorInventario()


class Hu01RegistrarProducto(Base):
    def test_hu01_codigo_no_puede_repetirse(self):
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)
        with self.assertRaises(ValueError):
            self.gestor.registrar_producto("A01", "Otro", "Granos", 100, 1)

    def test_hu01_nombre_no_puede_estar_vacio(self):
        with self.assertRaises(ValueError):
            self.gestor.registrar_producto("A01", "  ", "Granos", 4500, 10)

    def test_hu01_precio_debe_ser_mayor_que_cero(self):
        for precio in (0, -5, "abc"):
            with self.subTest(precio=precio):
                with self.assertRaises(ValueError):
                    self.gestor.registrar_producto("A01", "Arroz", "Granos", precio, 10)

    def test_hu01_cantidad_inicial_cero_es_valida_y_negativa_no(self):
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 0)
        with self.assertRaises(ValueError):
            self.gestor.registrar_producto("A02", "Sal", "Cond", 1000, -1)

    def test_hu01_producto_registrado_queda_disponible(self):
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)
        self.assertEqual([p.codigo for p in self.gestor.consultar_productos()], ["A01"])

    def test_hu01_registro_rechazado_no_modifica_el_inventario(self):
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)
        antes = self.texto_json()
        with self.assertRaises(ValueError):
            self.gestor.registrar_producto("A02", "Frijol", "Granos", 0, 5)
        self.assertEqual(len(self.gestor.consultar_productos()), 1)
        self.assertEqual(self.texto_json(), antes)


class Hu02ActualizarProducto(Base):
    def setUp(self):
        super().setUp()
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)

    def test_hu02_actualiza_precio_y_datos(self):
        self.gestor.actualizar_producto("A01", nombre="Arroz Roa", categoria="Cereales", precio=5000)
        self.assertEqual(self.datos("A01"), ("Arroz Roa", "Cereales", 5000.0, 10))

    def test_hu02_el_producto_debe_existir(self):
        with self.assertRaises(ProductoNoEncontradoError):
            self.gestor.actualizar_producto("ZZZ", precio=100)

    def test_hu02_precio_debe_ser_mayor_que_cero(self):
        for precio in (0, -1):
            with self.subTest(precio=precio):
                with self.assertRaises(ValueError):
                    self.gestor.actualizar_producto("A01", precio=precio)

    def test_hu02_datos_obligatorios_no_pueden_estar_vacios(self):
        with self.assertRaises(ValueError):
            self.gestor.actualizar_producto("A01", nombre="   ")

    def test_hu02_las_entradas_aumentan_las_existencias(self):
        self.gestor.actualizar_producto("A01", entrada=5)
        self.assertEqual(self.datos("A01")[3], 15)

    def test_hu02_actualizacion_rechazada_no_modifica_nada(self):
        antes, json_antes = self.datos("A01"), self.texto_json()
        with self.assertRaises(ValueError):
            self.gestor.actualizar_producto("A01", nombre=" ", precio=9999)
        self.assertEqual(self.datos("A01"), antes)
        self.assertEqual(self.texto_json(), json_antes)


class Hu03BuscarProductos(Base):
    def setUp(self):
        super().setUp()
        self.gestor.registrar_producto("A01", "Arroz Diana", "Granos", 4500, 10)
        self.gestor.registrar_producto("A02", "Fríjol", "Granos", 6000, 0)
        self.gestor.registrar_producto("B01", "Leche", "Lácteos", 3800, 20)

    def codigos(self, **criterios):
        return [p.codigo for p in self.gestor.buscar_productos(**criterios)]

    def test_hu03_nombre_sin_distinguir_mayusculas(self):
        self.assertEqual(self.codigos(nombre="aRRoz"), ["A01"])

    def test_hu03_codigo_exacto(self):
        self.assertEqual(self.codigos(codigo="B01"), ["B01"])
        self.assertEqual(self.codigos(codigo="B0"), [])

    def test_hu03_filtrar_por_categoria(self):
        self.assertEqual(self.codigos(categoria="granos"), ["A01", "A02"])

    def test_hu03_sin_resultados_devuelve_lista_vacia(self):
        self.assertEqual(self.codigos(nombre="zzz"), [])

    def test_hu03_la_busqueda_no_modifica_los_datos(self):
        antes = self.texto_json()
        self.gestor.buscar_productos(nombre="a")
        self.assertEqual(self.texto_json(), antes)


class Hu04RegistrarUsuarios(Base):
    def setUp(self):
        super().setUp()
        self.usuarios = []
        self.admin = registrar_y_guardar(self.usuarios, "ana", "Admin123x", ROL_ADMINISTRADOR)

    def registrar(self, nombre="luis", contrasena="Empleado1x", rol=ROL_EMPLEADO, quien=None):
        return registrar_y_guardar(self.usuarios, nombre, contrasena, rol, quien or self.admin)

    def test_hu04_nombre_no_puede_estar_vacio_ni_repetido(self):
        with self.assertRaises(ValueError):
            self.registrar(nombre="  ")
        self.registrar()
        with self.assertRaises(ValueError):
            self.registrar(nombre="LUIS")

    def test_hu04_contrasena_debe_cumplir_las_reglas(self):
        for mala in ("corta1A", "sinmayuscula1", "SINMINUSCULA1", "SinNumeroAqui"):
            with self.subTest(contrasena=mala):
                with self.assertRaises(ValueError):
                    self.registrar(contrasena=mala)

    def test_hu04_el_rol_debe_ser_valido(self):
        with self.assertRaises(ValueError):
            self.registrar(rol="Gerente")

    def test_hu04_empleado_no_puede_crear_administradores(self):
        empleado = self.registrar()
        with self.assertRaises(PermissionError):
            self.registrar(nombre="pepe", rol=ROL_ADMINISTRADOR, quien=empleado)

    def test_hu04_registro_valido_queda_disponible_para_iniciar_sesion(self):
        self.registrar()
        guardados = cargar_usuarios()          # como al reiniciar el programa
        luis = next(u for u in guardados if u.nombre_usuario == "luis")
        self.assertTrue(luis.verificar_contrasena("Empleado1x"))
        self.assertFalse(luis.verificar_contrasena("otra"))
        self.assertEqual(luis.rol, ROL_EMPLEADO)

    def test_hu04_la_contrasena_se_guarda_con_hash(self):
        self.registrar()
        self.assertNotIn("Empleado1x", self.texto_json())
        self.assertNotIn("Admin123x", self.texto_json())

    def test_hu04_registro_rechazado_no_modifica_la_lista_ni_el_archivo(self):
        antes, json_antes = list(self.usuarios), self.texto_json()
        with self.assertRaises(ValueError):
            self.registrar(contrasena="x")
        self.assertEqual(self.usuarios, antes)
        self.assertEqual(self.texto_json(), json_antes)

    def test_hu04_sin_administrador_no_se_pueden_crear_usuarios(self):
        with self.assertRaises(PermissionError):
            registrar_usuario([self.admin], "x", "Empleado1x", ROL_EMPLEADO)


class Hu05Hu06Movimientos(Base):
    def setUp(self):
        super().setUp()
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)

    def historial(self):
        return self.cargar().consultar_historial_movimientos()

    def test_hu05_salida_valida_descuenta_y_registra_el_movimiento(self):
        self.gestor.registrar_salida("A01", 4, "maria")
        self.assertEqual(self.datos("A01")[3], 6)
        mov = self.historial()[0]
        self.assertEqual((mov["tipo"], mov["codigo_producto"], mov["cantidad"], mov["usuario"]),
                         ("Salida", "A01", 4, "maria"))
        self.assertTrue(mov["fecha"])

    def test_hu05_producto_debe_existir(self):
        with self.assertRaises(ValueError):
            self.gestor.registrar_salida("ZZZ", 1, "maria")

    def test_hu05_cantidad_mayor_que_cero_y_no_mayor_al_stock(self):
        for cantidad in (0, -2, 11):
            with self.subTest(cantidad=cantidad):
                with self.assertRaises(ValueError):
                    self.gestor.registrar_salida("A01", cantidad, "maria")

    def test_hu05_salida_rechazada_no_modifica_existencias_ni_historial(self):
        antes = self.texto_json()
        with self.assertRaises(ValueError):
            self.gestor.registrar_salida("A01", 99, "maria")
        self.assertEqual(self.texto_json(), antes)
        self.assertEqual(self.historial(), [])

    def test_hu06_entrada_se_suma_y_registra_fecha_producto_cantidad_usuario(self):
        self.gestor.registrar_entrada("A01", 5, "juan")
        self.assertEqual(self.datos("A01")[3], 15)
        mov = self.historial()[0]
        self.assertEqual((mov["tipo"], mov["codigo_producto"], mov["cantidad"], mov["usuario"]),
                         ("Entrada", "A01", 5, "juan"))
        self.assertTrue(mov["fecha"])

    def test_hu06_producto_inexistente_o_cantidad_invalida_se_rechaza(self):
        with self.assertRaises(ProductoNoEncontradoError):
            self.gestor.registrar_entrada("ZZZ", 5, "juan")
        for cantidad in (0, -1, 2.5, True):
            with self.subTest(cantidad=cantidad):
                with self.assertRaises(ValueError):
                    self.gestor.registrar_entrada("A01", cantidad, "juan")

    def test_hu06_entrada_rechazada_no_modifica_el_inventario(self):
        antes = self.texto_json()
        with self.assertRaises(ValueError):
            self.gestor.registrar_entrada("A01", 0, "juan")
        with self.assertRaises(ValueError):
            self.gestor.registrar_entrada("A01", 5, "")
        self.assertEqual(self.texto_json(), antes)


class Hu08Hu09Consultas(Base):
    def setUp(self):
        super().setUp()
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 3)
        self.gestor.registrar_producto("A02", "Fríjol", "Granos", 6000, 0)
        self.gestor.registrar_producto("B01", "Leche", "Lácteos", 3800, 20)

    def pantalla(self, funcion):
        lineas = []
        funcion(self.gestor, lineas.append)
        return "\n".join(lineas)

    def test_hu08_solo_aparecen_productos_con_existencias_cero(self):
        self.assertEqual([p.codigo for p in self.gestor.productos_agotados()], ["A02"])

    def test_hu08_muestra_codigo_nombre_y_categoria(self):
        texto = self.pantalla(mostrar_agotados)
        for dato in ("A02", "Fríjol", "Granos"):
            self.assertIn(dato, texto)
        self.assertNotIn("Leche", texto)

    def test_hu08_sin_agotados_lo_informa(self):
        self.gestor.registrar_entrada("A02", 5, "juan")
        self.assertIn("No hay productos agotados.", self.pantalla(mostrar_agotados))

    def test_hu08_hu09_las_consultas_no_modifican_las_existencias(self):
        antes = self.texto_json()
        self.pantalla(mostrar_agotados)
        self.pantalla(mostrar_inventario)
        self.assertEqual(self.texto_json(), antes)

    def test_hu09_muestra_codigo_nombre_categoria_precio_y_existencias(self):
        texto = self.pantalla(mostrar_inventario)
        for dato in ("Código", "Nombre", "Categoría", "Precio", "Existencias",
                     "A01", "Arroz", "Granos", "$4,500.00", "Leche", "20"):
            self.assertIn(dato, texto)

    def test_hu09_refleja_entradas_y_salidas(self):
        self.gestor.registrar_entrada("A01", 7, "juan")
        self.gestor.registrar_salida("B01", 5, "maria")
        self.assertEqual({p.codigo: p.cantidad for p in self.gestor.listar_productos()},
                         {"A01": 10, "A02": 0, "B01": 15})

    def test_hu09_sin_productos_muestra_mensaje(self):
        vacio = GestorInventario.__new__(GestorInventario)
        vacio.productos = []
        lineas = []
        mostrar_inventario(vacio, lineas.append)
        self.assertIn("No hay productos registrados.", "\n".join(lineas))


class Hu11Persistencia(Base):
    def test_hu11_se_guardan_productos_usuarios_y_movimientos_en_un_solo_archivo(self):
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)
        self.gestor.registrar_salida("A01", 2, "maria")
        registrar_y_guardar([], "ana", "Admin123x", ROL_ADMINISTRADOR)
        datos = json.loads(self.texto_json())
        self.assertEqual(set(datos), {"productos", "usuarios", "movimientos"})
        self.assertEqual((len(datos["productos"]), len(datos["usuarios"]), len(datos["movimientos"])),
                         (1, 1, 1))

    def test_hu11_al_iniciar_se_cargan_los_datos_guardados(self):
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)
        self.gestor.registrar_entrada("A01", 5, "juan")
        nuevo = self.cargar()
        self.assertEqual(nuevo.buscar_producto("A01").cantidad, 15)
        self.assertEqual(len(nuevo.movimientos), 1)

    def test_hu11_archivo_inexistente_inicia_con_datos_vacios(self):
        self.assertFalse(self.ruta.exists())
        self.assertEqual(self.gestor.consultar_productos(), [])
        self.assertEqual(self.gestor.movimientos, [])
        self.assertEqual(cargar_usuarios(), [])

    def test_hu11_archivo_danado_se_informa_y_no_se_sobrescribe(self):
        self.ruta.parent.mkdir(parents=True)
        self.ruta.write_text("{esto no es json", encoding="utf-8")
        with self.assertRaises(ValueError) as contexto:
            GestorInventario()
        self.assertIn("dañado", str(contexto.exception))
        with self.assertRaises(ValueError):
            almacenamiento.guardar([])
        self.assertEqual(self.ruta.read_text(encoding="utf-8"), "{esto no es json")

    def test_hu11_se_guarda_despues_de_cada_operacion_exitosa(self):
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)
        self.assertEqual(len(json.loads(self.texto_json())["productos"]), 1)
        self.gestor.actualizar_producto("A01", precio=5000)
        self.assertEqual(json.loads(self.texto_json())["productos"][0]["precio"], 5000)
        self.gestor.registrar_salida("A01", 1, "maria")
        self.assertEqual(len(json.loads(self.texto_json())["movimientos"]), 1)

    def test_hu11_las_operaciones_rechazadas_no_alteran_el_archivo(self):
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)
        antes = self.texto_json()
        for operacion in (
            lambda: self.gestor.registrar_producto("A01", "Dup", "G", 1, 1),
            lambda: self.gestor.actualizar_producto("A01", precio=-1),
            lambda: self.gestor.registrar_salida("A01", 999, "maria"),
            lambda: self.gestor.registrar_entrada("A01", 0, "juan"),
        ):
            with self.assertRaises(ValueError):
                operacion()
        self.assertEqual(self.texto_json(), antes)

    def test_hu11_el_formato_anterior_de_lista_se_sigue_leyendo(self):
        self.ruta.parent.mkdir(parents=True)
        self.ruta.write_text(json.dumps([{"codigo": "Z1", "nombre": "Sal", "categoria": "C",
                                          "precio": 1000, "cantidad": 3}]), encoding="utf-8")
        self.assertEqual(self.cargar().buscar_producto("Z1").cantidad, 3)


class Hu12Historial(Base):
    def setUp(self):
        super().setUp()
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)
        self.gestor.registrar_producto("B01", "Leche", "Lácteos", 3800, 20)
        self.gestor.registrar_entrada("A01", 5, "juan")
        self.gestor.registrar_salida("A01", 2, "maria")
        self.gestor.registrar_salida("B01", 1, "maria")

    def test_hu12_cada_movimiento_tiene_identificador_unico(self):
        ids = [m["id_movimiento"] for m in self.gestor.consultar_historial_movimientos()]
        self.assertEqual(len(ids), 3)
        self.assertEqual(len(set(ids)), 3)

    def test_hu12_muestra_tipo_producto_cantidad_fecha_y_usuario(self):
        mov = self.gestor.consultar_historial_movimientos()[0]
        for campo in ("tipo", "codigo_producto", "cantidad", "fecha", "usuario"):
            self.assertIn(campo, mov)
            self.assertTrue(mov[campo])

    def test_hu12_historial_completo_y_filtros(self):
        self.assertEqual(len(self.gestor.consultar_historial_movimientos()), 3)
        self.assertEqual(len(self.gestor.consultar_historial_movimientos(codigo_producto="A01")), 2)
        self.assertEqual(len(self.gestor.consultar_historial_movimientos(tipo="salida")), 2)
        self.assertEqual(len(self.gestor.consultar_historial_movimientos("A01", "Entrada")), 1)

    def test_hu12_sin_movimientos_devuelve_lista_vacia(self):
        self.assertEqual(self.gestor.consultar_historial_movimientos(codigo_producto="ZZZ"), [])

    def test_hu12_consultar_no_modifica_los_datos(self):
        antes = self.texto_json()
        self.gestor.consultar_historial_movimientos(tipo="Entrada")
        self.assertEqual(self.texto_json(), antes)


if __name__ == "__main__":
    unittest.main()
