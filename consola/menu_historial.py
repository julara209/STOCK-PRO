"""Menú de consulta del historial de movimientos."""

def menu_historial(inventario):
    print("\n===== HISTORIAL DE MOVIMIENTOS =====")
    print("1. Consultar todo el historial")
    print("2. Buscar por producto")
    print("3. Filtrar por tipo de movimiento")
    print("4. Buscar por producto y tipo")
    print("0. Volver")

    opcion = input("Seleccione una opción: ").strip()

    if opcion == "0":
        return

    codigo = None
    tipo = None

    if opcion in ("2", "4"):
        codigo = input("Código del producto: ").strip()

        if not codigo:
            print("Debe ingresar el código del producto.")
            return

    if opcion in ("3", "4"):
        print("Tipos disponibles: Entrada, Salida")
        tipo = input("Tipo de movimiento: ").strip()

        if tipo.lower() not in ("entrada", "salida"):
            print("El tipo debe ser Entrada o Salida.")
            return

        tipo = tipo.capitalize()

    if opcion not in ("1", "2", "3", "4"):
        print("Opción inválida.")
        return

    movimientos = inventario.consultar_historial_movimientos(
        codigo_producto=codigo,
        tipo=tipo
    )

    if not movimientos:
        print("\nNo hay movimientos que coincidan con la consulta.")
        return

    print(f"\nMovimientos encontrados: {len(movimientos)}")

    for movimiento in movimientos:
        print("-" * 70)
        print(f"ID: {movimiento.get('id_movimiento', 'Sin ID')}")
        print(f"Tipo: {movimiento.get('tipo', 'No disponible')}")
        print(
            "Producto: "
            f"{movimiento.get('nombre_producto', movimiento.get('codigo_producto', 'No disponible'))}"
        )
        print(f"Código: {movimiento.get('codigo_producto', movimiento.get('codigo', 'No disponible'))}")
        print(f"Cantidad: {movimiento.get('cantidad', 'No disponible')}")
        print(f"Fecha: {movimiento.get('fecha', 'No disponible')}")
        print(
            "Responsable: "
            f"{movimiento.get('usuario_responsable', 'No disponible')}"
        )

    print("-" * 70)