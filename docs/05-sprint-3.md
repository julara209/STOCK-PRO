# Sprint 3

**Fechas en el tablero:** 23–24 oct 2026 · **Trabajo integrado realmente:** 24–25 oct (las fechas de T-04 y T-05 están en la tabla)

## Sprint Goal
Completar la consulta y el análisis del inventario (inventario completo, historial, reportes), exportar a CSV y conectar el login y los roles al programa principal.

> Redactado el 25/10/2026 a partir de lo entregado. No existía un Sprint Goal escrito antes del sprint.

## Sprint Backlog

| ID | Historia o tarea | Responsable | Prioridad | PR | Integrado en main | Estado final |
|---|---|---|---|---|---|---|
| HU-012 (#8) | Consultar el historial de movimientos | ra-cmyk16 | Media | #29 | 24-oct | Done |
| HU-010 (#12) | Generar reportes del inventario | julara209 | Media | #30 | 24-oct | Done |
| HU-009 (#10) | Consultar el inventario completo | Ca-Milo22 | Media | #32 | 25-oct | Done (integrada con retraso) |
| HU-013 (#16) | Exportar reportes a CSV | julara209 | Alta | #31 | 25-oct | Done (integrada con retraso) |
| T-03 (#33) | Conectar login y roles al programa, guardar usuarios y corregir pruebas | julara209 | — | #34 | 25-oct | Done (integrada con retraso) |
| T-04 (#35) | Refuerzo técnico: herencia y polimorfismo de roles (`Administrador`, `Empleado`) y guardado seguro del JSON con `finally` | Ca-Milo22 | — | #37 | 25-oct | Done  |
| T-05 (#36) | Documentación Scrum (`docs/`) y README completo | julara209 | — | #38 | 25-oct | Done  |

## Ajustes durante la ejecución (verificables en el repositorio)
- Se creó T-03 porque el login, los roles y el registro de usuarios (HU-004 y HU-007, ya integradas en #32) todavía no estaban conectados al programa principal. T-03 los conectó, guardó los usuarios en el JSON, agregó pruebas de aceptación por historia y corrigió pruebas desactualizadas (commits `9a4001b`, `09d99e1`, `4e55abb`, `baca4d7`).
  Esto indica que HU-004 y HU-007 no cumplían del todo el punto "integrada en el proyecto" de la Definition of Done al momento de cerrarse. **Confirmar en la retrospectiva.**
- Se eliminaron módulos duplicados en la raíz y una prueba obsoleta (commit `3fcae9e`).
- Trabajo realizado el 25-oct, fuera de la ventana de sprint del tablero (HU-009, HU-013, T-03).
- T-04 (#35) y T-05 (#36) se crearon el 25-oct, **después del cierre previsto del sprint**, para cubrir requisitos técnicos pendientes (herencia y polimorfismo, bloque `finally`) y la documentación. Se registran en este sprint como desbordamiento; no se planificaron dentro de él.
- Ninguna historia del sprint quedó sin terminar: HU-009, HU-010, HU-012 y HU-013 se integraron. HU-009 y HU-013 se cerraron el 25-oct, fuera de la ventana del sprint.

## Daily Scrum
No se realizaron Dailies formales. Ver [06-seguimiento-y-transparencia.md](06-seguimiento-y-transparencia.md).

## Sprint Review
Se registra en la reunión consolidada de Review y Retrospective, con la demostración de la aplicación completa: ver [06, sección 4](06-seguimiento-y-transparencia.md).

## Sprint Retrospective
**Hechos observables:** T-03 apareció al final por falta de integración continua del login; tres de cinco ítems se cerraron el día 25; sin Dailies no hubo un punto de control intermedio.
Se registra en la reunión consolidada: ver [06, sección 4](06-seguimiento-y-transparencia.md).
