"""Inicio de sesión y menús por rol (HU-007).

`entrada` y `salida` se inyectan para poder probar sin teclado real.
"""
from servicios.autenticacion import ErrorAutenticacion
from modelos.usuario import ROL_ADMINISTRADOR

# (tecla, texto, permiso requerido)
OPCIONES_ADMINISTRADOR = [
    ("1", "Registrar usuario", "registrar_usuarios"),
    ("2", "Gestionar inventario", "gestionar_inventario"),
    ("3", "Ver reportes", "ver_reportes"),
    ("4", "Consultar inventario", "consultar_inventario"),
    ("0", "Cerrar sesión", None),
]
OPCIONES_EMPLEADO = [
    ("1", "Gestionar inventario", "gestionar_inventario"),
    ("2", "Consultar productos agotados", "consultar_agotados"),
    ("3", "Consultar inventario", "consultar_inventario"),
    ("0", "Cerrar sesión", None),
]


def pedir_credenciales(auth, entrada=input, salida=print, max_intentos=3):
    """Pide usuario y contraseña. Devuelve el usuario o None si agota los intentos."""
    for restantes in range(max_intentos, 0, -1):
        nombre = entrada("Usuario: ")
        contrasena = entrada("Contraseña: ")
        try:
            return auth.iniciar_sesion(nombre, contrasena)
        except ErrorAutenticacion as e:
            salida(f"Error: {e} Intentos restantes: {restantes - 1}")
    salida("Demasiados intentos fallidos. Volviendo al menú principal.")
    return None


def opciones_del_rol(usuario):
    if usuario.rol == ROL_ADMINISTRADOR:
        return OPCIONES_ADMINISTRADOR
    return OPCIONES_EMPLEADO


def menu_por_rol(auth, acciones=None, entrada=input, salida=print):
    """Muestra el menú del rol hasta que el usuario cierre sesión.

    `acciones` es un dict {permiso: función} para conectar las pantallas
    existentes (menu_entrada, menu_reportes, menu_usuarios, ...).
    """
    acciones = acciones or {}
    usuario = auth.usuario_actual
    opciones = opciones_del_rol(usuario)
    titulo = usuario.titulo_menu()

    while True:
        salida(f"\n=== {titulo} ({usuario.nombre_usuario}) ===")
        for tecla, texto, _ in opciones:
            salida(f"{tecla}. {texto}")
        eleccion = entrada("Seleccione una opción: ").strip()

        seleccion = next((o for o in opciones if o[0] == eleccion), None)
        if seleccion is None:
            salida("Opción no válida. Intente de nuevo.")
            continue

        _, _, permiso = seleccion
        if permiso is None:  # cerrar sesión
            auth.cerrar_sesion()
            salida("Sesión cerrada.")
            return

        try:
            auth.requiere_permiso(permiso)  
        except PermissionError as e:
            salida(f"Acceso denegado: {e}")
            continue

        accion = acciones.get(permiso)
        if accion:
            accion()
        else:
            salida("(Función aún no conectada a este menú)")


def flujo_sesion(auth, acciones=None, entrada=input, salida=print):
    """Login + menú del rol. Al terminar, el control vuelve al menú principal."""
    if pedir_credenciales(auth, entrada, salida):
        menu_por_rol(auth, acciones, entrada, salida)