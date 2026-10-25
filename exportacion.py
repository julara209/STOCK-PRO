"""Exportación de información a archivos CSV (HU-013).

El CSV es solo para exportar y compartir; la persistencia principal de la
aplicación sigue siendo el archivo JSON. Las funciones solo leen los datos que
reciben: nunca modifican el inventario ni el JSON.
"""
import csv
from datetime import datetime
from pathlib import Path

from constantes import CARPETA_EXPORTACIONES

# Si al abrir el CSV en Excel todo aparece en una sola columna (según la
# configuración regional), cambiar el delimitador a ";".
DELIMITADOR = ","

ENCABEZADO_INVENTARIO = ["codigo", "nombre", "categoria", "precio", "cantidad"]
ENCABEZADO_MOVIMIENTOS = [
    "id_movimiento", "fecha", "tipo", "codigo_producto", "cantidad", "usuario",
]


def _ruta_libre(carpeta, prefijo, ahora):
    """Ruta con fecha y hora en el nombre. Si ya existe, agrega _2, _3, ...

    Así una exportación nunca sobrescribe a otra anterior.
    """
    marca = ahora.strftime("%Y%m%d_%H%M%S")
    ruta = Path(carpeta) / f"{prefijo}_{marca}.csv"

    contador = 2
    while ruta.exists():
        ruta = Path(carpeta) / f"{prefijo}_{marca}_{contador}.csv"
        contador += 1

    return ruta


def _escribir_csv(ruta, encabezado, filas):
    ruta.parent.mkdir(parents=True, exist_ok=True)

    try:
        # utf-8-sig agrega una marca al inicio para que Excel muestre bien
        # las tildes y la ñ. newline="" evita líneas en blanco en Windows.
        with open(ruta, "w", encoding="utf-8-sig", newline="") as archivo:
            escritor = csv.writer(archivo, delimiter=DELIMITADOR)
            escritor.writerow(encabezado)
            escritor.writerows(filas)
    except OSError:
        # Si falla a mitad de camino, no se deja un archivo incompleto.
        try:
            ruta.unlink()
        except OSError:
            pass
        raise


def exportar_inventario_csv(productos, carpeta=None, ahora=None):
    """Exporta el inventario a un CSV y devuelve la ruta del archivo.

    Lanza ValueError (sin crear ningún archivo) si no hay productos, y
    OSError si no se puede escribir el archivo.
    """
    productos = list(productos)
    if not productos:
        raise ValueError("No hay productos para exportar.")

    carpeta = carpeta or CARPETA_EXPORTACIONES
    ruta = _ruta_libre(carpeta, "inventario", ahora or datetime.now())

    filas = [
        [p.codigo, p.nombre, p.categoria, f"{p.precio:.2f}", p.cantidad]
        for p in sorted(productos, key=lambda p: p.codigo)
    ]
    _escribir_csv(ruta, ENCABEZADO_INVENTARIO, filas)
    return ruta


def exportar_movimientos_csv(movimientos, carpeta=None, ahora=None):
    """Exporta el historial de movimientos a un CSV y devuelve la ruta.

    Conserva el orden en que se registraron los movimientos. Lanza ValueError
    (sin crear ningún archivo) si no hay movimientos.
    """
    movimientos = list(movimientos)
    if not movimientos:
        raise ValueError("No hay movimientos para exportar.")

    carpeta = carpeta or CARPETA_EXPORTACIONES
    ruta = _ruta_libre(carpeta, "movimientos", ahora or datetime.now())

    filas = [
        [m.id_movimiento, m.fecha, m.tipo, m.codigo_producto, m.cantidad, m.usuario]
        for m in movimientos
    ]
    _escribir_csv(ruta, ENCABEZADO_MOVIMIENTOS, filas)
    return ruta
