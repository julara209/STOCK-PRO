"""Reportes de inventario (HU-010).

Son funciones puras: reciben las listas de productos y movimientos y devuelven
datos calculados. No usan input() ni print(), y no modifican nada.
"""
from constantes import STOCK_BAJO, TIPO_ENTRADA, TIPO_SALIDA


def productos_agotados(productos):
    """Productos con existencias iguales a cero, ordenados por código."""
    agotados = [p for p in productos if p.cantidad == 0]
    return sorted(agotados, key=lambda p: p.codigo)


def productos_con_stock_bajo(productos, umbral=STOCK_BAJO):
    """Productos con existencias entre 1 y el umbral (incluido).

    Los agotados (0) no se incluyen aquí: tienen su propio reporte.
    """
    bajos = [p for p in productos if 0 < p.cantidad <= umbral]
    return sorted(bajos, key=lambda p: p.codigo)


def filtrar_movimientos(movimientos, tipo=None):
    """Devuelve los movimientos de un tipo, o todos si tipo es None.

    Conserva el orden en que fueron registrados.
    """
    if tipo is not None and tipo not in (TIPO_ENTRADA, TIPO_SALIDA):
        raise ValueError(
            f"El tipo debe ser '{TIPO_ENTRADA}' o '{TIPO_SALIDA}'."
        )
    return [m for m in movimientos if tipo is None or m.tipo == tipo]


def resumen_inventario(productos, movimientos=(), umbral=STOCK_BAJO):
    """Calcula el resumen general del inventario. Devuelve un diccionario."""
    productos = list(productos)
    movimientos = list(movimientos)

    entradas = filtrar_movimientos(movimientos, TIPO_ENTRADA)
    salidas = filtrar_movimientos(movimientos, TIPO_SALIDA)

    return {
        "total_productos": len(productos),
        "unidades_totales": sum(p.cantidad for p in productos),
        "valor_total": round(sum(p.precio * p.cantidad for p in productos), 2),
        "umbral": umbral,
        "stock_bajo": productos_con_stock_bajo(productos, umbral),
        "agotados": productos_agotados(productos),
        "total_entradas": len(entradas),
        "unidades_entradas": sum(m.cantidad for m in entradas),
        "total_salidas": len(salidas),
        "unidades_salidas": sum(m.cantidad for m in salidas),
    }
