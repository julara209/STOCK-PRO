"""Consola de reportes de inventario (HU-010). Usa input()/print();
los cálculos están en reportes.py."""
import reportes
from constantes import TIPO_ENTRADA, TIPO_SALIDA


def _imprimir_productos(productos):
    print(f"{'Código':<10}{'Nombre':<25}{'Categoría':<15}{'Stock':>8}")
    print("-" * 58)
    for p in productos:
        print(f"{p.codigo:<10}{p.nombre:<25}{p.categoria:<15}{p.cantidad:>8}")


def _datos(gestor):
    productos = gestor.consultar_productos()
    # Si todavía no existe el historial de movimientos, se trata como vacío.
    movimientos = list(getattr(gestor, "movimientos", []))
    return productos, movimientos


def mostrar_resumen(gestor):
    productos, movimientos = _datos(gestor)

    if not productos:
        print("\nNo hay productos registrados.")
        return

    r = reportes.resumen_inventario(productos, movimientos)

    print("\n===== RESUMEN DEL INVENTARIO =====")
    print(f"Productos registrados: {r['total_productos']}")
    print(f"Unidades en existencia: {r['unidades_totales']}")
    print(f"Valor total del inventario: ${r['valor_total']:.2f}")

    print(f"\nProductos con existencias bajas (1 a {r['umbral']} unidades):")
    if r["stock_bajo"]:
        _imprimir_productos(r["stock_bajo"])
    else:
        print("Ninguno.")

    print("\nProductos agotados:")
    if r["agotados"]:
        _imprimir_productos(r["agotados"])
    else:
        print("Ninguno.")

    print("\nMovimientos registrados:")
    print(f"Entradas: {r['total_entradas']} ({r['unidades_entradas']} unidades)")
    print(f"Salidas: {r['total_salidas']} ({r['unidades_salidas']} unidades)")


def mostrar_stock_bajo(gestor):
    productos, _ = _datos(gestor)
    if not productos:
        print("\nNo hay productos registrados.")
        return

    bajos = reportes.productos_con_stock_bajo(productos)
    print("\n--- Productos con existencias bajas ---")
    if not bajos:
        print("No hay productos con existencias bajas.")
    else:
        _imprimir_productos(bajos)


def mostrar_agotados(gestor):
    productos, _ = _datos(gestor)
    if not productos:
        print("\nNo hay productos registrados.")
        return

    agotados = reportes.productos_agotados(productos)
    print("\n--- Productos agotados ---")
    if not agotados:
        print("No hay productos agotados.")
    else:
        _imprimir_productos(agotados)


def mostrar_movimientos(gestor):
    _, movimientos = _datos(gestor)
    if not movimientos:
        print("\nNo hay movimientos registrados.")
        return

    print("\n1. Todos   2. Solo entradas   3. Solo salidas")
    opcion = input("Seleccione qué movimientos ver: ").strip()
    tipos = {"1": None, "2": TIPO_ENTRADA, "3": TIPO_SALIDA}

    if opcion not in tipos:
        print("Opción inválida.")
        return

    seleccion = reportes.filtrar_movimientos(movimientos, tipos[opcion])
    print("\n--- Movimientos ---")
    if not seleccion:
        print("No hay movimientos de ese tipo.")
        return
    for movimiento in seleccion:
        print(movimiento)


def menu_reportes(gestor):
    # Provisional: cuando exista el inicio de sesión (HU-007), este menú
    # solo estará disponible para el administrador.
    while True:
        print("\n===== REPORTES DE INVENTARIO =====")
        print("1. Resumen general")
        print("2. Productos con existencias bajas")
        print("3. Productos agotados")
        print("4. Movimientos de entrada y salida")
        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            mostrar_resumen(gestor)
        elif opcion == "2":
            mostrar_stock_bajo(gestor)
        elif opcion == "3":
            mostrar_agotados(gestor)
        elif opcion == "4":
            mostrar_movimientos(gestor)
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")
