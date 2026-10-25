"""Pantalla de consola: inventario completo (HU-009)."""

ENCABEZADOS = ("Código", "Nombre", "Categoría", "Precio", "Existencias")


def _precio(valor) -> str:
    try:
        return f"${float(valor):,.2f}"
    except (TypeError, ValueError):
        return str(valor)


def formatear_tabla(productos) -> list:
    """Líneas de una tabla alineada: texto a la izquierda, números a la derecha."""
    filas = [
        (str(p.codigo), str(p.nombre), str(p.categoria),
         _precio(p.precio), str(p.cantidad))
        for p in productos
    ]
    anchos = [max(len(ENCABEZADOS[i]), *(len(f[i]) for f in filas)) for i in range(5)]
    numericas = (3, 4)

    def linea(f):
        return " | ".join(
            f[i].rjust(anchos[i]) if i in numericas else f[i].ljust(anchos[i])
            for i in range(5)
        )

    separador = "-+-".join("-" * a for a in anchos)
    return [linea(ENCABEZADOS), separador, *(linea(f) for f in filas)]


def mostrar_inventario(gestor, salida=print) -> None:
    productos = gestor.listar_productos()
    salida("\n=== INVENTARIO ===")
    if not productos:
        salida("No hay productos registrados.")
        return
    for linea in formatear_tabla(productos):
        salida(linea)
    salida(f"\nTotal de productos: {len(productos)}")