# Casos de prueba

**Cómo ejecutarlos:** `python -m unittest discover -s tests -t .`
**Suite completa:** 243 pruebas automatizadas con `unittest`.
Las pruebas que usan archivos trabajan sobre carpetas temporales (`tempfile`), nunca sobre `data/inventario.json` real.

**Resultado al preparar este documento:** 243 pruebas, OK.
**Última ejecución en la máquina del equipo:** 2026-10-26 10:18, Angie Espinosa, 243 pruebas OK.

| ID | Funcionalidad (HU) | Datos de entrada | Resultado esperado | Resultado obtenido | Estado | Prueba automatizada |
|---|---|---|---|---|---|---|
| CP-01 | Primer uso, sin usuarios (HU-004/007) | Programa sin usuarios; se crea administrador | Se crea el primer administrador y se guarda | Se creó y quedó guardado | Satisfactorio | `test_flujo_sesion.test_sin_usuarios_se_crea_el_primer_administrador_y_se_guarda` |
| CP-02 | Registrar producto (HU-001) | A01, Arroz, Granos, 4500, 10 | Producto disponible en el inventario | Quedó disponible | Satisfactorio | `test_criterios_aceptacion.Hu01…test_hu01_producto_registrado_queda_disponible` |
| CP-03 | Entradas inválidas y errores de conversión (HU-001) | Precio `0`, `-5`, `"abc"` | Se rechaza con `ValueError` | Rechazado en los tres casos | Satisfactorio | `…test_hu01_precio_debe_ser_mayor_que_cero` |
| CP-04 | Opción no reconocida (HU-007) | Opción inválida en el menú | El menú no se rompe y vuelve a pedir | No se interrumpió | Satisfactorio | `test_autenticacion.…test_entrada_invalida_no_rompe_el_menu` |
| CP-05 | Regla de negocio: salida mayor al stock (HU-005) | Salida de `0`, `-2` y `11` sobre stock 10 | Se rechaza | Rechazado | Satisfactorio | `…test_hu05_cantidad_mayor_que_cero_y_no_mayor_al_stock` |
| CP-06 | Estado tras operación rechazada (HU-005/HU-011) | Salida de 99 sobre stock 10 | Existencias, historial y archivo JSON sin cambios | Sin cambios | Satisfactorio | `…test_hu05_salida_rechazada_no_modifica_existencias_ni_historial` |
| CP-07 | Búsquedas (HU-003) | Nombre en distinto uso de mayúsculas; categoría; término inexistente | Encuentra sin distinguir mayúsculas, filtra por categoría y devuelve lista vacía si no hay coincidencias | Cumplido | Satisfactorio | `…Hu03BuscarProductos` (5 pruebas) |
| CP-08 | Entrada de mercancía (HU-006) | Entrada de 5 unidades sobre stock 10, usuario "juan" | Stock 15 y movimiento con tipo, producto, cantidad, fecha y usuario | Stock 15; movimiento registrado | Satisfactorio | `…test_hu06_entrada_se_suma_y_registra_fecha_producto_cantidad_usuario` |
| CP-09 | Reportes y cálculos (HU-010) | Productos y movimientos de prueba | Totales, stock bajo y agotados calculados correctamente | Cálculos correctos | Satisfactorio | `test_reportes.test_resumen_calcula_totales` y 11 más |
| CP-10 | Persistencia JSON (HU-011) | Registrar producto, entrada y cerrar/abrir | Los datos se recuperan al reiniciar | Recuperados | Satisfactorio | `…test_hu11_al_iniciar_se_cargan_los_datos_guardados` |
| CP-11 | Archivo JSON inexistente (HU-011) | No existe `data/inventario.json` | Inicia con datos vacíos sin error | Inició vacío | Satisfactorio | `…test_hu11_archivo_inexistente_inicia_con_datos_vacios` |
| CP-12 | Archivo JSON dañado (HU-011) | Contenido `{esto no es json` en una copia temporal | Se informa "dañado" y **no** se sobrescribe | Informó el error; el contenido quedó igual | Satisfactorio | `…test_hu11_archivo_danado_se_informa_y_no_se_sobrescribe` |
| CP-13 | Exportación CSV (HU-013) | Inventario con tildes y ñ | CSV con encabezado, filas ordenadas y caracteres conservados | Cumplido | Satisfactorio | `test_exportacion.test_conserva_tildes_y_enes` |
| CP-14 | CSV sin datos (HU-013) | Exportar sin productos | Se rechaza y no se crea archivo | Rechazado, sin archivo | Satisfactorio | `test_exportacion.test_sin_productos_se_rechaza_y_no_crea_nada` |
| CP-15 | Permisos por rol (HU-007) | Empleado intenta una opción de administrador | Acceso denegado | Denegado | Satisfactorio | `test_autenticacion.test_empleado_no_accede_a_funciones_de_admin` |
| CP-16 | Seguridad de contraseña (HU-004) | Registro de usuario válido | La contraseña se guarda como hash, no en texto plano | Guardada con hash | Satisfactorio | `…test_hu04_la_contrasena_se_guarda_con_hash` |
| CP-17 | Polimorfismo de roles (HU-007) | Administrador y Empleado ante `tiene_permiso("ver_reportes")` y `titulo_menu()` | Cada rol responde distinto al mismo mensaje | Cumplido | Satisfactorio | `test_roles_polimorfismo.TestPolimorfismo` |
| CP-18 | Guardado seguro con `finally` (HU-011) | Fallo simulado de escritura sobre una copia temporal | Se conserva el JSON anterior y no queda archivo `.tmp` | Cumplido | Satisfactorio | `test_guardado_seguro.test_si_falla_la_escritura_finally_elimina_el_temporal` |

## Pruebas manuales
Ejecutadas con la aplicación real (`python main.py`) sobre una carpeta sin datos previos.
**Fecha y responsable:** 25-oct, Angie Espinosa.

| ID | Pasos | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| PM-01 | Iniciar, crear administrador, registrar un producto y reiniciar | El producto sigue ahí | El producto se encuentra en el inventario. | Satisfactorio |
| PM-02 | Escribir una letra donde se pide un número | Mensaje de error, el programa sigue | Mensaje de error, se rechazó el registro y el programa continuó. | Satisfactorio |
| PM-03 | Exportar a CSV y abrir el archivo en Excel | Archivo en `exportaciones/` con tildes correctas | La exportación fue exitosa y las tildes se ven correctas. | Satisfactorio |
