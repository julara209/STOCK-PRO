import unittest

from servicios.autenticacion import Autenticacion, ErrorAutenticacion
from consola.menu_sesion import flujo_sesion, pedir_credenciales
from modelos.usuario import ROL_ADMINISTRADOR, ROL_EMPLEADO
from servicios.usuarios import registrar_usuario

CLAVE = "Segura123"


def simular(respuestas):
    """Devuelve (entrada, salida, log) con respuestas predefinidas."""
    it = iter(respuestas)
    log = []
    return (lambda _="": next(it)), log.append, log


class Base(unittest.TestCase):
    def setUp(self):
        self.usuarios = []
        admin = registrar_usuario(self.usuarios, "admin", CLAVE, ROL_ADMINISTRADOR)
        registrar_usuario(self.usuarios, "ana", CLAVE, ROL_EMPLEADO, admin)
        self.auth = Autenticacion(self.usuarios)


class TestIniciarSesion(Base):
    def test_credenciales_correctas(self):
        u = self.auth.iniciar_sesion("admin", CLAVE)
        self.assertEqual(u.rol, ROL_ADMINISTRADOR)
        self.assertTrue(self.auth.sesion_activa)

    def test_contrasena_incorrecta(self):
        with self.assertRaises(ErrorAutenticacion):
            self.auth.iniciar_sesion("admin", "Mala1234")
        self.assertFalse(self.auth.sesion_activa)

    def test_usuario_no_registrado(self):
        with self.assertRaises(ErrorAutenticacion):
            self.auth.iniciar_sesion("fantasma", CLAVE)

    def test_campos_vacios(self):
        with self.assertRaises(ErrorAutenticacion):
            self.auth.iniciar_sesion("", "")

    def test_cerrar_sesion(self):
        self.auth.iniciar_sesion("ana", CLAVE)
        self.auth.cerrar_sesion()
        self.assertIsNone(self.auth.usuario_actual)


class TestPermisos(Base):
    def test_admin_tiene_permisos_exclusivos(self):
        self.auth.iniciar_sesion("admin", CLAVE)
        self.auth.requiere_permiso("registrar_usuarios")
        self.auth.requiere_permiso("ver_reportes")

    def test_empleado_no_accede_a_funciones_de_admin(self):
        self.auth.iniciar_sesion("ana", CLAVE)
        self.auth.requiere_permiso("gestionar_inventario")
        with self.assertRaises(PermissionError):
            self.auth.requiere_permiso("registrar_usuarios")
        with self.assertRaises(PermissionError):
            self.auth.requiere_permiso("ver_reportes")

    def test_sin_sesion_no_hay_permisos(self):
        with self.assertRaises(PermissionError):
            self.auth.requiere_permiso("gestionar_inventario")


class TestConsola(Base):
    def test_credenciales_incorrectas_muestran_error(self):
        entrada, salida, log = simular(["admin", "mala", "admin", "mala", "admin", "mala"])
        self.assertIsNone(pedir_credenciales(self.auth, entrada, salida))
        self.assertTrue(any("incorrectos" in m for m in log))

    def test_admin_ve_menu_administracion_y_cierra_sesion(self):
        entrada, salida, log = simular(["admin", CLAVE, "0"])
        flujo_sesion(self.auth, entrada=entrada, salida=salida)
        self.assertTrue(any("ADMINISTRACIÓN" in m for m in log))
        self.assertFalse(self.auth.sesion_activa)

    def test_empleado_ve_menu_empleado_sin_opciones_de_admin(self):
        entrada, salida, log = simular(["ana", CLAVE, "0"])
        flujo_sesion(self.auth, entrada=entrada, salida=salida)
        texto = "\n".join(log)
        self.assertIn("EMPLEADO", texto)
        self.assertNotIn("Registrar usuario", texto)
        self.assertNotIn("Ver reportes", texto)

    def test_empleado_no_puede_elegir_opcion_de_admin(self):
        ejecutado = []
        acciones = {"registrar_usuarios": lambda: ejecutado.append(1)}
        entrada, salida, log = simular(["ana", CLAVE, "4", "0"])
        flujo_sesion(self.auth, acciones, entrada, salida)
        self.assertEqual(ejecutado, [])
        self.assertTrue(any("no válida" in m for m in log))

    def test_entrada_invalida_no_rompe_el_menu(self):
        entrada, salida, log = simular(["admin", CLAVE, "abc", "", "0"])
        flujo_sesion(self.auth, entrada=entrada, salida=salida)
        self.assertEqual(sum("no válida" in m for m in log), 2)

    def test_admin_ejecuta_accion_conectada(self):
        ejecutado = []
        acciones = {"ver_reportes": lambda: ejecutado.append(1)}
        entrada, salida, _ = simular(["admin", CLAVE, "3", "0"])
        flujo_sesion(self.auth, acciones, entrada, salida)
        self.assertEqual(ejecutado, [1])


if __name__ == "__main__":
    unittest.main()