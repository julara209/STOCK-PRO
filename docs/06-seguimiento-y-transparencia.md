# Seguimiento real del desarrollo y transparencia

**Documento actualizado:** 26 de octubre de 2026.\
**Propósito:** describir el proceso real del proyecto STOCK-PRO sin
atribuir al equipo reuniones, fechas o acuerdos que no ocurrieron.

## 1. Eventos Scrum

  -----------------------------------------------------------------------
  Evento                  Situación real          Evidencia o aclaración
  ----------------------- ----------------------- -----------------------
  Sprint Planning (S1,    Las historias se        La distribución de
  S2, S3)                 organizaron en tres     historias y el
                          sprints, pero debe      historial del tablero.
                          precisarse si hubo      No afirmar que hubo
                          reuniones formales de   reuniones formales si
                          planificación.          no ocurrieron.

  Daily Scrum             No se realizaron        La coordinación se hizo
                          reuniones formales.     por WhatsApp. Los
                                                  commits, Pull Requests
                                                  y el tablero muestran
                                                  parte del avance, pero
                                                  no sustituyen las
                                                  Dailies.

  Sprint Review           No se realizó una       La aplicación se
                          reunión formal al       ejecutó por separado.
                          cierre de los sprints.  Estas ejecuciones
                                                  permiten validar
                                                  funcionalidades, pero
                                                  no equivalen a una
                                                  Review grupal.

  Sprint Retrospective    No se realizó una       La reflexión sobre las
                          reunión formal al       dificultades y mejoras
                          cierre de los sprints.  se presenta como
                                                  análisis del proceso,
                                                  no como acta de una
                                                  retrospectiva que no
                                                  ocurrió.
  -----------------------------------------------------------------------

La coordinación se realizó por WhatsApp. Si existen mensajes que
documenten acuerdos o distribución de trabajo, pueden conservarse como
evidencia de coordinación informal. No se deben describir como reuniones
Scrum formales.

## 2. Cómo se movieron las historias entre sprints

Las historias de usuario se organizaron en tres sprints. Algunas no se
terminaron en el sprint previsto y se completaron posteriormente; otras
funcionalidades se finalizaron después del cierre del tercer sprint. Por
tanto, el estado final del producto no coincide por completo con la
planificación inicial.

  -----------------------------------------------------------------------
  Historia o tarea  Sprint asignado   Integración       Sprint planeado
                    en el tablero     registrada        originalmente
  ----------------- ----------------- ----------------- -----------------
  HU-001, T-00,     1                 21-oct            Completar
  T-02                                                  únicamente tras
                                                        revisar el
                                                        historial del
                                                        Issue en GitHub.

  HU-002, HU-003    1                 23-oct            Completar
                                                        únicamente tras
                                                        revisar el
                                                        historial del
                                                        Issue en GitHub.

  HU-004            1                 25-oct            Completar
                                                        únicamente tras
                                                        revisar el
                                                        historial del
                                                        Issue en GitHub.

  HU-005, HU-006,   2                 24-oct            Completar
  HU-011                                                únicamente tras
                                                        revisar el
                                                        historial del
                                                        Issue en GitHub.

  HU-007, HU-008    2                 25-oct            Completar
                                                        únicamente tras
                                                        revisar el
                                                        historial del
                                                        Issue en GitHub.

  HU-012, HU-010    3                 24-oct            Completar
                                                        únicamente tras
                                                        revisar el
                                                        historial del
                                                        Issue en GitHub.

  HU-009, HU-013,   3                 25-oct            Completar
  T-03                                                  únicamente tras
                                                        revisar el
                                                        historial del
                                                        Issue en GitHub.

  T-01 (#13), T-02  No estaban en el  No tenían PR      Se eliminaron el
  (#14)             tablero           propio            25-oct; revisar
                                                        el historial
                                                        disponible y
                                                        explicar el
                                                        motivo real.

  T-04 (#35), T-05  3 o sin sprint    Verificar en      Se crearon el
  (#36)                               GitHub            25-oct, después
                                                        del cierre
                                                        previsto del
                                                        Sprint 3.
  -----------------------------------------------------------------------

Las fechas anteriores corresponden a la información existente en el
documento de seguimiento original. Antes de entregar, deben comprobarse
con el historial de Pull Requests y Issues. No se debe completar el
sprint originalmente planeado a partir de suposiciones: hay que revisar
la actividad de cada Issue en GitHub Projects.

## 3. Limitaciones reconocidas

1.  **Sin Dailies ni reuniones formales durante los sprints.** Se perdió
    un punto de control periódico para detectar impedimentos y ajustar
    el trabajo a tiempo.
2.  **Tareas técnicas eliminadas.** Los Issues #13 (T-01, crear clase
    Producto) y #14 (T-02, implementar `registrar_producto`) se
    eliminaron el 25 de octubre durante la preparación de la entrega. El
    motivo debe describirse según lo que realmente ocurrió. La
    eliminación redujo la trazabilidad entre historias, tareas técnicas
    y Pull Requests. Como evidencia complementaria se pueden consultar
    los checklists de los PR #27, #28, #29, #30 y #31, además de los
    mensajes de los commits. El identificador T-02 también se había
    usado dos veces (#14 y #19).
3.  **Un PR para varias historias.** El PR #32 cubre HU-004, HU-007,
    HU-008 y HU-009. Por ello, la relación entre historia y Pull Request
    no es uno a uno en esos casos.
4.  **Autoría de commits.** Algunos commits se realizaron con un correo
    de Git no configurado (`unknown`), por lo que no quedan asociados a
    una cuenta de GitHub. La participación debe comprobarse con las
    evidencias disponibles, sin atribuir trabajo sin respaldo.
5.  **Trabajo posterior al cierre previsto.** Parte del trabajo se
    terminó el 25 de octubre, después del cierre previsto del Sprint 3.
6.  **Tareas de cierre creadas después del sprint.** T-04 (herencia,
    polimorfismo y `finally`) y T-05 (documentación y README) se
    registraron el 25 de octubre, después del cierre previsto del
    Sprint 3. Deben presentarse como trabajo posterior a la
    planificación inicial, no como actividades planificadas
    originalmente en ese sprint.
7.  **Documentación elaborada al final.** Los documentos Scrum se
    organizaron al final del proyecto a partir de la evidencia
    disponible. Por ello, deben distinguirse los registros
    contemporáneos del desarrollo de las explicaciones redactadas
    posteriormente.

## 4. Validación funcional y reflexión sobre el proceso

No se realizó una reunión formal de Sprint Review ni de Sprint
Retrospective. La aplicación se ejecutó por separado para comprobar sus
funcionalidades. Estas ejecuciones no deben presentarse como una reunión
grupal ni como un evento Scrum formal.

### Validación funcional

Durante las ejecuciones individuales, el equipo puede documentar las
funcionalidades que efectivamente comprobó, por ejemplo:

-   Registro, actualización, búsqueda y consulta de productos.
-   Registro de entradas y salidas de mercancía.
-   Inicio de sesión y acceso según el rol del usuario.
-   Consulta del inventario, productos agotados e historial de
    movimientos.
-   Guardado y recuperación de información mediante JSON.
-   Generación de reportes y exportación de información a CSV.

**Importante:** conservar únicamente las funciones que se ejecutaron y
verificaron realmente. Registrar los resultados concretos en
`docs/07-casos-de-prueba.md`, incluyendo los casos fallidos si los hubo.

### Aprendizajes

El equipo identifica que es necesario estimar el esfuerzo con mayor
cuidado, mantener una relación clara entre cada historia y sus tareas
técnicas, conservar las tareas registradas y actualizar el tablero
conforme avance el desarrollo. También se reconoce que la falta de
reuniones formales dificultó el seguimiento periódico y la detección
temprana de problemas.

Como aprendizaje propio del proceso, las diferencias entre la
planificación y la ejecución muestran que las historias deben revisarse
durante el desarrollo y trasladarse de sprint de forma transparente
cuando no se terminan a tiempo. Asimismo, la documentación debe
mantenerse junto con el código y no dejarse únicamente para el cierre
del proyecto.

### Mejoras pendientes

-   Ampliar y completar las pruebas manuales documentadas, registrando
    entradas, resultados esperados, resultados obtenidos y estado de
    cada caso.
-   Revisar la persistencia JSON y la exportación CSV con casos válidos
    y de error, y guardar evidencia de los resultados reales.
-   Mejorar los reportes según las necesidades del usuario, si se
    identifica una necesidad concreta y el tiempo disponible lo permite.
-   Conservar todas las tareas técnicas y vincularlas con sus historias
    de usuario y Pull Requests, evitando eliminarlas para simplificar el
    tablero.
-   Organizar mejor la distribución del trabajo y comprobar que todos
    los integrantes tengan contribuciones técnicas verificables.
-   En futuros proyectos, realizar los eventos Scrum previstos, aunque
    sean breves, y registrar los acuerdos y los impedimentos en el
    momento en que ocurran.

Estas mejoras son propuestas derivadas del análisis del proceso. No se
presentan como acuerdos de una retrospectiva formal, ya que dicha
reunión no se realizó.

## 5. Trabajo pendiente o posterior a la planificación inicial

Las funcionalidades o tareas que se terminaron después del cierre
previsto del Sprint 3 deben identificarse como trabajo posterior a la
planificación inicial. No deben asignarse retrospectivamente a un sprint
como si hubieran sido completadas durante ese periodo.

Antes de entregar, el equipo debe verificar: - El sprint originalmente
previsto para cada historia, usando el historial de GitHub. - Las fechas
de integración, usando los Pull Requests y commits existentes. - Los
resultados reales de las pruebas, especialmente el número de pruebas
satisfactorias. - La razón de la eliminación de los Issues #13 y #14,
según lo que el equipo pueda confirmar.

Cuando un dato no pueda verificarse, es preferible indicarlo como
limitación documental en lugar de inventarlo.
