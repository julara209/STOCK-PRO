"""Búsqueda de productos (HU-003). No modifica el inventario."""


def buscar_productos(productos, codigo=None, nombre=None, categoria=None):
    """Filtra una lista de Producto según los criterios indicados.

    - codigo: coincidencia exacta.
    - nombre: contiene el texto, sin distinguir mayúsculas.
    - categoria: igual, sin distinguir mayúsculas.
    Los criterios indicados se combinan (todos deben cumplirse).
    Devuelve una lista nueva ordenada por código; vacía si no hay resultados.
    """
    if not any((codigo, nombre, categoria)):
        raise ValueError("Indique al menos un criterio de búsqueda.")

    codigo = codigo.strip() if codigo else None
    nombre = nombre.strip().lower() if nombre else None
    categoria = categoria.strip().lower() if categoria else None

    resultados = []
    for producto in productos:
        if codigo and producto.codigo != codigo:
            continue
        if nombre and nombre not in producto.nombre.lower():
            continue
        if categoria and producto.categoria.lower() != categoria:
            continue
        resultados.append(producto)
    return sorted(resultados, key=lambda p: p.codigo)
