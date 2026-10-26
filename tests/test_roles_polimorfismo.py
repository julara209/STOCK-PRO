"""Herencia y polimorfismo de los usuarios: Administrador y Empleado."""
import unittest

from modelos.usuario import (
    Administrador,
    Empleado,
    ROL_ADMINISTRADOR,
    ROL_EMPLEADO,
    Usuario,
    crear_usuario,
)
from servicios.usuarios import registrar_usuario

CLAVE = "Segura123"


class TestHerencia(unittest.TestCase):
    def test_la_fabrica_crea_la_subclase_segun_el_rol(self):
        self.assertIsInstance(crear_usuario("ana", CLAVE, ROL_ADMINISTRADOR), Administrador)
        self.assertIsInstance(crear_usuario("luis", CLAVE, ROL_EMPLEADO), Empleado)

    def test_ambas_subclases_son_usuarios(self):
        self.assertTrue(issubclass(Administrador, Usuario))
        self.assertTrue(issubclass(Empleado, Usuario))

    def test_rol_invalido_se_rechaza(self):
        with self.assertRaises(ValueError):
            crear_usuario("ana", CLAVE, "Gerente")

    def test_la_clase_base_no_se_puede_crear_directamente(self):
        with self.assertRaises(TypeError):
            Usuario("ana", CLAVE)


class TestPolimorfismo(unittest.TestCase):
    def setUp(self):
        self.admin = crear_usuario("ana", CLAVE, ROL_ADMINISTRADOR)
        self.empleado = crear_usuario("luis", CLAVE, ROL_EMPLEADO)

    def test_cada_rol_sobrescribe_los_permisos(self):
        self.assertIn("registrar_usuarios", self.admin.permisos)
        self.assertIn("ver_reportes", self.admin.permisos)
        self.assertNotIn("registrar_usuarios", self.empleado.permisos)
        self.assertNotIn("ver_reportes", self.empleado.permisos)

    def test_el_mismo_mensaje_da_resultados_distintos(self):
        resultados = [(u.titulo_menu(), u.tiene_permiso("ver_reportes"))
                      for u in (self.admin, self.empleado)]
        self.assertEqual(resultados, [("MENÚ DE ADMINISTRACIÓN", True), ("MENÚ DE EMPLEADO", False)])

    def test_registrar_usuarios_decide_por_permiso_no_por_rol(self):
        usuarios = [self.admin]
        registrar_usuario(usuarios, "pedro", CLAVE, ROL_EMPLEADO, self.admin)
        with self.assertRaises(PermissionError):
            registrar_usuario(usuarios, "maria", CLAVE, ROL_EMPLEADO, self.empleado)
        self.assertEqual([u.nombre_usuario for u in usuarios], ["ana", "pedro"])

    def test_el_usuario_guardado_se_reconstruye_con_su_subclase(self):
        for original in (self.admin, self.empleado):
            with self.subTest(rol=original.rol):
                recuperado = Usuario.from_dict(original.to_dict())
                self.assertIs(type(recuperado), type(original))
                self.assertTrue(recuperado.verificar_contrasena(CLAVE))
                self.assertEqual(recuperado.permisos, original.permisos)


if __name__ == "__main__":
    unittest.main()
