"""Persistencia en JSON para productos, usuarios y movimientos."""

import json
from pathlib import Path

from constantes import ARCHIVO_DATOS


def _estado_vacio():
    return {
        "productos": [],
        "usuarios": [],
        "movimientos": []
    }


def _cargar_estado():
    ruta = Path(ARCHIVO_DATOS)

    if not ruta.exists():
        return _estado_vacio()

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"El archivo {ruta} está dañado. "
            "No se modificarán los datos."
        ) from error
    except OSError as error:
        raise OSError(
            f"No se pudo leer el archivo {ruta}: {error}"
        ) from error

    # Compatibilidad con el formato anterior:
    # una lista que contiene únicamente productos.
    if isinstance(datos, list):
        return {
            "productos": datos,
            "usuarios": [],
            "movimientos": []
        }

    if not isinstance(datos, dict):
        raise ValueError(
            f"El archivo {ruta} tiene una estructura inválida. "
            "No se modificarán los datos."
        )

    for clave in ("productos", "usuarios", "movimientos"):
        if clave not in datos or not isinstance(datos[clave], list):
            raise ValueError(
                f"El archivo {ruta} tiene una estructura inválida. "
                f"Falta la sección '{clave}' o no es una lista."
            )

    return datos


def _guardar_estado(estado):
    ruta = Path(ARCHIVO_DATOS)

    # Comprobar primero que el archivo existente se pueda leer.
    # Si está dañado, no se abre para escritura.
    _cargar_estado()

    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(
                estado,
                archivo,
                ensure_ascii=False,
                indent=4
            )
    except OSError as error:
        raise OSError(
            f"No se pudo guardar el archivo {ruta}: {error}"
        ) from error


def cargar():
    """Devuelve los productos guardados."""
    return _cargar_estado()["productos"]


def guardar(datos):
    """Guarda los productos sin eliminar usuarios ni movimientos."""
    if not isinstance(datos, list):
        raise ValueError("Los productos deben proporcionarse en una lista.")

    estado = _cargar_estado()
    estado["productos"] = datos

    _guardar_estado(estado)


def cargar_usuarios():
    """Devuelve los usuarios guardados."""
    return _cargar_estado()["usuarios"]


def guardar_usuarios(usuarios):
    """Guarda los usuarios sin eliminar productos ni movimientos."""
    if not isinstance(usuarios, list):
        raise ValueError("Los usuarios deben proporcionarse en una lista.")

    estado = _cargar_estado()
    estado["usuarios"] = usuarios

    _guardar_estado(estado)


def cargar_movimientos():
    """Devuelve el historial de movimientos guardado."""
    return _cargar_estado()["movimientos"]


def guardar_movimientos(movimientos):
    """Guarda los movimientos sin eliminar productos ni usuarios."""
    if not isinstance(movimientos, list):
        raise ValueError("Los movimientos deben proporcionarse en una lista.")

    estado = _cargar_estado()
    estado["movimientos"] = movimientos

    _guardar_estado(estado)