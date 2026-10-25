"""Autenticación y control de permisos (HU-007 · Iniciar sesión según el rol)."""


class ErrorAutenticacion(Exception):
    """Credenciales incorrectas o usuario no registrado."""


class Autenticacion:
    def __init__(self, usuarios: list):
        self.usuarios = usuarios
        self._usuario_actual = None

    @property
    def usuario_actual(self):
        return self._usuario_actual

    @property
    def sesion_activa(self) -> bool:
        return self._usuario_actual is not None

    def iniciar_sesion(self, nombre: str, contrasena: str):
        """Valida las credenciales y abre la sesión. Lanza ErrorAutenticacion si fallan."""
        nombre = (nombre or "").strip()
        if not nombre or not contrasena:
            raise ErrorAutenticacion("Usuario o contraseña incorrectos.")

        usuario = next(
            (u for u in self.usuarios if u.nombre_usuario.lower() == nombre.lower()), None
        )
        # Mismo mensaje para "no existe" y "contraseña mala": no revela qué usuarios existen
        if usuario is None or not usuario.verificar_contrasena(contrasena):
            raise ErrorAutenticacion("Usuario o contraseña incorrectos.")

        self._usuario_actual = usuario
        return usuario

    def cerrar_sesion(self) -> None:
        self._usuario_actual = None

    def tiene_permiso(self, permiso: str) -> bool:
        return self.sesion_activa and self._usuario_actual.tiene_permiso(permiso)

    def requiere_permiso(self, permiso: str) -> None:
        """Se llama antes de ejecutar cualquier operación protegida."""
        if not self.sesion_activa:
            raise PermissionError("Debe iniciar sesión.")
        if not self._usuario_actual.tiene_permiso(permiso):
            raise PermissionError("No tiene permisos para realizar esta operación.")