"""Consola de exportación a CSV (HU-013). Usa input()/print();
la escritura de archivos está en exportacion.py."""
import exportacion


def _exportar(funcion, datos, descripcion):
    """Ejecuta una exportación y muestra el resultado sin cerrar el programa."""
    datos = list(datos)
    try:
        ruta = funcion(datos)
    except ValueError as error:
        print(f"\nNo se generó ningún archivo: {error}")
    except OSError as error:
        print(f"\nError al exportar {descripcion}: {error}")
    else:
        print(f"\nArchivo generado: {ruta}")
        print(f"Registros exportados: {len(datos)}")


def menu_exportar(gestor):
    # Provisional: cuando exista el inicio de sesión (HU-007), este menú
    # solo estará disponible para el administrador.
    while True:
        print("\n===== EXPORTAR A CSV =====")
        print("1. Exportar inventario")
        print("2. Exportar historial de movimientos")
        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            _exportar(exportacion.exportar_inventario_csv,
                      gestor.consultar_productos(), "el inventario")
        elif opcion == "2":
            # Si todavía no existe el historial, se trata como vacío.
            _exportar(exportacion.exportar_movimientos_csv,
                      getattr(gestor, "movimientos", []), "los movimientos")
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")
