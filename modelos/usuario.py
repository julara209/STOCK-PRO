"""Modelo Usuario (HU-004 · Registrar Usuarios)."""
import hashlib
import hmac
import os

ROL_ADMINISTRADOR = "Administrador"
ROL_EMPLEADO = "Empleado"
ROLES_VALIDOS = (ROL_ADMINISTRADOR, ROL_EMPLEADO)

_ITERACIONES = 100_000


def generar_hash(contrasena: str, sal: bytes = None):
    """Devuelve (hash_hex, sal_hex) usando PBKDF2-HMAC-SHA256."""
    sal = sal if sal is not None else os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, _ITERACIONES)
    return digest.hex(), sal.hex()


class Usuario:
    """Clase base de los usuarios del sistema.

    No se crea directamente: cada rol es una subclase (Administrador, Empleado)
    que sobrescribe `permisos` y `titulo_menu`. El resto del programa solo
    pregunta `tiene_permiso(...)`, sin comparar roles (polimorfismo).
    """

    ROL = None  # lo define cada subclase

    def __init__(self, nombre_usuario: str, contrasena: str):
        if self.ROL is None:
            raise TypeError("Usuario es una clase base: use Administrador o Empleado.")
        self.nombre_usuario = nombre_usuario
        self.rol = self.ROL
        # La contraseña nunca se guarda en texto plano
        self._hash, self._sal = generar_hash(contrasena)

    @property
    def permisos(self) -> set:
        raise NotImplementedError("Cada rol define sus permisos.")

    def titulo_menu(self) -> str:
        raise NotImplementedError("Cada rol define el título de su menú.")

    def tiene_permiso(self, permiso: str) -> bool:
        return permiso in self.permisos

    def verificar_contrasena(self, contrasena: str) -> bool:
        hash_calculado, _ = generar_hash(contrasena, bytes.fromhex(self._sal))
        return hmac.compare_digest(hash_calculado, self._hash)

    def to_dict(self) -> dict:
        """Datos para el JSON. Guarda el hash y la sal, nunca la contraseña."""
        return {
            "nombre_usuario": self.nombre_usuario,
            "rol": self.rol,
            "hash": self._hash,
            "sal": self._sal,
        }

    @classmethod
    def from_dict(cls, datos: dict):
        """Reconstruye un usuario guardado. Lanza ValueError si los datos no sirven."""
        try:
            nombre = datos["nombre_usuario"]
            rol = datos["rol"]
            hash_hex = datos["hash"]
            sal_hex = datos["sal"]
            bytes.fromhex(hash_hex)
            bytes.fromhex(sal_hex)
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Los datos de un usuario guardado están incompletos o dañados.") from error

        if rol not in ROLES_VALIDOS or not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("Los datos de un usuario guardado están incompletos o dañados.")

        clase = CLASES_POR_ROL[rol]  # la subclase se elige según el rol guardado
        usuario = clase.__new__(clase)  # no se llama a __init__: no hay contraseña que hashear
        usuario.nombre_usuario = nombre
        usuario.rol = rol
        usuario._hash = hash_hex
        usuario._sal = sal_hex
        return usuario

    def __repr__(self):
        return f"{type(self).__name__}({self.nombre_usuario!r})"


class Empleado(Usuario):
    ROL = ROL_EMPLEADO

    @property
    def permisos(self) -> set:
        return {"gestionar_inventario", "consultar_agotados", "consultar_inventario"}

    def titulo_menu(self) -> str:
        return "MENÚ DE EMPLEADO"


class Administrador(Usuario):
    ROL = ROL_ADMINISTRADOR

    @property
    def permisos(self) -> set:
        return {"registrar_usuarios", "gestionar_inventario", "ver_reportes",
                "consultar_agotados", "consultar_inventario"}

    def titulo_menu(self) -> str:
        return "MENÚ DE ADMINISTRACIÓN"


CLASES_POR_ROL = {
    ROL_ADMINISTRADOR: Administrador,
    ROL_EMPLEADO: Empleado,
}


def crear_usuario(nombre_usuario: str, contrasena: str, rol: str) -> Usuario:
    """Crea el tipo de usuario que corresponde al rol (Administrador o Empleado)."""
    if rol not in ROLES_VALIDOS:
        raise ValueError(f"Rol inválido: {rol}")
    return CLASES_POR_ROL[rol](nombre_usuario, contrasena)
