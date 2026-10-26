# Sprint 1

**Fechas en el tablero:** 19–20 oct 2026 · **Trabajo integrado realmente:** 21–25 oct (ver tabla)

## Sprint Goal
Dejar lista la base del proyecto (estructura modular en paquetes) y poder registrar, actualizar y buscar productos, además de registrar usuarios con rol.

> Redactado el 25/10/2026 a partir de lo entregado. No existía un Sprint Goal escrito antes del sprint.

## Sprint Backlog

| ID | Historia o tarea | Responsable | Prioridad | PR | Integrado en main | Estado final |
|---|---|---|---|---|---|---|
| T-00 (#15) | Estructura inicial del proyecto | julara209 | Alta | #17, #18 | 21-oct | Done |
| T-02 (#19) | Reorganizar el proyecto en paquetes (modelos, servicios, consola) | Ca-Milo22, julara209 | Alta | #20, #22 | 21-oct y 23-oct | Done |
| HU-001 (#1) | Registrar un producto | ra-cmyk16 | Alta | #21 | 21-oct | Done |
| HU-002 (#2) | Actualizar un producto | julara209 | Media | #23, #26 | 23-oct | Done |
| HU-003 (#4) | Buscar productos | julara209 | Media | #24 | 23-oct | Done |
| HU-004 (#3) | Registrar usuarios | Ca-Milo22 | Alta | #32 | 25-oct | Done (integrada con retraso) |

## Tareas técnicas registradas antes del sprint y luego eliminadas

Los Issues #13 (T-01 · Crear clase Producto con atributos y validaciones) y #14 (T-02 · Implementar
GestorInventario.registrar_producto()) se crearon y cerraron antes del Sprint 1. **El equipo los eliminó el
25-oct** (ver [06](06-seguimiento-y-transparencia.md)), por lo que ya no es posible consultarlos.
No tenían commits ni PR que los referenciaran; el código correspondiente llegó a `main` en los PR #17, #18 y #21.
Ambas pertenecían a HU-001 (#1): T-01 creaba la clase `Producto` y T-02 implementaba `registrar_producto()`.

## Ajustes durante la ejecución (hechos verificables en el repositorio)
- T-02 necesitó dos PRs: #20 (estructura y README) y #22 (mover módulos a `modelos/`, `servicios/` y `consola/`).
- HU-002 necesitó dos PRs: #23 (reglas de actualización y opción de menú) y #26 (`GestorInventario.actualizar_producto` con guardado en JSON).
- HU-004 no se integró dentro del sprint: se entregó el 25-oct junto con HU-007, 008 y 009 en el PR #32.
- Ninguna historia cambió de sprint en el tablero: HU-001, HU-002, HU-003 y HU-004 siguen asignadas al Sprint 1, pero se integraron fuera de la ventana del 19–20 oct (HU-001, T-00 y T-02 el 21-oct; HU-002 y HU-003 el 23-oct; HU-004 el 25-oct).
- HU-002 y HU-003 no empezaron antes porque necesitaban la clase `Producto` (HU-001, integrada el 21-oct 20:19) y la estructura en paquetes: sus primeros commits son del 23-oct (00:52 y 01:05), después de que el PR #22 completó esa estructura (23-oct 00:34).
- Motivo del retraso de HU-004: La historia no se integró dentro del periodo previsto del Sprint 1 debido a asuntos personales que afectaron el tiempo disponible para su desarrollo. Finalmente, se entregó el 25 de octubre de 2026 junto con las historias HU-007, HU-008 y HU-009, mediante el PR #32.

## Daily Scrum
No se realizaron Dailies formales. Ver [06-seguimiento-y-transparencia.md](06-seguimiento-y-transparencia.md).
La coordinación informal y su evidencia se describen en 06, sección 1.

## Sprint Review
Se registra en la reunión consolidada de Review y Retrospective: ver [06, sección 4](06-seguimiento-y-transparencia.md).

## Sprint Retrospective
**Hechos observables:** el trabajo se integró de 1 a 5 días después del cierre previsto del sprint; HU-004 quedó fuera del sprint; se necesitaron PRs adicionales para T-02 y HU-002.
Lo que salió bien, lo que salió mal y las mejoras acordadas se registran en [06, sección 4](06-seguimiento-y-transparencia.md).
