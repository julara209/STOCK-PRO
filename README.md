# STOCK-PRO

Sistema de inventario de consola en Python para una **tienda de abarrotes**, con roles de
Administrador y Empleado. Proyecto integrador desarrollado con Scrum y GitHub.

## Problema que resuelve
Una tienda pequeña suele llevar el inventario en cuadernos u hojas sueltas: se pierde la cuenta de las
existencias, no se sabe quién sacó o recibió mercancía y es difícil saber qué reponer.
STOCK-PRO centraliza productos, entradas, salidas e historial, controla quién puede hacer cada cosa
y conserva todo en un archivo JSON entre ejecuciones.

## Usuarios
- **Administrador:** registra usuarios, gestiona productos, ve reportes e historial y exporta a CSV.
- **Empleado:** busca productos, registra entradas y salidas, consulta el inventario y los agotados.

| Función | Administrador | Empleado |
|---|---|---|
| Registrar usuarios | Sí | No |
| Registrar y actualizar productos | Sí | No |
| Buscar productos | Sí | Sí |
| Registrar entradas y salidas | Sí | Sí |
| Consultar inventario completo | Sí | Sí |
| Consultar productos agotados | Sí | Sí |
| Reportes, historial y exportar a CSV | Sí | No |

## Requisitos
- Python 3.10 o superior.
- No usa librerías externas: solo la biblioteca estándar (`json`, `csv`, `pathlib`, `hashlib`, `unittest`...).

## Ejecución
```
python main.py
```
**Primer uso:** si no hay usuarios, el programa pide crear el primer administrador. Con ese usuario
se inicia sesión y se registran empleados, productos, etc.

Reglas de la contraseña: mínimo 8 caracteres, con mayúscula, minúscula y número.

## Pruebas
```
python -m unittest discover -s tests -t .
```
Hay pruebas automatizadas de modelos, reglas de negocio, persistencia, exportación, menús y
criterios de aceptación por historia. Los casos documentados están en
[docs/07-casos-de-prueba.md](docs/07-casos-de-prueba.md).
Las pruebas con archivos usan carpetas temporales: nunca tocan `data/inventario.json`.

## Estructura del proyecto
```
STOCK-PRO/
├── main.py               Punto de entrada: carga los datos y abre el menú principal
├── constantes.py         Constantes globales (rutas, roles, tipos de movimiento, stock bajo)
├── almacenamiento.py     Persistencia en JSON (productos, usuarios y movimientos)
├── reportes.py           Cálculos de los reportes (resumen, stock bajo, agotados)
├── exportacion.py        Exportación a CSV (carpeta exportaciones/)
├── modelos/              Entidades del dominio
│   ├── producto.py         Producto
│   ├── movimiento.py       Movimiento (entrada o salida)
│   └── usuario.py          Usuario, Administrador, Empleado
├── servicios/            Reglas de negocio
│   ├── inventario.py       GestorInventario: colección de productos y movimientos
│   ├── busqueda.py, actualizacion.py, salidas.py
│   ├── usuarios.py         Registro y validación de usuarios
│   └── autenticacion.py    Sesión y permisos
├── consola/              Menús e interacción con el usuario (única capa que usa input/print)
├── tests/                Pruebas automatizadas (unittest)
└── docs/                 Documentación Scrum
```
La capa `consola/` solo muestra información y pide datos; las reglas de negocio están en
`servicios/` y `modelos/`, que no usan `input()`.

## Diseño orientado a objetos
- **Encapsulamiento:** la contraseña nunca se guarda; `Usuario` conserva solo un hash PBKDF2 con
  sal en atributos internos (`_hash`, `_sal`) y expone `verificar_contrasena()`.
- **Propiedades:** `Usuario.permisos` y `Movimiento.usuario_responsable` se consultan como atributos.
- **Herencia y polimorfismo:** `Administrador` y `Empleado` heredan de `Usuario` y sobrescriben
  `permisos` y `titulo_menu()`. El resto del programa pregunta `usuario.tiene_permiso(...)` sin
  comparar roles; el comportamiento depende del tipo de objeto. `crear_usuario()` elige la subclase
  según el rol, y `Usuario.from_dict()` la reconstruye al leer el JSON.
- **Composición y colaboración:** `GestorInventario` contiene listas de `Producto` y `Movimiento`;
  `Autenticacion` mantiene la lista de usuarios y la sesión actual.
- **Excepciones propias:** `ErrorAutenticacion` y `ProductoNoEncontradoError`, que heredan de `Exception`.

## Persistencia e integridad de datos
Todo se guarda en `data/inventario.json` con tres secciones:
```json
{ "productos": [], "usuarios": [], "movimientos": [] }
```
- **Archivo inexistente:** el programa inicia con datos vacíos.
- **Archivo con contenido incorrecto:** se informa del error y **no se sobrescribe**, para poder recuperarlo.
- **Guardado seguro:** se escribe primero en un archivo temporal y después se reemplaza el original.
  Un bloque `finally` elimina el temporal si algo falla, así un error a mitad de escritura no daña el JSON.
- Las operaciones rechazadas por validación no modifican el archivo.
- El JSON conserva el formato anterior de lista de productos para ser compatible.

## Exportación CSV
Un administrador puede exportar el **inventario** y el **historial de movimientos** a CSV.
Los archivos se crean en `exportaciones/` con fecha y hora en el nombre, no se sobrescriben entre sí,
conservan tildes y ñ (se abren bien en Excel) y se rechazan si no hay datos. El CSV es solo de
exportación; la persistencia principal es el JSON.

## Validaciones y manejo de errores
Código y nombre obligatorios, precio mayor que cero, cantidades enteras positivas, salidas que no
superen las existencias, usuarios únicos, roles válidos y contraseñas seguras. Las entradas incorrectas
y los errores previsibles (opción inválida, archivo dañado, error de escritura) se informan al usuario
sin cerrar el programa.

## Gestión con Scrum
El proyecto se desarrolló en tres sprints con GitHub Projects, Issues, ramas `feature/*` y Pull Requests.
- Índice de artefactos: [docs/README.md](docs/README.md)
- Product Goal y Product Backlog: [docs/01-product-goal-y-backlog.md](docs/01-product-goal-y-backlog.md)
- Definition of Done: [docs/02-definition-of-done.md](docs/02-definition-of-done.md)
- Sprints: [1](docs/03-sprint-1.md) · [2](docs/04-sprint-2.md) · [3](docs/05-sprint-3.md)
- Seguimiento y transparencia: [docs/06-seguimiento-y-transparencia.md](docs/06-seguimiento-y-transparencia.md)
- Tablero: https://github.com/users/julara209/projects/3/views/2?groupedBy%5BcolumnId%5D=429292259 

## Equipo
| Integrante | Rol Scrum |
|---|---|
| Angie Juliana Espinosa Lara (julara209) | Scrum Master + Developer |
| Rafael Daniel Acero Narváez (ra-cmyk16) | Product Owner + Developer |
| Dilan Camilo Ospina Manrique (Ca-Milo22) |  Developer |

## Limitaciones conocidas
- Aplicación de consola, sin interfaz gráfica ni base de datos (por requisito del curso).
- Un solo archivo JSON local, sin acceso simultáneo de varios usuarios.

