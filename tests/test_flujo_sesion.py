"""Prueba el programa completo: primer administrador, inicio de sesión,
menús por rol, permisos y registro de usuarios desde la consola (HU-004 y HU-007).

Usa un JSON temporal y teclado simulado.
"""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from consola.menu_principal import menu_principal
from modelos.usuario import ROL_ADMINISTRADOR, ROL_EMPLEADO
from servicios.autenticacion import Autenticacion
from servicios.inventario import GestorInventario
from servicios.usuarios import cargar_usuarios, registrar_y_guardar


class Base(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "data" / "inventario.json"
        parche = patch("almacenamiento.ARCHIVO_DATOS", self.ruta)
        parche.start()
        self.addCleanup(parche.stop)

    def preparar(self, con_usuarios=True):
        self.usuarios = []
        if con_usuarios:
            registrar_y_guardar(self.usuarios, "ana", "Admin123x", ROL_ADMINISTRADOR)
            registrar_y_guardar(self.usuarios, "luis", "Empleado1x", ROL_EMPLEADO,
                                self.usuarios[0])
        self.gestor = GestorInventario()
        self.gestor.registrar_producto("A01", "Arroz", "Granos", 4500, 10)
        self.gestor.registrar_producto("A02", "Fríjol", "Granos", 6000, 0)
        self.auth = Autenticacion(self.usuarios)

    def ejecutar(self, teclas, contrasenas=()):
        """Corre el menú principal con teclado simulado y devuelve lo impreso."""
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=list(teclas)), \
             patch("getpass.getpass", side_effect=list(contrasenas)), \
             redirect_stdout(buffer):
            menu_principal(self.gestor, self.auth, self.usuarios)
        return buffer.getvalue()


class TestPrimerAdministrador(Base):
    def test_sin_usuarios_se_crea_el_primer_administrador_y_se_guarda(self):
        self.preparar(con_usuarios=False)
        texto = self.ejecutar(["admin", "0"], ["Admin123x"])
        self.assertIn("Administrador creado correctamente.", texto)
        guardados = cargar_usuarios()
        self.assertEqual([(u.nombre_usuario, u.rol) for u in guardados],
                         [("admin", ROL_ADMINISTRADOR)])

    def test_contrasena_debil_se_rechaza_y_vuelve_a_pedir(self):
        self.preparar(con_usuarios=False)
        texto = self.ejecutar(["admin", "admin", "0"], ["corta", "Admin123x"])
        self.assertIn("Registro rechazado: La contraseña debe tener al menos 8", texto)
        self.assertIn("Administrador creado correctamente.", texto)

    def test_cancelar_sale_sin_crear_usuarios(self):
        self.preparar(con_usuarios=False)
        self.ejecutar([""])
        self.assertEqual(cargar_usuarios(), [])


class TestInicioDeSesion(Base):
    def setUp(self):
        super().setUp()
        self.preparar()

    def test_credenciales_incorrectas_muestran_error(self):
        texto = self.ejecutar(["1", "ana", "mala", "ana", "mala", "ana", "mala", "0"])
        self.assertIn("Usuario o contraseña incorrectos.", texto)
        self.assertIn("Demasiados intentos fallidos", texto)
        self.assertNotIn("MENÚ DE ADMINISTRACIÓN", texto)

    def test_usuario_no_registrado_no_entra(self):
        texto = self.ejecutar(["1", "fantasma", "Admin123x"] * 3 + ["0"])
        self.assertNotIn("MENÚ DE ADMINISTRACIÓN", texto)
        self.assertNotIn("MENÚ DE EMPLEADO", texto)
        self.assertIn("Usuario o contraseña incorrectos.", texto)

    def test_administrador_entra_al_menu_de_administracion(self):
        texto = self.ejecutar(["1", "ana", "Admin123x", "0", "0"])
        self.assertIn("MENÚ DE ADMINISTRACIÓN (ana)", texto)
        self.assertIn("Registrar usuario", texto)
        self.assertIn("Ver reportes", texto)

    def test_empleado_entra_al_menu_de_empleado_sin_opciones_de_admin(self):
        texto = self.ejecutar(["1", "luis", "Empleado1x", "0", "0"])
        self.assertIn("MENÚ DE EMPLEADO (luis)", texto)
        self.assertIn("Consultar productos agotados", texto)
        self.assertNotIn("Registrar usuario", texto)
        self.assertNotIn("Ver reportes", texto)

    def test_cerrar_sesion_regresa_al_menu_principal(self):
        texto = self.ejecutar(["1", "ana", "Admin123x", "0", "0"])
        self.assertIn("Sesión cerrada.", texto)
        self.assertEqual(texto.count("SISTEMA DE INVENTARIO"), 2)
        self.assertFalse(self.auth.sesion_activa)

    def test_empleado_no_puede_elegir_una_opcion_de_admin(self):
        texto = self.ejecutar(["1", "luis", "Empleado1x", "4", "0", "0"])
        # la 4 no existe en el menú de empleado
        self.assertIn("Opción no válida", texto)

    def test_empleado_no_ve_registrar_ni_actualizar_producto(self):
        texto = self.ejecutar(["1", "luis", "Empleado1x", "1", "0", "0", "0"])
        self.assertIn("GESTIONAR INVENTARIO", texto)
        self.assertIn("Registrar entrada de mercancía", texto)
        self.assertNotIn("Registrar producto", texto)
        self.assertNotIn("Actualizar producto", texto)

    def test_administrador_si_ve_registrar_actualizar_y_reportes(self):
        texto = self.ejecutar(["1", "ana", "Admin123x", "2", "0", "3", "0", "0", "0"])
        self.assertIn("Registrar producto", texto)
        self.assertIn("Actualizar producto", texto)
        self.assertIn("Historial de movimientos", texto)
        self.assertIn("Exportar a CSV", texto)

    def test_empleado_consulta_agotados_e_inventario(self):
        texto = self.ejecutar(["1", "luis", "Empleado1x", "2", "3", "0", "0"])
        self.assertIn("PRODUCTOS AGOTADOS", texto)
        self.assertIn("Fríjol", texto)
        self.assertIn("=== INVENTARIO ===", texto)
        self.assertIn("Arroz", texto)


class TestResponsableDeLaSesion(Base):
    def setUp(self):
        super().setUp()
        self.preparar()

    def movimientos(self):
        return json.loads(self.ruta.read_text(encoding="utf-8"))["movimientos"]

    def test_la_salida_queda_a_nombre_del_usuario_de_la_sesion(self):
        # empleado: 1 gestionar -> 3 salida -> código, cantidad (no pide usuario)
        self.ejecutar(["1", "luis", "Empleado1x", "1", "3", "A01", "2", "0", "0", "0"])
        self.assertEqual([(m["tipo"], m["usuario"], m["cantidad"]) for m in self.movimientos()],
                         [("Salida", "luis", 2)])

    def test_la_entrada_queda_a_nombre_del_usuario_de_la_sesion(self):
        # empleado: 1 gestionar -> 2 entrada -> código, cantidad
        self.ejecutar(["1", "luis", "Empleado1x", "1", "2", "A02", "7", "0", "0", "0"])
        self.assertEqual([(m["tipo"], m["usuario"]) for m in self.movimientos()],
                         [("Entrada", "luis")])
        self.assertEqual(GestorInventario().buscar_producto("A02").cantidad, 7)


class TestRegistroDeUsuariosDesdeLaConsola(Base):
    def setUp(self):
        super().setUp()
        self.preparar()

    def test_administrador_registra_un_empleado_y_queda_guardado(self):
        # admin: 1 registrar usuario -> nombre, (contraseña), rol Enter = Empleado
        texto = self.ejecutar(["1", "ana", "Admin123x", "1", "pedro", "", "0", "0"],
                              ["Empleado9z"])
        self.assertIn("Usuario 'pedro' registrado como Empleado.", texto)
        pedro = next(u for u in cargar_usuarios() if u.nombre_usuario == "pedro")
        self.assertEqual(pedro.rol, ROL_EMPLEADO)
        self.assertTrue(pedro.verificar_contrasena("Empleado9z"))

    def test_registro_rechazado_no_modifica_los_usuarios_guardados(self):
        texto = self.ejecutar(["1", "ana", "Admin123x", "1", "pedro", "", "0", "0"], ["x"])
        self.assertIn("Registro rechazado", texto)
        self.assertEqual(sorted(u.nombre_usuario for u in cargar_usuarios()), ["ana", "luis"])

    def test_nombre_repetido_se_rechaza(self):
        texto = self.ejecutar(["1", "ana", "Admin123x", "1", "LUIS", "", "0", "0"],
                              ["Empleado9z"])
        self.assertIn("El nombre de usuario ya existe.", texto)

    def test_el_nuevo_empleado_puede_iniciar_sesion_despues(self):
        self.ejecutar(["1", "ana", "Admin123x", "1", "pedro", "", "0", "0"], ["Empleado9z"])
        texto = self.ejecutar(["1", "pedro", "Empleado9z", "0", "0"])
        self.assertIn("MENÚ DE EMPLEADO (pedro)", texto)


if __name__ == "__main__":
    unittest.main()
