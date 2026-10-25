import unittest

from modelos.usuario import Usuario, ROL_ADMINISTRADOR, ROL_EMPLEADO
from servicios.usuarios import registrar_usuario, iniciar_sesion

CLAVE = "Segura123"


class TestRegistroAceptado(unittest.TestCase):
    def setUp(self):
        self.usuarios = []
        self.admin = registrar_usuario(self.usuarios, "admin", CLAVE, ROL_ADMINISTRADOR)

    def test_admin_registra_empleado(self):
        emp = registrar_usuario(self.usuarios, "ana", CLAVE, ROL_EMPLEADO, self.admin)
        self.assertIn(emp, self.usuarios)
        self.assertEqual(emp.rol, ROL_EMPLEADO)

    def test_registro_valido_puede_iniciar_sesion(self):
        registrar_usuario(self.usuarios, "ana", CLAVE, ROL_EMPLEADO, self.admin)
        self.assertIsNotNone(iniciar_sesion(self.usuarios, "ana", CLAVE))
        self.assertIsNone(iniciar_sesion(self.usuarios, "ana", "Incorrecta1"))

    def test_contrasena_guardada_con_hash(self):
        u = self.usuarios[0]
        self.assertNotIn(CLAVE, vars(u).values())
        self.assertTrue(u.verificar_contrasena(CLAVE))


class TestRegistroRechazado(unittest.TestCase):
    def setUp(self):
        self.usuarios = []
        self.admin = registrar_usuario(self.usuarios, "admin", CLAVE, ROL_ADMINISTRADOR)
        self.emp = registrar_usuario(self.usuarios, "ana", CLAVE, ROL_EMPLEADO, self.admin)

    def _rechaza(self, exc, *args, **kw):
        antes = list(self.usuarios)
        with self.assertRaises(exc):
            registrar_usuario(self.usuarios, *args, **kw)
        self.assertEqual(self.usuarios, antes)  # lista intacta

    def test_nombre_vacio(self):
        self._rechaza(ValueError, "  ", CLAVE, ROL_EMPLEADO, solicitante=self.admin)

    def test_nombre_repetido(self):
        self._rechaza(ValueError, "ANA", CLAVE, ROL_EMPLEADO, solicitante=self.admin)

    def test_contrasena_debil(self):
        self._rechaza(ValueError, "luis", "abc", ROL_EMPLEADO, solicitante=self.admin)

    def test_rol_invalido(self):
        self._rechaza(ValueError, "luis", CLAVE, "Gerente", solicitante=self.admin)

    def test_empleado_no_crea_administrador(self):
        self._rechaza(PermissionError, "luis", CLAVE, ROL_ADMINISTRADOR, solicitante=self.emp)

    def test_empleado_no_registra_usuarios(self):
        self._rechaza(PermissionError, "luis", CLAVE, ROL_EMPLEADO, solicitante=self.emp)


if __name__ == "__main__":
    unittest.main()