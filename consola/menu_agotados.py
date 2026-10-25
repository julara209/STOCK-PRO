"""Pantalla de consola: productos agotados (HU-008)."""

ENCABEZADOS = ("Código", "Nombre", "Categoría")


def formatear_tabla(productos) -> list:
    """Devuelve las líneas de una tabla alineada con código, nombre y categoría."""
    filas = [(str(p.codigo), str(p.nombre), str(p.categoria)) for p in productos]
    anchos = [
        max(len(ENCABEZADOS[i]), *(len(f[i]) for f in filas)) for i in range(3)
    ]
    linea = lambda f: " | ".join(f[i].ljust(anchos[i]) for i in range(3))
    separador = "-+-".join("-" * a for a in anchos)
    return [linea(ENCABEZADOS), separador, *(linea(f) for f in filas)]


def mostrar_agotados(gestor, salida=print) -> None:
    agotados = gestor.productos_agotados()
    salida("\n=== PRODUCTOS AGOTADOS ===")
    if not agotados:
        salida("No hay productos agotados.")
        return
    for linea in formatear_tabla(agotados):
        salida(linea)
    salida(f"\nTotal agotados: {len(agotados)}")