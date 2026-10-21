## Sistema de inventario - Tienda de abarrotes

Aplicación de consola en Python con roles de Administrador y Empleado.

### Estructura
- `main.py`: menús e interacción por consola
- `modelos.py`: Producto, Usuario, Movimiento
- `gestor.py`: GestorInventario (reglas de negocio)
- `autenticacion.py`: login y permisos
- `almacenamiento.py`: persistencia JSON
- `reportes.py`: reportes y exportación CSV
- `constantes.py`: constantes globales
- `tests/`: pruebas automatizadas

### Ejecutar
python main.py

### Pruebas
python -m unittest discover -s tests -t .