"""Servicio de registro y validación de usuarios (HU-004)."""
import re

from modelos.usuario import (
    ROL_ADMINISTRADOR,
    ROLES_VALIDOS,
    Usuario,
)

# Reglas de seguridad de la contraseña (ajustar o mover a constantes.py)
LONGITUD_MINIMA = 8


def validar_nombre_usuario(nombre: str, usuarios: list) -> None:
    if not nombre or not nombre.strip():
        raise ValueError("El nombre de usuario no puede estar vacío.")
    if any(u.nombre_usuario.lower() == nombre.strip().lower() for u in usuarios):
        raise ValueError("El nombre de usuario ya existe.")


def validar_contrasena(contrasena: str) -> None:
    if not contrasena or len(contrasena) < LONGITUD_MINIMA:
        raise ValueError(f"La contraseña debe tener al menos {LONGITUD_MINIMA} caracteres.")
    if not re.search(r"[A-Z]", contrasena):
        raise ValueError("La contraseña debe incluir una mayúscula.")
    if not re.search(r"[a-z]", contrasena):
        raise ValueError("La contraseña debe incluir una minúscula.")
    if not re.search(r"\d", contrasena):
        raise ValueError("La contraseña debe incluir un número.")


def validar_rol(rol: str) -> None:
    if rol not in ROLES_VALIDOS:
        raise ValueError("Rol inválido: debe ser Administrador o Empleado.")


def validar_permiso_solicitante(solicitante, rol_nuevo: str) -> None:
    """Un empleado no puede crear administradores ni otorgarse permisos."""
    if solicitante is not None and solicitante.rol != ROL_ADMINISTRADOR:
        raise PermissionError("Solo un administrador puede registrar usuarios.")


def registrar_usuario(usuarios: list, nombre: str, contrasena: str, rol: str,
                      solicitante: Usuario = None) -> Usuario:
    """Registra un usuario. Si falla, lanza excepción y NO modifica la lista.

    `solicitante=None` se permite solo para crear el primer administrador
    (lista vacía); en cualquier otro caso se exige un administrador.
    """
    if solicitante is None and usuarios:
        raise PermissionError("Se requiere un administrador autenticado.")
    if solicitante is None and rol != ROL_ADMINISTRADOR:
        raise PermissionError("El primer usuario debe ser Administrador.")

    validar_permiso_solicitante(solicitante, rol)
    validar_nombre_usuario(nombre, usuarios)
    validar_contrasena(contrasena)
    validar_rol(rol)

    nuevo = Usuario(nombre.strip(), contrasena, rol)
    usuarios.append(nuevo)  # solo se llega aquí si todo fue válido
    return nuevo


def iniciar_sesion(usuarios: list, nombre: str, contrasena: str):
    """Devuelve el Usuario si las credenciales son correctas, si no None."""
    for u in usuarios:
        if u.nombre_usuario.lower() == nombre.strip().lower():
            return u if u.verificar_contrasena(contrasena) else None
    return None