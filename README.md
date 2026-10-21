## Sistema de inventario - Tienda de abarrotes

Aplicación de consola en Python con roles de Administrador y Empleado.

### Estructura
- `main.py`: punto de entrada
- `constantes.py`: constantes globales
- `modelos/`: entidades del dominio (producto, usuario, movimiento)
- `servicios/`: reglas de negocio (inventario, autenticación)
- `consola/`: menús e interacción con el usuario
- `almacenamiento.py`: persistencia JSON
- `reportes.py`: reportes y exportación CSV
- `tests/`: pruebas automatizadas

### Ejecutar
python main.py

### Pruebas
python -m unittest discover -s tests -t .