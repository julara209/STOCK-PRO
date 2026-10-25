"""Consola de salida de mercancía (HU-005). Usa input()/print();
las reglas de negocio están en servicios/salidas.py y en el gestor."""


def menu_registrar_salida(gestor, usuario=None):
    print("\n--- Registrar salida de mercancía ---")
    codigo = input("Código del producto: ").strip()

    producto = gestor.buscar_producto(codigo)
    if producto is None:
        print(f"\nSalida rechazada: El producto '{codigo}' no existe.")
        return

    print(f"Producto: {producto.nombre} | Existencias: {producto.cantidad}")

    try:
        texto = input("Cantidad que sale: ").strip()
        try:
            cantidad = int(texto)
        except ValueError:
            raise ValueError(f"'{texto}' no es un número entero válido.") from None

        # Con sesión iniciada, el responsable es el usuario de la sesión.
        if usuario is None:
            usuario = input("Usuario responsable: ").strip()

        movimiento = gestor.registrar_salida(codigo, cantidad, usuario)
    except ValueError as error:
        print(f"\nSalida rechazada: {error}")
    except OSError as error:
        print(f"\nError al guardar: {error}")
    else:
        print("\nSalida registrada correctamente.")
        print(movimiento)
        print(f"Existencias restantes: {gestor.buscar_producto(codigo).cantidad}")
