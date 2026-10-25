"""Pantallas de consola para registrar usuarios (HU-004).
Usa input()/print(); las reglas están en servicios/usuarios.py."""
import getpass

from modelos.usuario import ROL_ADMINISTRADOR, ROL_EMPLEADO
from servicios.usuarios import registrar_y_guardar


def crear_primer_administrador(usuarios, entrada=None, salida=None,
                               leer_contrasena=None):
    entrada = entrada or input
    salida = salida or print
    leer_contrasena = leer_contrasena or getpass.getpass

    salida("\n--- Crear el primer administrador ---")
    while True:
        nombre = entrada("Nombre de usuario (Enter para cancelar): ").strip()
        if not nombre:
            return None
        contrasena = leer_contrasena("Contraseña: ")
        try:
            nuevo = registrar_y_guardar(usuarios, nombre, contrasena,
                                        ROL_ADMINISTRADOR)
        except (ValueError, PermissionError) as error:
            salida(f"\nRegistro rechazado: {error}")
        except OSError as error:
            salida(f"\nError al guardar: {error}")
        else:
            salida("\nAdministrador creado correctamente.")
            return nuevo


def menu_registrar_usuario(usuarios, solicitante, entrada=None, salida=None,
                           leer_contrasena=None):
    """Registra un usuario nuevo. El solicitante debe ser un administrador."""
    entrada = entrada or input
    salida = salida or print
    leer_contrasena = leer_contrasena or getpass.getpass

    salida("\n--- Registrar usuario ---")
    nombre = entrada("Nombre de usuario: ").strip()
    contrasena = leer_contrasena("Contraseña: ")
    opcion = entrada("Rol: 1. Empleado  2. Administrador (Enter = Empleado): ").strip()

    roles = {"": ROL_EMPLEADO, "1": ROL_EMPLEADO, "2": ROL_ADMINISTRADOR}
    if opcion not in roles:
        salida("\nRegistro rechazado: Rol inválido: debe ser Administrador o Empleado.")
        return None

    try:
        nuevo = registrar_y_guardar(usuarios, nombre, contrasena, roles[opcion],
                                    solicitante)
    except (ValueError, PermissionError) as error:
        salida(f"\nRegistro rechazado: {error}")
        return None
    except OSError as error:
        salida(f"\nError al guardar: {error}")
        return None

    salida(f"\nUsuario '{nuevo.nombre_usuario}' registrado como {nuevo.rol}.")
    return nuevo
