
# Seguimiento del desarrollo y transparencia del proyecto STOCK-PRO

**Fecha de actualización:** 26 de octubre de 2026

**Propósito:** documentar el desarrollo del proyecto STOCK-PRO, describiendo la organización del trabajo, el seguimiento de las historias de usuario, las dificultades presentadas y los aprendizajes obtenidos durante el proceso.

## 1. Desarrollo de los eventos Scrum

Durante el desarrollo de STOCK-PRO, el trabajo se organizó en tres sprints. Sin embargo, no se realizaron formalmente todos los eventos establecidos en Scrum. La coordinación entre los integrantes se llevó a cabo principalmente mediante WhatsApp, mientras que el avance del proyecto quedó reflejado parcialmente en GitHub Projects, los commits y los Pull Requests.

| Evento Scrum | Desarrollo durante el proyecto |
|---|---|
| Sprint Planning | Las historias de usuario se distribuyeron en tres sprints para organizar el trabajo. No se realizaron reuniones formales de planificación. |
| Daily Scrum | No se realizaron reuniones diarias formales. La comunicación sobre el trabajo se mantuvo principalmente mediante WhatsApp. |
| Sprint Review | No se realizaron reuniones formales de revisión al finalizar los sprints. Las funcionalidades de la aplicación se comprobaron mediante ejecuciones individuales. |
| Sprint Retrospective | No se realizaron reuniones formales de retrospectiva. Las dificultades y oportunidades de mejora se identificaron mediante el análisis posterior del proceso. |

Aunque no se desarrollaron formalmente estos eventos, se cuenta con evidencias parciales del trabajo realizado, como los mensajes de coordinación, el historial de GitHub Projects, los commits y los Pull Requests.

La ausencia de reuniones formales dificultó el seguimiento periódico de las actividades y redujo las oportunidades de identificar oportunamente los impedimentos, revisar los avances en equipo y ajustar la planificación.

## 2. Organización de las historias de usuario y avance de los sprints

Las historias de usuario se organizaron en tres sprints. Durante el desarrollo, algunas actividades no se completaron dentro del periodo inicialmente previsto y continuaron posteriormente. Además, se crearon nuevas tareas después de la fecha prevista para finalizar el tercer sprint.

La siguiente tabla presenta la distribución registrada y las fechas de integración consignadas en el seguimiento del proyecto.

| Historia o tarea | Sprint registrado | Fecha de integración o registro |
|---|---|---|
| HU-001, T-00 y T-02 | Sprint 1 | 21 de octubre |
| HU-002 y HU-003 | Sprint 1 | 23 de octubre |
| HU-004 | Sprint 1 | 25 de octubre |
| HU-005, HU-006 y HU-011 | Sprint 2 | 24 de octubre |
| HU-007 y HU-008 | Sprint 2 | 25 de octubre |
| HU-012 y HU-010 | Sprint 3 | 24 de octubre |
| HU-009, HU-013 y T-03 | Sprint 3 | 25 de octubre |
| T-01 (#13) y T-02 (#14) | Sin asignación vigente en el tablero | Eliminadas el 25 de octubre |
| T-04 (#35) y T-05 (#36) | Creadas después del cierre previsto del Sprint 3 | 25 de octubre |

Las fechas presentadas corresponden a los registros disponibles en el seguimiento del proyecto. La distribución permite observar que algunas actividades se completaron cerca del cierre previsto y que otras se incorporaron posteriormente.

Por esta razón, el estado final de STOCK-PRO no coincide completamente con la planificación inicial. La asignación de cada historia y sus fechas de finalización deben interpretarse de acuerdo con el historial de actividad registrado en GitHub.

## 3. Dificultades y limitaciones identificadas

Durante el desarrollo del proyecto se presentaron situaciones que afectaron la organización, el seguimiento y la trazabilidad del trabajo.

### 3.1. Ausencia de reuniones formales de seguimiento

La falta de reuniones diarias dificultó la identificación temprana de problemas y el seguimiento continuo de las responsabilidades individuales. Aunque existió comunicación por WhatsApp, esta no reemplazó completamente los beneficios de los eventos formales de Scrum.

### 3.2. Eliminación de tareas técnicas

Los Issues #13 (T-01, crear la clase Producto) y #14 (T-02, implementar `registrar_producto`) fueron eliminados el 25 de octubre. Esta acción redujo la trazabilidad entre las tareas técnicas, las historias de usuario y los Pull Requests.

Como evidencia complementaria del desarrollo se encuentran los checklists de los Pull Requests #27, #28, #29, #30 y #31, así como los mensajes de los commits. También se identificó que el código T-02 fue utilizado en dos tareas diferentes, correspondientes a los Issues #14 y #19, lo que puede generar confusión al consultar los registros.

### 3.3. Relación entre historias de usuario y Pull Requests

El Pull Request #32 incluye trabajo relacionado con las historias HU-004, HU-007, HU-008 y HU-009. Por lo tanto, en este caso, un único Pull Request agrupa varias historias de usuario, lo que hace necesario revisar su contenido para identificar las funcionalidades integradas.

### 3.4. Identificación de la autoría de los commits

Algunos commits se registraron con un correo de Git no configurado, identificado como `unknown`. Esta situación dificulta asociarlos directamente con una cuenta de GitHub. Por ello, la participación individual debe analizarse a partir de las evidencias disponibles, sin atribuir contribuciones que no puedan comprobarse.

### 3.5. Actividades finalizadas después del cierre previsto

Parte del trabajo se completó el 25 de octubre, después del cierre previsto del Sprint 3. Esto evidencia diferencias entre la planificación inicial y la ejecución real del proyecto.

### 3.6. Creación de tareas posteriores

Las tareas T-04 (#35), relacionada con herencia, polimorfismo y el uso de `finally`, y T-05 (#36), relacionada con la documentación y el archivo README, se crearon el 25 de octubre. Estas actividades corresponden a trabajo incorporado después del cierre previsto del tercer sprint.

### 3.7. Elaboración de la documentación al finalizar el proyecto

Parte de la documentación relacionada con el proceso Scrum se organizó al final del desarrollo, utilizando la información disponible en GitHub y los demás registros. Por ello, es importante diferenciar las evidencias generadas durante el trabajo de las explicaciones redactadas posteriormente.

## 4. Validación funcional y análisis del proceso

No se realizaron reuniones formales de Sprint Review ni de Sprint Retrospective. Sin embargo, la aplicación se ejecutó individualmente para comprobar sus funcionalidades.

Estas ejecuciones permitieron revisar el comportamiento del sistema, pero no constituyeron una revisión grupal formal. Los resultados de las pruebas deben corresponder a las funcionalidades que efectivamente fueron ejecutadas y verificadas.

### 4.1. Funcionalidades evaluadas

Entre las funcionalidades del proyecto STOCK-PRO que pueden incluirse en la validación se encuentran:

- Registro, actualización, búsqueda y consulta de productos.
- Registro de entradas y salidas de mercancía.
- Inicio de sesión y control de acceso según el rol del usuario.
- Consulta del inventario, identificación de productos agotados e historial de movimientos.
- Guardado y recuperación de información mediante archivos JSON.
- Generación de reportes y exportación de información a archivos CSV.

La validación de cada funcionalidad debe respaldarse con los resultados obtenidos durante su ejecución. Los casos de prueba, incluidos los que presentaron errores, deben documentarse en el archivo `docs/07-casos-de-prueba.md`.

### 4.2. Aprendizajes obtenidos

El desarrollo de STOCK-PRO permitió identificar la importancia de mantener una planificación realista, distribuir adecuadamente las responsabilidades y establecer una relación clara entre las historias de usuario, las tareas técnicas y los Pull Requests.

También se evidenció la necesidad de actualizar el tablero de seguimiento durante el desarrollo, registrar los cambios de planificación y mantener una comunicación constante entre los integrantes.

La ausencia de reuniones formales dificultó el seguimiento periódico de las actividades. Asimismo, las diferencias entre el trabajo planificado y el ejecutado mostraron la importancia de revisar el avance de las historias y reorganizar las actividades cuando no se completan dentro del sprint correspondiente.

Otro aprendizaje importante es que la documentación debe mantenerse actualizada durante todo el proyecto. Esto facilita la identificación de los cambios, permite verificar las contribuciones y evita que la reconstrucción del proceso dependa únicamente de los registros consultados al finalizar el desarrollo.

### 4.3. Oportunidades de mejora

A partir del análisis del proyecto, se identifican las siguientes oportunidades de mejora:

- Ampliar las pruebas manuales y documentar las entradas, los resultados esperados, los resultados obtenidos y el estado de cada caso.
- Verificar el funcionamiento de la persistencia JSON y la exportación CSV mediante casos válidos y situaciones de error.
- Mejorar los reportes de acuerdo con las necesidades identificadas durante el desarrollo.
- Mantener las tareas técnicas registradas y relacionarlas con las historias de usuario y los Pull Requests correspondientes.
- Organizar la distribución del trabajo para facilitar el seguimiento de las responsabilidades y la verificación de las contribuciones individuales.
- Realizar los eventos Scrum previstos en futuros proyectos, aunque sean breves, dejando registro de los acuerdos, avances e impedimentos.
- Actualizar la documentación y el tablero de seguimiento a medida que se realizan cambios en el proyecto.

Estas oportunidades de mejora se derivan del análisis del proceso de desarrollo y no corresponden a acuerdos registrados en una reunión formal de retrospectiva.

## 5. Trabajo posterior a la planificación inicial

El desarrollo de STOCK-PRO incluyó actividades que se completaron o registraron después de las fechas previstas en la planificación inicial. Entre ellas se encuentran tareas finalizadas el 25 de octubre y la creación de los Issues #35 y #36, relacionados con aspectos técnicos y documentación.

Esta situación demuestra que la ejecución real del proyecto presentó diferencias respecto a la distribución inicial del trabajo. Por ello, es importante distinguir las actividades previstas desde el comienzo de aquellas que se incorporaron o finalizaron posteriormente.

Para mantener la transparencia del seguimiento, la información del proyecto debe basarse en los registros disponibles de GitHub Projects, Issues, commits y Pull Requests. Las fechas, asignaciones y contribuciones deben corresponder a las evidencias existentes.
