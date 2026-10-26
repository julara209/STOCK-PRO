# Sprint 2

**Fechas en el tablero:** 21–22 oct 2026 · **Trabajo integrado realmente:** 24–25 oct

## Sprint Goal
Registrar entradas y salidas de mercancía, conservar los datos entre ejecuciones y permitir el inicio de sesión según el rol.

> Redactado el 25/10/2026 a partir de lo entregado. No existía un Sprint Goal escrito antes del sprint.

## Sprint Backlog

| ID | Historia o tarea | Responsable | Prioridad | PR | Integrado en main | Estado final |
|---|---|---|---|---|---|---|
| HU-005 (#11) | Registrar salida de mercancía | julara209 | Alta | #25 | 24-oct | Done |
| HU-006 (#5) | Registrar entrada de mercancía | ra-cmyk16 | Alta | #27 | 24-oct | Done |
| HU-011 (#7) | Conservar los datos entre ejecuciones | ra-cmyk16 | Alta | #28 | 24-oct | Done |
| HU-007 (#6) | Iniciar sesión según el rol | Ca-Milo22 | Alta | #32 | 25-oct | Done (integrada con retraso) |
| HU-008 (#9) | Consultar productos agotados | Ca-Milo22 | Baja | #32 | 25-oct | Done (integrada con retraso) |

## Ajustes durante la ejecución (verificables en el repositorio)
- HU-005 incorporó el modelo `Movimiento` y su almacenamiento en JSON (commits `b7ecfb4`, `0b3eff1`), que luego reutilizaron HU-006 y HU-012.
- HU-007 y HU-008 se entregaron junto con HU-004 y HU-009 en un solo PR (#32), en vez de un PR por historia. **Decisión a evaluar en la retrospectiva.**
- Ninguna historia cambió de sprint en el tablero. Desde el Sprint 1 llegó trabajo sin terminar a este periodo: HU-004, integrada el 25-oct dentro del mismo PR #32 que HU-007 y HU-008.
- Motivo de entregar HU-004, 007, 008 y 009 en un solo PR:  La entrega conjunta se realizó porque no había claridad o comunicación suficiente sobre la organización de las entregas por historia. Como resultado, las cuatro historias se integraron mediante el PR #32 el 25 de octubre.

## Daily Scrum
No se realizaron Dailies formales. Ver [06-seguimiento-y-transparencia.md](06-seguimiento-y-transparencia.md).

## Sprint Review
Se registra en la reunión consolidada de Review y Retrospective: ver [06, sección 4](06-seguimiento-y-transparencia.md).

## Sprint Retrospective
**Hechos observables:** las cinco historias se integraron 2 y 3 días después del cierre previsto; un único PR cubrió dos historias de este sprint y dos de otros.
Se registra en la reunión consolidada: ver [06, sección 4](06-seguimiento-y-transparencia.md).
