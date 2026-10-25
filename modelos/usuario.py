"""Modelo Usuario (HU-004 · Registrar Usuarios)."""
import hashlib
import hmac
import os

ROL_ADMINISTRADOR = "Administrador"
ROL_EMPLEADO = "Empleado"
ROLES_VALIDOS = (ROL_ADMINISTRADOR, ROL_EMPLEADO)

# Permisos por rol
PERMISOS = {
    ROL_ADMINISTRADOR: {"registrar_usuarios", "gestionar_inventario", "ver_reportes",
                        "consultar_agotados", "consultar_inventario"},
    ROL_EMPLEADO: {"gestionar_inventario", "consultar_agotados", "consultar_inventario"},
}

_ITERACIONES = 100_000


def generar_hash(contrasena: str, sal: bytes = None):
    """Devuelve (hash_hex, sal_hex) usando PBKDF2-HMAC-SHA256."""
    sal = sal if sal is not None else os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, _ITERACIONES)
    return digest.hex(), sal.hex()


class Usuario:
    def __init__(self, nombre_usuario: str, contrasena: str, rol: str):
        if rol not in ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {rol}")
        self.nombre_usuario = nombre_usuario
        self.rol = rol
        # La contraseña nunca se guarda en texto plano
        self._hash, self._sal = generar_hash(contrasena)

    @property
    def permisos(self) -> set:
        return set(PERMISOS[self.rol])

    def tiene_permiso(self, permiso: str) -> bool:
        return permiso in PERMISOS[self.rol]

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

        usuario = cls.__new__(cls)  # no se llama a __init__: no hay contraseña que hashear
        usuario.nombre_usuario = nombre
        usuario.rol = rol
        usuario._hash = hash_hex
        usuario._sal = sal_hex
        return usuario

    def __repr__(self):
        return f"Usuario({self.nombre_usuario!r}, rol={self.rol!r})"