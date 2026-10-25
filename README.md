# STOCK-PRO

## Sistema de inventario - Tienda de abarrotes

Aplicación de consola en Python con roles de Administrador y Empleado. Los datos se
guardan en `data/inventario.json` y los reportes se pueden exportar a CSV.

### Estructura
- `main.py`: punto de entrada (carga los datos y abre el menú principal)
- `constantes.py`: constantes globales
- `modelos/`: entidades del dominio (`producto`, `usuario`, `movimiento`)
- `servicios/`: reglas de negocio (`inventario`, `busqueda`, `actualizacion`, `salidas`, `usuarios`, `autenticacion`)
- `consola/`: menús e interacción con el usuario (`menu_principal`, `menu_sesion`, `menu_productos`, `menu_buscar`, `menu_actualizar`, `menu_entrada`, `menu_salidas`, `menu_inventario`, `menu_agotados`, `menu_historial`, `menu_reportes`, `menu_exportar`, `menu_usuarios`)
- `almacenamiento.py`: persistencia en JSON (productos, usuarios y movimientos)
- `reportes.py`: cálculos de los reportes de inventario
- `exportacion.py`: exportación a CSV (carpeta `exportaciones/`)
- `tests/`: pruebas automatizadas

### Primer uso
1. Ejecuta `python main.py`.
2. Si todavía no hay usuarios, el programa pide crear el **primer administrador**.
3. Inicia sesión con ese usuario. Desde el menú de administración puedes registrar
   empleados, gestionar el inventario y ver reportes.

### Qué puede hacer cada rol
| Función | Administrador | Empleado |
|---|---|---|
| Registrar usuarios | Sí | No |
| Registrar y actualizar productos | Sí | No |
| Buscar productos | Sí | Sí |
| Registrar entradas y salidas | Sí | Sí |
| Consultar inventario completo | Sí | Sí |
| Consultar productos agotados | Sí | Sí |
| Reportes, historial y exportar a CSV | Sí | No |

### Ejecutar
```
python main.py
```

### Pruebas
```
python -m unittest discover -s tests -t .
```
