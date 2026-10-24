"""Persistencia en JSON: guardar() y cargar() sobre data/inventario.json."""


import json
from pathlib import Path

from constantes import ARCHIVO_DATOS, ARCHIVO_MOVIMIENTOS

def cargar():
    ruta = Path(ARCHIVO_DATOS)

    if not ruta.exists():
        return []

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar(datos):
    ruta = Path(ARCHIVO_DATOS)

    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def cargar_movimientos():
    ruta = Path(ARCHIVO_MOVIMIENTOS)

    if not ruta.exists():
        return []

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_movimientos(datos):
    ruta = Path(ARCHIVO_MOVIMIENTOS)

    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)