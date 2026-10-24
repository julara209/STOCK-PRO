"""Consola de búsqueda de productos (HU-003). Usa input()/print();
las reglas de negocio están en servicios/busqueda.py."""


def mostrar_productos(productos):
    if not productos:
        print("No se encontraron productos.")
        return
    print(f"{'Código':<10}{'Nombre':<25}{'Categoría':<15}{'Precio':>10}{'Stock':>8}")
    print("-" * 68)
    for p in productos:
        print(f"{p.codigo:<10}{p.nombre:<25}{p.categoria:<15}"
              f"{p.precio:>10.2f}{p.cantidad:>8}")


def menu_buscar(gestor):
    print("\n--- Buscar productos (Enter para omitir un criterio) ---")
    codigo = input("Código exacto: ").strip()
    nombre = input("Nombre (o parte): ").strip()
    categoria = input("Categoría: ").strip()
    try:
        resultados = gestor.buscar_productos(codigo or None, nombre or None,
                                             categoria or None)
    except ValueError as error:
        print(f"Búsqueda rechazada: {error}")
        return
    mostrar_productos(resultados)
