"""Menú principal, inicio de sesión y menús por rol (HU-007).

Conecta el inicio de sesión con las pantallas del sistema. Las reglas de
acceso viven en Autenticacion y Usuario; aquí solo se decide qué opción
llama a qué pantalla. Con la sesión abierta, el usuario responsable de las
entradas y salidas es el de la sesión.
"""
from consola.menu_actualizar import menu_actualizar
from consola.menu_agotados import mostrar_agotados
from consola.menu_buscar import menu_buscar
from consola.menu_entrada import menu_entrada
from consola.menu_exportar import menu_exportar
from consola.menu_historial import menu_historial
from consola.menu_inventario import mostrar_inventario
from consola.menu_productos import menu_registrar_producto
from consola.menu_reportes import menu_reportes
from consola.menu_salidas import menu_registrar_salida
from consola.menu_sesion import flujo_sesion
from consola.menu_usuarios import crear_primer_administrador, menu_registrar_usuario
from modelos.usuario import ROL_ADMINISTRADOR


def _submenu(titulo, opciones, entrada, salida):
    """Muestra opciones numeradas [(texto, función)] hasta elegir 0 (volver)."""
    while True:
        salida(f"\n--- {titulo} ---")
        for numero, (texto, _) in enumerate(opciones, start=1):
            salida(f"{numero}. {texto}")
        salida("0. Volver")

        eleccion = entrada("Seleccione una opción: ").strip()
        if eleccion == "0":
            return
        if not eleccion.isdigit() or not 1 <= int(eleccion) <= len(opciones):
            salida("Opción inválida.")
            continue
        opciones[int(eleccion) - 1][1]()


def _solo_administrador(auth, accion):
    """Envuelve una acción para que solo la ejecute un administrador."""
    def protegida():
        if auth.usuario_actual.rol != ROL_ADMINISTRADOR:
            print("Acceso denegado: esta función es exclusiva del administrador.")
            return
        accion()
    return protegida


def _submenu_inventario(gestor, auth, entrada, salida):
    usuario = auth.usuario_actual.nombre_usuario

    opciones = [
        ("Buscar productos", lambda: menu_buscar(gestor)),
        ("Registrar entrada de mercancía", lambda: menu_entrada(gestor, usuario)),
        ("Registrar salida de mercancía",
         lambda: menu_registrar_salida(gestor, usuario)),
    ]
    if auth.usuario_actual.rol == ROL_ADMINISTRADOR:
        opciones = [
            ("Registrar producto", _solo_administrador(
                auth, lambda: menu_registrar_producto(gestor))),
            ("Actualizar producto", _solo_administrador(
                auth, lambda: menu_actualizar(gestor))),
        ] + opciones

    _submenu("GESTIONAR INVENTARIO", opciones, entrada, salida)


def _submenu_reportes(gestor, entrada, salida):
    opciones = [
        ("Reportes de inventario", lambda: menu_reportes(gestor)),
        ("Historial de movimientos", lambda: menu_historial(gestor)),
        ("Exportar a CSV", lambda: menu_exportar(gestor)),
    ]
    _submenu("REPORTES", opciones, entrada, salida)


def construir_acciones(gestor, auth, usuarios, entrada, salida,
                       leer_contrasena=None):
    """Diccionario {permiso: función} que usa menu_sesion.flujo_sesion."""
    return {
        "registrar_usuarios": lambda: menu_registrar_usuario(
            usuarios, auth.usuario_actual, entrada, salida, leer_contrasena),
        "gestionar_inventario": lambda: _submenu_inventario(
            gestor, auth, entrada, salida),
        "ver_reportes": lambda: _submenu_reportes(gestor, entrada, salida),
        "consultar_agotados": lambda: mostrar_agotados(gestor, salida),
        "consultar_inventario": lambda: mostrar_inventario(gestor, salida),
    }


def menu_principal(gestor, auth, usuarios, entrada=None, salida=None,
                   leer_contrasena=None):
    """Menú inicial: iniciar sesión o salir. Cerrar sesión regresa aquí."""
    entrada = entrada or input
    salida = salida or print

    if not usuarios:
        salida("\nTodavía no hay usuarios registrados.")
        if crear_primer_administrador(usuarios, entrada, salida,
                                      leer_contrasena) is None:
            return

    acciones = construir_acciones(gestor, auth, usuarios, entrada, salida,
                                  leer_contrasena)

    while True:
        salida("\n===== SISTEMA DE INVENTARIO =====")
        salida("1. Iniciar sesión")
        salida("0. Salir")

        opcion = entrada("Seleccione una opción: ").strip()

        if opcion == "1":
            flujo_sesion(auth, acciones, entrada, salida)
        elif opcion == "0":
            return
        else:
            salida("Opción inválida.")
