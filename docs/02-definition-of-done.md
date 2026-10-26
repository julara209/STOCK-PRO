# Definition of Done

Una historia de usuario solo pasa a **Done** cuando cumple **todo** lo siguiente:

1. Cumple sus criterios de aceptación (ver [Product Backlog](01-product-goal-y-backlog.md)).
2. El código funciona y respeta la estructura del proyecto (`modelos/`, `servicios/`, `consola/`, persistencia y reportes separados; las clases del dominio no usan `input()`).
3. Fue probada: tiene pruebas en `tests/` y la suite completa pasa con
   `python -m unittest discover -s tests -t .`
4. No introduce errores conocidos que afecten otras funcionalidades.
5. Está integrada en `main` mediante Pull Request.
6. Tiene trazabilidad en GitHub: Issue → rama → commits → Pull Request que referencia la historia.
7. La documentación (README y `docs/`) refleja el comportamiento implementado.
8. Cualquier integrante del equipo puede explicarla técnicamente.

Si algún punto no se cumple, la historia **no** se marca como Done y vuelve a planificarse.

## Estados del tablero

| Estado | Significado |
|---|---|
| Backlog | Trabajo identificado y pendiente de selección |
| Todo | Trabajo seleccionado para el sprint |
| In Progress | Trabajo en desarrollo |
| In Review | Pendiente de revisión |
| Done | Terminado y validado según esta Definition of Done |
