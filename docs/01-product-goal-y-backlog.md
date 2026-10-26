# Product Goal y Product Backlog

## Producto
**STOCK-PRO** — sistema de inventario de consola en Python para una tienda de abarrotes,
con roles de Administrador y Empleado.

## Product Goal
Permitir que una tienda de abarrotes controle sus productos y existencias desde la consola:
registrar, actualizar y buscar productos, registrar entradas y salidas de mercancía,
consultar el inventario y los agotados, generar reportes y exportarlos a CSV, con acceso
según el rol del usuario y con los datos conservados en JSON entre ejecuciones.

No existía un Sprint Goal escrito previamente; se redactó el 25/10/2026 a partir de lo entregado.

## Usuarios
- **Administrador:** registra usuarios, gestiona productos, ve reportes, historial y exporta CSV.
- **Empleado:** busca productos, registra entradas y salidas, consulta inventario y agotados.

## Equipo y responsabilidades

| Integrante | Cuenta GitHub | Responsabilidad Scrum | Participación técnica (PRs) |
|---|---|---|---|
| Angie Juliana Espinosa Lara | julara209 | Scrum Master + Developer | HU-002, 003, 005, 010, 013, T-00, T-02, T-03, T-05|
| Rafael Daniel Acero Narváez | ra-cmyk16 | Product Owner + Developer| HU-001, 006, 011, 012 |
| Dilan Camilo Ospina Manrique | Ca-Milo22 | Developer | HU-004, 007, 008, 009, T-04 |

Todos los integrantes son Developers.

## Product Backlog

Orden: por prioridad y dependencia técnica. Los criterios de aceptación están tomados de las
pruebas de aceptación del repositorio (`tests/test_criterios_aceptacion.py`, `test_reportes.py`,
`test_exportacion.py`).
Los criterios de HU-001 a HU-012 coinciden con el documento de historias de usuario original del equipo. HU-013 se redactó durante el desarrollo, al detectar que la exportación a CSV, exigida por el enunciado, no estaba en el backlog.

| ID | Issue | Historia de usuario | Prioridad | Estimación | Responsable |
|---|---|---|---|---|---|
| HU-001 | #1 | Registrar un producto | Alta | 3 | ra-cmyk16 |
| HU-002 | #2 | Actualizar un producto | Media | 2 | julara209 |
| HU-003 | #4 | Buscar productos | Media | 2 | julara209 |
| HU-004 | #3 | Registrar usuarios | Alta | 3 | Ca-Milo22 |
| HU-005 | #11 | Registrar salida de mercancía | Alta | 3 | julara209 |
| HU-006 | #5 | Registrar entrada de mercancía | Alta | 2 | ra-cmyk16 |
| HU-007 | #6 | Iniciar sesión según el rol | Alta | 3 | Ca-Milo22 |
| HU-008 | #9 | Consultar productos agotados | Baja | 1 | Ca-Milo22 |
| HU-009 | #10 | Consultar el inventario completo | Media | 1 | Ca-Milo22 |
| HU-010 | #12 | Generar reportes del inventario | Media | 3 | julara209 |
| HU-011 | #7 | Conservar los datos entre ejecuciones | Alta | 3 | ra-cmyk16 |
| HU-012 | #8 | Consultar el historial de movimientos | Media | 2 | ra-cmyk16 |
| HU-013 | #16 | Exportar reportes a CSV | Alta | 2 | julara209 |

Estimación en puntos relativos de esfuerzo (1 = poco, 2 = medio, 3 = alto), registrados el 25/10/2026 a partir de lo implementado.

Tareas técnicas (Issues vigentes): T-00 (#15), T-02 (#19), T-03 (#33), T-04 (#35), T-05 (#36).
Los Issues #13 (T-01) y #14 (T-02) existieron y fueron eliminados el 25-oct; ver
[06](06-seguimiento-y-transparencia.md).

### Historias y criterios de aceptación

**HU-001 · Registrar un producto** — Como administrador, quiero registrar productos con su código, nombre, categoría, precio y cantidad inicial, para mantener organizado el inventario de la tienda.

- El código del producto no puede estar repetido.
- El nombre no puede estar vacío.
- El precio debe ser mayor que cero.
- La cantidad inicial debe ser igual o mayor que cero.
- Los datos obligatorios deben ser válidos.
- Un producto registrado debe quedar disponible para las consultas.
- Un registro rechazado no debe modificar el inventario.

**HU-002 · Actualizar un producto** — Como administrador, quiero modificar el precio o la información de un producto y actualizar sus existencias, para mantener actualizado el inventario de la tienda.
- El producto debe existir previamente.
- El nuevo precio debe ser un número mayor que cero.
- Los datos obligatorios no pueden estar vacíos.
- Las entradas de mercancía deben aumentar las existencias actuales.
- Si el producto no existe, se debe mostrar un mensaje de error.
- Una actualización rechazada no debe modificar la información del producto.

**HU-003 · Buscar productos** — Como administrador o empleado, quiero buscar productos por código, nombre o categoría, para encontrar rápidamente la información que necesito.
- La búsqueda por nombre no debe distinguir entre mayúsculas y minúsculas.
- Se debe permitir buscar por código exacto.
- Se debe permitir filtrar por categoría.
- Si no hay resultados, se debe informar al usuario.
- La búsqueda no debe modificar los datos del inventario.

**HU-004 · Registrar usuarios** — Como administrador, quiero registrar empleados con sus datos de acceso, para que puedan utilizar el sistema según los permisos de su rol.
- El nombre de usuario no puede estar vacío ni repetido.
- La contraseña debe cumplir las reglas de seguridad definidas.
- Cada usuario debe tener asignado un rol válido: Administrador o Empleado.
- Los empleados no deben poder crear administradores ni asignarse permisos adicionales.
- Un registro válido debe quedar disponible para iniciar sesión.
- Un registro rechazado no debe modificar la lista de usuarios.

**HU-005 · Registrar salida de mercancía** — Como empleado, quiero registrar la salida de productos del inventario, para mantener actualizadas las existencias cuando se retire mercancía de la tienda.
- El producto debe existir previamente.
- La cantidad que sale debe ser mayor que cero.
- No se puede retirar una cantidad superior a las existencias disponibles.
- Una salida válida debe descontar la cantidad correspondiente.
- Cada movimiento debe registrar la fecha, el producto, la cantidad y el usuario responsable.
- Una salida rechazada no debe modificar las existencias ni el historial de movimientos.

**HU-006 · Registrar entrada de mercancía** — Como empleado, quiero registrar la entrada de mercancía a la tienda, para actualizar las existencias cuando lleguen nuevos productos.
- El producto debe estar registrado previamente.
- La cantidad recibida debe ser mayor que cero.
- La entrada debe sumarse a las existencias actuales.
- Se debe registrar la fecha, el producto, la cantidad y el usuario responsable.
- Si el producto no existe o la cantidad no es válida, se debe rechazar la operación.
- Una entrada rechazada no debe modificar el inventario.

**HU-007 · Iniciar sesión según el rol** — Como usuario del sistema, quiero iniciar sesión con mis credenciales, para acceder únicamente a las opciones permitidas según mi rol.
- El usuario debe estar registrado.
- Las credenciales deben validarse antes de permitir el acceso.
- El administrador debe acceder al menú de administración.
- El empleado debe acceder al menú de empleado.
- Si las credenciales son incorrectas, se debe mostrar un mensaje de error.
- Un empleado no debe poder acceder a las funciones exclusivas del administrador.
- Cerrar sesión debe regresar al menú principal.

**HU-008 · Consultar productos agotados** — Como empleado, quiero consultar los productos que están agotados, para informar al administrador y facilitar su reposición.
- Solo deben aparecer productos con existencias iguales a cero.
- Se debe mostrar el código, nombre y categoría del producto.
- Si no hay productos agotados, el programa debe informarlo.
- La consulta no debe modificar las existencias.
- Los resultados deben mostrarse de forma organizada en la consola.

**HU-009 · Consultar el inventario completo** — Como administrador o empleado, quiero consultar los productos y sus existencias actuales, para conocer la disponibilidad de la mercancía de la tienda.
- Se deben mostrar el código, nombre, categoría, precio y existencias.
- La consulta debe incluir los productos registrados.
- La información debe reflejar las entradas y salidas realizadas.
- Si no hay productos registrados, se debe mostrar un mensaje informativo.
- La consulta no debe modificar los datos del inventario.

**HU-010 · Generar reportes del inventario** — Como administrador, quiero consultar reportes del inventario, para conocer las existencias disponibles e identificar los productos que necesitan reposición.
- El reporte debe mostrar los productos registrados y sus existencias.
- Debe identificar los productos con existencias bajas.
- Debe mostrar los productos agotados.
- Debe permitir consultar los movimientos de entrada y salida.
- Si no hay información, el programa debe mostrar un mensaje sin generar errores.

**HU-011 · Conservar los datos entre ejecuciones** — Como administrador, quiero que los productos, usuarios y movimientos queden guardados al cerrar el programa, para no tener que registrar toda la información nuevamente.
- Los productos, usuarios y movimientos deben guardarse en data/inventario.json.
- Al iniciar el programa, se deben cargar los datos guardados.
- Si el archivo no existe, el sistema debe iniciar con datos vacíos o con la configuración inicial.
- Si el archivo está dañado, se debe informar del problema y evitar sobrescribirlo automáticamente.
- Los datos deben guardarse después de cada operación exitosa que los modifique.
- Las operaciones rechazadas no deben alterar la información guardada.

**HU-012 · Consultar el historial de movimientos** — Como administrador, quiero consultar el historial de entradas y salidas de mercancía, para conocer los cambios realizados en las existencias de la tienda.
- Cada movimiento debe tener un identificador único.
- Se debe mostrar el tipo de movimiento, el producto, la cantidad, la fecha y el usuario responsable.
- Se debe poder consultar el historial completo.
- Se debe poder buscar los movimientos de un producto específico.
- Si no hay movimientos registrados, el sistema debe informarlo.
- Consultar el historial no debe modificar los datos.

**HU-013 · Exportar reportes a CSV** — Como administrador, quiero exportar el inventario y el historial de movimientos a archivos CSV, para compartir o archivar la información fuera del programa.
- Se debe poder exportar el inventario con código, nombre, categoría, precio y existencias.
- Se debe poder exportar el historial de movimientos.
- Los archivos se guardan en la carpeta `exportaciones/`, que se crea automáticamente si no existe.
- El nombre del archivo incluye la fecha y hora para no sobrescribir exportaciones anteriores.
- Si no hay datos para exportar, el programa lo informa y no genera el archivo.
- Exportar no debe modificar el inventario ni el archivo JSON.
- Si ocurre un error de escritura, se muestra un mensaje y el programa no se cierra.
- El CSV es solo para exportar; la persistencia principal sigue siendo JSON.