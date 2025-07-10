import datetime
import os
import getpass
from colorama import init, Fore, Style

from auth import verify_password, create_account
from database_connection import DatabaseConnection
from clientes.clientes_queries import obtener_clientes, crear_cliente, modificar_cliente, eliminar_cliente, obtener_cliente_por_id
from clientes.clientes import Cliente
from insumos.insumos_queries import (
    obtener_insumos, crear_insumo, modificar_insumo, eliminar_insumo, obtener_insumo_por_id,
    registrar_consumo, generar_reporte_consumo_costo_insumos, obtener_costos_mensuales_insumos
)
from insumos.insumos import Insumos
from proveedores.proveedores_queries import obtener_proveedores, crear_proveedor, modificar_proveedor, eliminar_proveedor, obtener_proveedor_por_id
from proveedores.proveedores import Proveedor
from maquinas.maquinas_queries import (
    obtener_maquinas, crear_maquina, modificar_maquina, eliminar_maquina, obtener_maquina_por_id,
    obtener_clientes_con_mas_maquinas
)
from maquinas.maquinas import Maquina
from tecnicos.tecnicos_queries import (
    obtener_tecnicos, crear_tecnico, modificar_tecnico, eliminar_tecnico, obtener_tecnico_por_ci,
    tecnicos_mas_mantenimientos
)
from tecnicos.tecnicos import Tecnico
from mantenimientos.mantenimientos_queries import obtener_mantenimiento, crear_mantenimiento, modificar_mantenimiento, eliminar_mantenimiento, obtener_mantenimiento_por_id
from mantenimientos.mantenimientos import Mantenimiento
from registros.registros_queries import generar_reporte_facturacion_mensual, calcular_costos_insumos_mensuales, obtener_alquileres_mensuales


class CancelOperation(Exception):
    """Excepción personalizada para señalar la cancelación de una operación."""
    pass

def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def press_enter_to_continue():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")

def get_input(prompt, required=True, input_type=str):
    """Obtiene y valida la entrada del usuario. CancelOperation si el usuario ingresa /q."""
    while True:
        value = input(prompt).strip()
        if value.lower() == '/q':
            raise CancelOperation

        if not value and required:
            print("Este campo es obligatorio.")
            continue
        if not value and not required:
            return None
        if input_type != str:
            try:
                return input_type(value)
            except ValueError:
                print(f"Entrada inválida. Por favor, ingrese un valor de tipo {input_type.__name__}.")
                continue
        return value

def get_date_input(prompt):
    """Obtiene y valida una fecha del usuario."""
    while True:
        date_str = get_input(prompt)
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            print("Formato de fecha incorrecto. Use YYYY-MM-DD.")

def manage_clientes():
    """Menú para la gestión de clientes."""
    while True:
        clear_screen()
        print("--- Gestión de Clientes ---")
        print("1. Listar todos los clientes")
        print("2. Crear un nuevo cliente")
        print("3. Modificar un cliente existente")
        print("4. Eliminar un cliente")
        print("5. Volver al menú principal")
        
        try:
            choice = get_input("Seleccione una opción: ", input_type=int)

            if choice == 1:
                clientes = obtener_clientes()
                clear_screen()
                print("--- Lista de Clientes ---")
                if not clientes:
                    print("No hay clientes para mostrar.")
                else:
                    for cliente in clientes:
                        print(cliente)
                press_enter_to_continue()

            elif choice == 2:
                clear_screen()
                print("--- Crear Nuevo Cliente ---")
                print("(Ingrese /q para cancelar)")
                nombre = get_input("Nombre: ")
                direccion = get_input("Dirección: ")
                telefono = get_input("Teléfono: ")
                correo = get_input("Correo: ")
                nuevo_cliente = Cliente(None, nombre, direccion, telefono, correo)
                crear_cliente(nuevo_cliente)
                print("\nCliente creado con éxito.")
                press_enter_to_continue()

            elif choice == 3:
                clear_screen()
                print("--- Modificar Cliente ---")
                print("(Ingrese /q para cancelar)")
                id_cliente = get_input("Ingrese el ID del cliente a modificar: ", input_type=int)
                cliente = obtener_cliente_por_id(id_cliente)
                if not cliente:
                    print("Cliente no encontrado.")
                else:
                    print("\nDatos actuales:", cliente)
                    nombre = get_input(f"Nuevo Nombre ({cliente.nombre}): ", required=False) or cliente.nombre
                    direccion = get_input(f"Nueva Dirección ({cliente.direccion}): ", required=False) or cliente.direccion
                    telefono = get_input(f"Nuevo Teléfono ({cliente.telefono}): ", required=False) or cliente.telefono
                    correo = get_input(f"Nuevo Correo ({cliente.correo}): ", required=False) or cliente.correo
                    cliente_modificado = Cliente(id_cliente, nombre, direccion, telefono, correo)
                    modificar_cliente(cliente_modificado)
                    print("\nCliente modificado con éxito.")
                press_enter_to_continue()

            elif choice == 4:
                clear_screen()
                print("--- Eliminar Cliente ---")
                print("(Ingrese /q para cancelar)")
                id_cliente = get_input("Ingrese el ID del cliente a eliminar: ", input_type=int)
                cliente = obtener_cliente_por_id(id_cliente)
                if not cliente:
                    print("Cliente no encontrado.")
                else:
                    confirm = get_input(f"¿Está seguro de que desea eliminar al cliente '{cliente.nombre}' (ID: {id_cliente})? (s/n): ").lower()
                    if confirm == 's':
                        eliminar_cliente(id_cliente)
                        print("Cliente eliminado con éxito.")
                    else:
                        print("Eliminación cancelada.")
                press_enter_to_continue()

            elif choice == 5:
                break
            else:
                print("Opción no válida.")
                press_enter_to_continue()
        except CancelOperation:
            print("\nOperación cancelada.")
            press_enter_to_continue()

def manage_insumos():
    """Menú para la gestión de insumos y consumo."""
    while True:
        clear_screen()
        print("--- Gestión de Insumos ---")
        print("1. Listar todos los insumos")
        print("2. Crear un nuevo insumo")
        print("3. Modificar un insumo existente")
        print("4. Eliminar un insumo")
        print("5. Registrar consumo de insumo")
        print("6. Volver al menú principal")

        try:
            choice = get_input("Seleccione una opción: ", input_type=int)

            if choice == 1:
                insumos = obtener_insumos()
                clear_screen()
                print("--- Lista de Insumos ---")
                if not insumos:
                    print("No hay insumos para mostrar.")
                else:
                    for insumo in insumos:
                        print(insumo)
                press_enter_to_continue()
            
            elif choice == 2:
                clear_screen()
                print("--- Crear Nuevo Insumo ---")
                print("(Ingrese /q para cancelar)")
                descripcion = get_input("Descripción: ")
                tipo = get_input("Tipo: ")
                precio_unitario = get_input("Precio Unitario: ", input_type=float)
                id_proveedor = get_input("ID Proveedor: ", input_type=int)
                nuevo_insumo = Insumos(None, descripcion, tipo, precio_unitario, id_proveedor)
                crear_insumo(nuevo_insumo)
                print("\nInsumo creado con éxito.")
                press_enter_to_continue()

            elif choice == 3:
                clear_screen()
                print("--- Modificar Insumo ---")
                print("(Ingrese /q para cancelar)")
                id_insumo = get_input("Ingrese el ID del insumo a modificar: ", input_type=int)
                insumo = obtener_insumo_por_id(id_insumo)
                if not insumo:
                    print("Insumo no encontrado.")
                else:
                    print("\nDatos actuales:", insumo)
                    descripcion = get_input(f"Nueva Descripción ({insumo.descripcion}): ", required=False) or insumo.descripcion
                    tipo = get_input(f"Nuevo Tipo ({insumo.tipo}): ", required=False) or insumo.tipo
                    precio_unitario = get_input(f"Nuevo Precio ({insumo.precio_unitario}): ", required=False, input_type=float) or insumo.precio_unitario
                    id_proveedor = get_input(f"Nuevo ID Proveedor ({insumo.id_proveedor}): ", required=False, input_type=int) or insumo.id_proveedor
                    insumo_modificado = Insumos(id_insumo, descripcion, tipo, precio_unitario, id_proveedor)
                    modificar_insumo(insumo_modificado)
                    print("\nInsumo modificado con éxito.")
                press_enter_to_continue()

            elif choice == 4:
                clear_screen()
                print("--- Eliminar Insumo ---")
                print("(Ingrese /q para cancelar)")
                id_insumo = get_input("Ingrese el ID del insumo a eliminar: ", input_type=int)
                insumo = obtener_insumo_por_id(id_insumo)
                if not insumo:
                    print("Insumo no encontrado.")
                else:
                    confirm = get_input(f"¿Está seguro de que desea eliminar el insumo '{insumo.descripcion}' (ID: {id_insumo})? (s/n): ").lower()
                    if confirm == 's':
                        eliminar_insumo(id_insumo)
                        print("Insumo eliminado con éxito.")
                    else:
                        print("Eliminación cancelada.")
                press_enter_to_continue()

            elif choice == 5:
                clear_screen()
                print("--- Registrar Consumo de Insumo ---")
                print("(Ingrese /q para cancelar)")
                id_maquina = get_input("ID de la Máquina: ", input_type=int)
                id_insumo = get_input("ID del Insumo: ", input_type=int)
                cantidad_usada = get_input("Cantidad Usada: ", input_type=int)
                fecha = get_date_input("Fecha (YYYY-MM-DD): ")
                registrar_consumo(id_maquina, id_insumo, fecha, cantidad_usada)
                print("\nConsumo registrado con éxito.")
                press_enter_to_continue()

            elif choice == 6:
                break
            else:
                print("Opción no válida.")
                press_enter_to_continue()
        except CancelOperation:
            print("\nOperación cancelada.")
            press_enter_to_continue()

def manage_mantenimientos():
    """Menú para la gestión de mantenimientos."""
    while True:
        clear_screen()
        print("--- Gestión de Mantenimientos ---")
        print("1. Listar todos los mantenimientos")
        print("2. Crear un nuevo mantenimiento")
        print("3. Modificar un mantenimiento existente")
        print("4. Eliminar un mantenimiento")
        print("5. Volver al menú principal")

        try:
            choice = get_input("Seleccione una opción: ", input_type=int)

            if choice == 1:
                mantenimientos = obtener_mantenimiento()
                clear_screen()
                print("--- Lista de Mantenimientos ---")
                if not mantenimientos:
                    print("No hay mantenimientos para mostrar.")
                else:
                    for m in mantenimientos:
                        print(m)
                press_enter_to_continue()

            elif choice == 2:
                clear_screen()
                print("--- Crear Nuevo Mantenimiento ---")
                print("(Ingrese /q para cancelar)")
                id_maquina = get_input("ID Máquina: ", input_type=int)
                ci_tecnico = get_input("CI Técnico: ")
                tipo = get_input("Tipo: ")
                fecha = get_date_input("Fecha (YYYY-MM-DD): ")
                observaciones = get_input("Observaciones: ")
                nuevo_mantenimiento = Mantenimiento(None, id_maquina, ci_tecnico, tipo, fecha, observaciones)
                crear_mantenimiento(nuevo_mantenimiento)
                print("\nMantenimiento creado con éxito.")
                press_enter_to_continue()

            elif choice == 3:
                clear_screen()
                print("--- Modificar Mantenimiento ---")
                print("(Ingrese /q para cancelar)")
                id_mantenimiento = get_input("Ingrese el ID del mantenimiento a modificar: ", input_type=int)
                mantenimiento = obtener_mantenimiento_por_id(id_mantenimiento)
                if not mantenimiento:
                    print("Mantenimiento no encontrado.")
                else:
                    print("\nDatos actuales:", mantenimiento)
                    id_maquina = get_input(f"Nuevo ID Máquina ({mantenimiento.id_maquina}): ", required=False, input_type=int) or mantenimiento.id_maquina
                    ci_tecnico = get_input(f"Nuevo CI Técnico ({mantenimiento.ci_tecnico}): ", required=False) or mantenimiento.ci_tecnico
                    tipo = get_input(f"Nuevo Tipo ({mantenimiento.tipo}): ", required=False) or mantenimiento.tipo
                    fecha_str = get_input(f"Nueva Fecha ({mantenimiento.fecha}) (YYYY-MM-DD): ", required=False)
                    fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else mantenimiento.fecha
                    observaciones = get_input(f"Nuevas Observaciones ({mantenimiento.observaciones}): ", required=False) or mantenimiento.observaciones
                    mantenimiento_modificado = Mantenimiento(id_mantenimiento, id_maquina, ci_tecnico, tipo, fecha, observaciones)
                    modificar_mantenimiento(mantenimiento_modificado)
                    print("\nMantenimiento modificado con éxito.")
                press_enter_to_continue()

            elif choice == 4:
                clear_screen()
                print("--- Eliminar Mantenimiento ---")
                print("(Ingrese /q para cancelar)")
                id_mantenimiento = get_input("Ingrese el ID del mantenimiento a eliminar: ", input_type=int)
                mantenimiento = obtener_mantenimiento_por_id(id_mantenimiento)
                if not mantenimiento:
                    print("Mantenimiento no encontrado.")
                else:
                    confirm = get_input(f"¿Está seguro de que desea eliminar el mantenimiento ID {id_mantenimiento}? (s/n): ").lower()
                    if confirm == 's':
                        eliminar_mantenimiento(id_mantenimiento)
                        print("Mantenimiento eliminado con éxito.")
                    else:
                        print("Eliminación cancelada.")
                press_enter_to_continue()

            elif choice == 5:
                break
            else:
                print("Opción no válida.")
                press_enter_to_continue()
        except CancelOperation:
            print("\nOperación cancelada.")
            press_enter_to_continue()

def manage_proveedores():
    """Menú para la gestión de proveedores (solo admin)."""
    while True:
        clear_screen()
        print("--- Gestión de Proveedores ---")
        print("1. Listar todos los proveedores")
        print("2. Crear un nuevo proveedor")
        print("3. Modificar un proveedor existente")
        print("4. Eliminar un proveedor")
        print("5. Volver al menú principal")

        try:
            choice = get_input("Seleccione una opción: ", input_type=int)

            if choice == 1:
                proveedores = obtener_proveedores()
                clear_screen()
                print("--- Lista de Proveedores ---")
                if not proveedores:
                    print("No hay proveedores para mostrar.")
                else:
                    for p in proveedores:
                        print(p)
                press_enter_to_continue()
            
            elif choice == 2:
                clear_screen()
                print("--- Crear Nuevo Proveedor ---")
                print("(Ingrese /q para cancelar)")
                nombre = get_input("Nombre: ")
                contacto = get_input("Contacto: ")
                nuevo_proveedor = Proveedor(None, nombre, contacto)
                crear_proveedor(nuevo_proveedor)
                print("\nProveedor creado con éxito.")
                press_enter_to_continue()

            elif choice == 3:
                clear_screen()
                print("--- Modificar Proveedor ---")
                print("(Ingrese /q para cancelar)")
                id_proveedor = get_input("Ingrese el ID del proveedor a modificar: ", input_type=int)
                proveedor = obtener_proveedor_por_id(id_proveedor)
                if not proveedor:
                    print("Proveedor no encontrado.")
                else:
                    print("\nDatos actuales:", proveedor)
                    nombre = get_input(f"Nuevo Nombre ({proveedor.nombre}): ", required=False) or proveedor.nombre
                    contacto = get_input(f"Nuevo Contacto ({proveedor.contacto}): ", required=False) or proveedor.contacto
                    proveedor_modificado = Proveedor(id_proveedor, nombre, contacto)
                    modificar_proveedor(proveedor_modificado)
                    print("\nProveedor modificado con éxito.")
                press_enter_to_continue()

            elif choice == 4:
                clear_screen()
                print("--- Eliminar Proveedor ---")
                print("(Ingrese /q para cancelar)")
                id_proveedor = get_input("Ingrese el ID del proveedor a eliminar: ", input_type=int)
                proveedor = obtener_proveedor_por_id(id_proveedor)
                if not proveedor:
                    print("Proveedor no encontrado.")
                else:
                    confirm = get_input(f"¿Está seguro de que desea eliminar al proveedor '{proveedor.nombre}' (ID: {id_proveedor})? (s/n): ").lower()
                    if confirm == 's':
                        eliminar_proveedor(id_proveedor)
                        print("Proveedor eliminado con éxito.")
                    else:
                        print("Eliminación cancelada.")
                press_enter_to_continue()

            elif choice == 5:
                break
            else:
                print("Opción no válida.")
                press_enter_to_continue()
        except CancelOperation:
            print("\nOperación cancelada.")
            press_enter_to_continue()

def manage_maquinas():
    """Menú para la gestión de máquinas (solo admin)."""
    while True:
        clear_screen()
        print("--- Gestión de Máquinas ---")
        print("1. Listar todas las máquinas")
        print("2. Crear una nueva máquina")
        print("3. Modificar una máquina existente")
        print("4. Eliminar una máquina")
        print("5. Volver al menú principal")

        try:
            choice = get_input("Seleccione una opción: ", input_type=int)

            if choice == 1:
                maquinas = obtener_maquinas()
                clear_screen()
                print("--- Lista de Máquinas ---")
                if not maquinas:
                    print("No hay máquinas para mostrar.")
                else:
                    for m in maquinas:
                        print(m)
                press_enter_to_continue()

            elif choice == 2:
                clear_screen()
                print("--- Crear Nueva Máquina ---")
                print("(Ingrese /q para cancelar)")
                modelo = get_input("Modelo: ")
                id_cliente = get_input("ID Cliente: ", input_type=int)
                ubicacion = get_input("Ubicación en cliente: ")
                costo = get_input("Costo alquiler mensual: ", input_type=float)
                nueva_maquina = Maquina(None, modelo, id_cliente, ubicacion, costo)
                crear_maquina(nueva_maquina)
                print("\nMáquina creada con éxito.")
                press_enter_to_continue()

            elif choice == 3:
                clear_screen()
                print("--- Modificar Máquina ---")
                print("(Ingrese /q para cancelar)")
                id_maquina = get_input("Ingrese el ID de la máquina a modificar: ", input_type=int)
                maquina = obtener_maquina_por_id(id_maquina)
                if not maquina:
                    print("Máquina no encontrada.")
                else:
                    print("\nDatos actuales:", maquina)
                    modelo = get_input(f"Nuevo Modelo ({maquina.modelo}): ", required=False) or maquina.modelo
                    id_cliente = get_input(f"Nuevo ID Cliente ({maquina.id_cliente}): ", required=False, input_type=int) or maquina.id_cliente
                    ubicacion = get_input(f"Nueva Ubicación ({maquina.ubicacion_cliente}): ", required=False) or maquina.ubicacion_cliente
                    costo = get_input(f"Nuevo Costo ({maquina.costo_alquiler_mensual}): ", required=False, input_type=float) or maquina.costo_alquiler_mensual
                    maquina_modificada = Maquina(id_maquina, modelo, id_cliente, ubicacion, costo)
                    modificar_maquina(maquina_modificada)
                    print("\nMáquina modificada con éxito.")
                press_enter_to_continue()

            elif choice == 4:
                clear_screen()
                print("--- Eliminar Máquina ---")
                print("(Ingrese /q para cancelar)")
                id_maquina = get_input("Ingrese el ID de la máquina a eliminar: ", input_type=int)
                maquina = obtener_maquina_por_id(id_maquina)
                if not maquina:
                    print("Máquina no encontrada.")
                else:
                    confirm = get_input(f"¿Está seguro de que desea eliminar la máquina '{maquina.modelo}' (ID: {id_maquina})? (s/n): ").lower()
                    if confirm == 's':
                        eliminar_maquina(id_maquina)
                        print("Máquina eliminada con éxito.")
                    else:
                        print("Eliminación cancelada.")
                press_enter_to_continue()

            elif choice == 5:
                break
            else:
                print("Opción no válida.")
                press_enter_to_continue()
        except CancelOperation:
            print("\nOperación cancelada.")
            press_enter_to_continue()

def manage_tecnicos():
    """Menú para la gestión de técnicos (solo admin)."""
    while True:
        clear_screen()
        print("--- Gestión de Técnicos ---")
        print("1. Listar todos los técnicos")
        print("2. Crear un nuevo técnico")
        print("3. Modificar un técnico existente")
        print("4. Eliminar un técnico")
        print("5. Volver al menú principal")

        try:
            choice = get_input("Seleccione una opción: ", input_type=int)

            if choice == 1:
                tecnicos = obtener_tecnicos()
                clear_screen()
                print("--- Lista de Técnicos ---")
                if not tecnicos:
                    print("No hay técnicos para mostrar.")
                else:
                    for t in tecnicos:
                        print(t)
                press_enter_to_continue()

            elif choice == 2:
                clear_screen()
                print("--- Crear Nuevo Técnico ---")
                print("(Ingrese /q para cancelar)")
                ci = get_input("CI: ")
                nombre = get_input("Nombre: ")
                apellido = get_input("Apellido: ")
                telefono = get_input("Teléfono: ")
                nuevo_tecnico = Tecnico(ci, nombre, apellido, telefono)
                crear_tecnico(nuevo_tecnico)
                print("\nTécnico creado con éxito.")
                press_enter_to_continue()

            elif choice == 3:
                clear_screen()
                print("--- Modificar Técnico ---")
                print("(Ingrese /q para cancelar)")
                ci_tecnico = get_input("Ingrese la CI del técnico a modificar: ")
                tecnico = obtener_tecnico_por_ci(ci_tecnico)
                if not tecnico:
                    print("Técnico no encontrado.")
                else:
                    print("\nDatos actuales:", tecnico)
                    nombre = get_input(f"Nuevo Nombre ({tecnico.nombre}): ", required=False) or tecnico.nombre
                    apellido = get_input(f"Nuevo Apellido ({tecnico.apellido}): ", required=False) or tecnico.apellido
                    telefono = get_input(f"Nuevo Teléfono ({tecnico.telefono}): ", required=False) or tecnico.telefono
                    tecnico_modificado = Tecnico(ci_tecnico, nombre, apellido, telefono)
                    modificar_tecnico(tecnico_modificado)
                    print("\nTécnico modificado con éxito.")
                press_enter_to_continue()

            elif choice == 4:
                clear_screen()
                print("--- Eliminar Técnico ---")
                print("(Ingrese /q para cancelar)")
                ci_tecnico = get_input("Ingrese la CI del técnico a eliminar: ")
                tecnico = obtener_tecnico_por_ci(ci_tecnico)
                if not tecnico:
                    print("Técnico no encontrado.")
                else:
                    confirm = get_input(f"¿Está seguro de que desea eliminar al técnico '{tecnico.nombre} {tecnico.apellido}' (CI: {ci_tecnico})? (s/n): ").lower()
                    if confirm == 's':
                        eliminar_tecnico(ci_tecnico)
                        print("Técnico eliminado con éxito.")
                    else:
                        print("Eliminación cancelada.")
                press_enter_to_continue()

            elif choice == 5:
                break
            else:
                print("Opción no válida.")
                press_enter_to_continue()
        except CancelOperation:
            print("\nOperación cancelada.")
            press_enter_to_continue()

def execute_sql_console():
    """Permite a un administrador ejecutar consultas SQL directamente."""
    clear_screen()
    print("--- Consola SQL ---")
    print("ADVERTENCIA: Está a punto de ejecutar consultas SQL directamente en la base de datos.")
    print("Esto puede alterar o eliminar datos de forma permanente. Proceda con precaución.")
    print("Ingrese su consulta. Para terminar, escriba la consulta y presione Enter.")
    print("Ingrese /q para salir.")

    try:
        query = get_input("SQL> ", required=True)

        db = DatabaseConnection()
        if not db.connection:
            print("No se pudo establecer la conexión con la base de datos.")
            press_enter_to_continue()
            return

        if query.strip().lower().startswith('select'):
            results = db.execute_query(query)
            db.close_connection()
            if results is None:
                print("\nLa consulta no se pudo ejecutar.")
            elif not results:
                print("\nLa consulta se ejecutó correctamente, pero no devolvió filas.")
            else:
                headers = results[0].keys()
                col_widths = {h: len(h) for h in headers}
                for row in results:
                    for h in headers:
                        col_widths[h] = max(col_widths[h], len(str(row[h])))
                
                header_line = " | ".join([h.ljust(col_widths[h]) for h in headers])
                print("\n" + header_line)
                print("-" * len(header_line))

                for row in results:
                    row_line = " | ".join([str(row[h]).ljust(col_widths[h]) for h in headers])
                    print(row_line)
        else:
            last_id = db.execute_modification(query)
            db.close_connection()
            if last_id is not None:
                print(f"Consulta de modificación ejecutada. Último ID insertado (si aplica): {last_id}")

    except CancelOperation:
        print("\nSaliendo de la consola SQL.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")
    
    press_enter_to_continue()

def reports_menu():
    """Menú para visualizar los reportes."""
    while True:
        clear_screen()
        print("--- Menú de Reportes ---")
        print("1. Facturación Mensual por Cliente") #5a) Total mensual a cobrar a cada cliente (suma de alquiler de máquinas más costo de insumos consumidos)
        print("2. Consumo y Costo de Insumos") #5b) Insumos con mayor consumo y costos.
        print("3. Técnicos con Más Mantenimientos") #5c) Técnicos con más mantenimientos realizados.
        print("4. Clientes con Más Máquinas") #5d) Clientes con más máquinas alquiladas.
        print("5. Costos de Insumos por Máquina (Mensual)") #4b) Respetar las restricciones: Los consumos deben registrarse con fecha para permitir calculo de facturación mensual.
        print("6. Alquileres Mensuales por Máquina") #3) Registrar el alquiler mensual fijo por máquina que se cobra a cada cliente.
        print("7. Registro de Consumo de Insumos por Máquina y Fecha") #2) Registrar el consumo de insumos por máquina y fecha (registro_consumo) para poder calcular los costos mensuales de insumos consumidos.
        print("8. Volver al menú principal")

        try:
            choice = get_input("Seleccione una opción: ", input_type=int)

            if choice == 1:
                clear_screen()
                print("--- Reporte de Facturación Mensual ---")
                print("(Ingrese /q para cancelar)")
                anio = get_input("Ingrese el año (YYYY): ", input_type=int)
                mes = get_input("Ingrese el mes (MM): ", input_type=int)
                reporte = generar_reporte_facturacion_mensual(anio, mes)
                if not reporte:
                    print("No hay datos para el período seleccionado.")
                else:
                    print(f"\n--- Reporte para {mes:02d}/{anio} ---")
                    print(f"{'ID Cliente':<12} {'Nombre':<30} {'Total Alquiler':<20} {'Total Insumos':<20} {'Total a Cobrar':<20}")
                    print("-" * 102)
                    for r in reporte:
                        print(f"{r['id_cliente']:<12} {r['nombre_cliente']:<30} ${r['total_alquiler']:<19.2f} ${r['total_insumos']:<19.2f} ${r['total_a_cobrar']:<19.2f}")
                press_enter_to_continue()

            elif choice == 2:
                clear_screen()
                print("--- Reporte de Consumo y Costo de Insumos ---")
                reporte = generar_reporte_consumo_costo_insumos()
                if not reporte:
                    print("No hay datos de consumo para mostrar.")
                else:
                    print(f"{'ID Insumo':<10} {'Descripción':<30} {'Tipo':<15} {'Consumo Total':<15} {'Costo Total':<15}")
                    print("-" * 85)
                    for r in reporte:
                        print(f"{r['id_insumo']:<10} {r['descripcion']:<30} {r['tipo']:<15} {r['total_cantidad_consumida']:<15} ${r['costo_total']:<14.2f}")
                press_enter_to_continue()

            elif choice == 3:
                clear_screen()
                print("--- Reporte de Técnicos con Más Mantenimientos ---")
                reporte = tecnicos_mas_mantenimientos()
                if not reporte:
                    print("No hay datos de mantenimientos para mostrar.")
                else:
                    print(f"{'CI Técnico':<15} {'Nombre':<30} {'Mantenimientos':<15}")
                    print("-" * 60)
                    for r in reporte:
                        print(f"{r['ci']:<15} {r['tecnico']:<30} {r['total_mantenimientos']:<15}")
                press_enter_to_continue()

            elif choice == 4:
                clear_screen()
                print("--- Reporte de Clientes con Más Máquinas ---")
                print("(Ingrese /q para cancelar)")
                limit = get_input("¿Cuántos clientes desea mostrar? (ej: 5): ", input_type=int)
                reporte = obtener_clientes_con_mas_maquinas(limit)
                if not reporte:
                    print("No hay datos de máquinas para mostrar.")
                else:
                    print(f"{'ID Cliente':<12} {'Nombre':<30} {'Cantidad de Máquinas':<25}")
                    print("-" * 67)
                    for r in reporte:
                        print(f"{r['id']:<12} {r['nombre']:<30} {r['cantidad_maquinas']:<25}")
                press_enter_to_continue()

            elif choice == 5:
                clear_screen()
                print("--- Reporte de Costos de Insumos por Máquina (Mensual) ---")
                print("(Ingrese /q para cancelar)")
                anio = get_input("Ingrese el año (YYYY): ", input_type=int)
                mes = get_input("Ingrese el mes (MM): ", input_type=int)
                reporte = calcular_costos_insumos_mensuales(anio, mes)
                if not reporte:
                    print("No hay datos de costos para el período seleccionado.")
                else:
                    print(f"\n--- Reporte para {mes:02d}/{anio} ---")
                    print(f"{'ID Máquina':<15} {'Costo Total Insumos':<25}")
                    print("-" * 40)
                    for r in reporte:
                        print(f"{r['id_maquina']:<15} ${r['total_costo']:<24.2f}")
                press_enter_to_continue()

            elif choice == 6:
                clear_screen()
                print("--- Reporte de Alquileres Mensuales por Máquina ---")
                reporte = obtener_alquileres_mensuales()
                if not reporte:
                    print("No hay datos de alquileres para mostrar.")
                else:
                    print(f"{'ID Cliente':<12} {'Nombre Cliente':<30} {'ID Máquina':<12} {'Alquiler Mensual':<20}")
                    print("-" * 74)
                    for r in reporte:
                        print(f"{r['id_cliente']:<12} {r['nombre_cliente']:<30} {r['id_maquina']:<12} ${r['costo_alquiler_mensual']:<19.2f}")
                press_enter_to_continue()

            elif choice == 7:
                clear_screen()
                print("--- Reporte de Registro de Consumo de Insumos por Máquina y Fecha ---")
                print("(Ingrese /q para cancelar)")
                anio = get_input("Ingrese el año (YYYY): ", input_type=int)
                mes = get_input("Ingrese el mes (MM): ", input_type=int)
                reporte = obtener_costos_mensuales_insumos(anio, mes)
                if not reporte:
                    print("No hay datos de consumo para el período seleccionado.")
                else:
                    print(f"\n--- Reporte para {mes:02d}/{anio} ---")
                    print(f"{'ID Máquina':<15} {'ID Insumo':<12} {'Fecha':<12} {'Cantidad Usada':<15}")
                    print("-" * 60)
                    for r in reporte:
                        print(f"{r['id_maquina']:<15} {r['id_insumo']:<12} {r['fecha'].strftime('%Y-%m-%d'):<12} {r['cantidad_usada']:<15}")
                press_enter_to_continue()

            elif choice == 8:
                break
            else:
                print("Opción no válida.")
                press_enter_to_continue()
        except CancelOperation:
            print("\nOperación cancelada.")
            press_enter_to_continue()

def login_flow():
    """Gestiona el login o la creación de una cuenta."""
    while True:
        clear_screen()
        print("--- Bienvenido a Cafés Marloy ---")
        print("\n1. Iniciar sesión")
        print("2. Crear cuenta")
        print("3. Salir")
        
        try:
            choice = get_input("Seleccione una opción: ", input_type=int)

            if choice == 1:
                print("\n(Ingrese /q para cancelar)")
                email = get_input("Correo: ")
                password = getpass.getpass("Contraseña: ")
                user_info = verify_password(email, password)
                if user_info:
                    print("\nInicio de sesión exitoso.")
                    press_enter_to_continue()
                    return user_info
                else:
                    print("\nCorreo o contraseña incorrectos.")
                    press_enter_to_continue()
            elif choice == 2:
                print("\n(Ingrese /q para cancelar)")
                email = get_input("Nuevo Correo: ")
                password = getpass.getpass("Nueva Contraseña: ")
                is_admin_input = get_input("¿Es administrador? (s/n): ").lower()
                is_admin = is_admin_input == 's'
                user_id = create_account(email, password, is_admin)
                if user_id is not None:
                    print("\nCuenta creada exitosamente.")
                else:
                    print("\nEl correo ya existe. Por favor, elija otro.")
                press_enter_to_continue()
            elif choice == 3:
                return None
            else:
                print("Opción no válida.")
                press_enter_to_continue()
        except CancelOperation:
            print("\nOperación cancelada.")
            press_enter_to_continue()

def main_menu(user_info):
    """Muestra el menú principal y gestiona la navegación."""
    is_admin = user_info['es_administrador']

    while True:
        clear_screen()
        print(f"--- Menú Principal (Usuario: {user_info['correo']}) ---")
        print("1. Gestionar Clientes")
        print("2. Gestionar Insumos")
        print("3. Gestionar Mantenimientos")
        print("4. Ver Reportes")
        
        admin_base_choice = 5
        if is_admin:
            init()
            print(Fore.BLUE +  f"{admin_base_choice}. Gestionar Proveedores" + Style.RESET_ALL)
            print(Fore.BLUE +  f"{admin_base_choice + 1}. Gestionar Máquinas" + Style.RESET_ALL)
            print(Fore.BLUE +  f"{admin_base_choice + 2}. Gestionar Técnicos" + Style.RESET_ALL)
            print(Fore.BLUE +  f"{admin_base_choice + 3}. Ejecutar SQL" + Style.RESET_ALL)

        exit_choice = admin_base_choice + 4 if is_admin else admin_base_choice
        print(f"{exit_choice}. Salir")

        try:
            choice = get_input("Seleccione una opción: ", input_type=int)

            if choice == 1: manage_clientes()
            elif choice == 2: manage_insumos()
            elif choice == 3: manage_mantenimientos()
            elif choice == 4: reports_menu()
            elif choice == exit_choice:
                print(Fore.RED + "Sesión finalizada..." + Style.RESET_ALL)
                break
            elif is_admin:
                if choice == admin_base_choice: manage_proveedores()
                elif choice == admin_base_choice + 1: manage_maquinas()
                elif choice == admin_base_choice + 2: manage_tecnicos()
                elif choice == admin_base_choice + 3: execute_sql_console()
                else:
                    print("Opción no válida.")
                    press_enter_to_continue()
            else:
                print("Opción no válida o no tiene permisos.")
                press_enter_to_continue()
        except CancelOperation:
            print("\nOperación cancelada.")
            press_enter_to_continue()
        except (ValueError, TypeError):
             print("Opción no válida.")
             press_enter_to_continue()

if __name__ == "__main__":
    user = login_flow()
    if user:
        main_menu(user)