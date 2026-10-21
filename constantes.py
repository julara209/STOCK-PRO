"""Constantes globales del sistema de inventario."""
from pathlib import Path

ARCHIVO_DATOS = Path("data") / "inventario.json"
CARPETA_EXPORTACIONES = Path("exportaciones")

STOCK_BAJO = 5

ROL_ADMINISTRADOR = "Administrador"
ROL_EMPLEADO = "Empleado"
ROLES_VALIDOS = (ROL_ADMINISTRADOR, ROL_EMPLEADO)

TIPO_ENTRADA = "Entrada"
TIPO_SALIDA = "Salida"