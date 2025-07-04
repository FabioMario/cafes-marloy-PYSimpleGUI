import PySimpleGUI as sg
from auth import verify_password, create_account
from clientes.clientes_queries import obtener_clientes, crear_cliente, modificar_cliente, eliminar_cliente
from clientes.clientes import Cliente
from insumos.insumos_queries import obtener_insumos, crear_insumo, eliminar_insumo, obtener_insumo_por_id
from insumos.insumos import Insumos
from proveedores.proveedores_queries import obtener_proveedores, crear_proveedor, modificar_proveedor, eliminar_proveedor, obtener_proveedor_por_id
from proveedores.proveedores import Proveedor
from maquinas.maquinas_queries import obtener_maquinas, crear_maquina, modificar_maquina, eliminar_maquina, obtener_maquina_por_id
from maquinas.maquinas import Maquina
from tecnicos.tecnicos_queries import obtener_tecnicos, crear_tecnico, modificar_tecnico, eliminar_tecnico, obtener_tecnico_por_ci
from tecnicos.tecnicos import Tecnico
from mantenimientos.mantenimientos_queries import obtener_mantenimiento, crear_mantenimiento, modificar_mantenimiento, eliminar_mantenimiento, obtener_mantenimiento_por_id
from mantenimientos.mantenimientos import Mantenimiento

def show_error(message):
    """Muestra un popup de error estandarizado."""
    sg.popup_error(message, title="Error")

def mantenimientos_window():
    """Ventana principal para la gestión de mantenimientos."""

    def refresh_table():
        try:
            return [[m.id, m.id_maquina, m.ci_tecnico, m.tipo, m.fecha, m.observaciones] for m in obtener_mantenimiento()]
        except Exception as e:
            show_error(f"Error al cargar los mantenimientos: {e}")
            return []

    headings = ["ID", "ID Máquina", "CI Técnico", "Tipo", "Fecha", "Observaciones"]
    mantenimiento_data = refresh_table()

    layout = [
        [sg.Text("Gestión de Mantenimientos", font=("Helvetica", 25))],
        [sg.Table(values=mantenimiento_data, headings=headings, max_col_width=35,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification="right",
                    num_rows=15,
                    key="-TABLE-",
                    row_height=35,
                    tooltip="Lista de Mantenimientos")],
        [sg.Button("Crear Mantenimiento"), sg.Button("Modificar Mantenimiento"), sg.Button("Eliminar Mantenimiento"), sg.Button("Salir")]
    ]

    window = sg.Window("Mantenimientos", layout, resizable=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Salir":
            break

        selected_row = values["-TABLE-"]

        if event == "Crear Mantenimiento":
            if create_or_edit_mantenimiento_window():
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Modificar Mantenimiento":
            if not selected_row:
                sg.popup("Por favor, seleccione un mantenimiento de la tabla para modificar.")
                continue
            
            mantenimiento_id = mantenimiento_data[selected_row[0] - 1][0]
            if create_or_edit_mantenimiento_window(mantenimiento_id=mantenimiento_id):
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Eliminar Mantenimiento":
            if not selected_row:
                sg.popup("Por favor, seleccione un mantenimiento de la tabla para eliminar.")
                continue

            mantenimiento_id = mantenimiento_data[selected_row[0] - 1][0]
            
            confirm = sg.popup_yes_no(f"¿Está seguro de que desea eliminar el mantenimiento con ID {mantenimiento_id}?", title="Confirmar Eliminación")
            
            if confirm == "Yes":
                try:
                    eliminar_mantenimiento(mantenimiento_id)
                    sg.popup("Mantenimiento eliminado con éxito.")
                    window["-TABLE-"].update(values=refresh_table())
                except Exception as e:
                    show_error(f"Error al eliminar el mantenimiento: {e}")

    window.close()

def create_or_edit_mantenimiento_window(mantenimiento_id=None):
    """Ventana para crear o editar un mantenimiento. Si se provee mantenimiento_id, es modo edición."""
    
    is_edit = mantenimiento_id is not None
    title = "Modificar Mantenimiento" if is_edit else "Crear Mantenimiento"
    
    initial_data = {"id_maquina": "", "ci_tecnico": "", "tipo": "", "fecha": "", "observaciones": ""}
    if is_edit:
        try:
            mantenimiento = obtener_mantenimiento_por_id(mantenimiento_id)
            if mantenimiento:
                initial_data["id_maquina"] = mantenimiento.id_maquina
                initial_data["ci_tecnico"] = mantenimiento.ci_tecnico
                initial_data["tipo"] = mantenimiento.tipo
                initial_data["fecha"] = mantenimiento.fecha.strftime("%Y-%m-%d") # Format date for display
                initial_data["observaciones"] = mantenimiento.observaciones
            else:
                show_error(f"No se encontró el mantenimiento con ID {mantenimiento_id}")
                return False
        except Exception as e:
            show_error(f"Error al cargar el mantenimiento: {e}")
            return False

    layout = [
        [sg.Text(title, font=("Helvetica", 20))],
        [sg.Text("ID Máquina:", size=(15,1)), sg.Input(initial_data["id_maquina"], key="-ID_MAQUINA-")],
        [sg.Text("CI Técnico:", size=(15,1)), sg.Input(initial_data["ci_tecnico"], key="-CI_TECNICO-")],
        [sg.Text("Tipo:", size=(15,1)), sg.Input(initial_data["tipo"], key="-TIPO-")],
        [sg.Text("Fecha (YYYY-MM-DD):", size=(15,1)), sg.Input(initial_data["fecha"], key="-FECHA-")],
        [sg.Text("Observaciones:", size=(15,1)), sg.Input(initial_data["observaciones"], key="-OBSERVACIONES-")],
        [sg.Button("Guardar"), sg.Button("Cancelar")]
    ]

    window = sg.Window(title, layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancelar":
            window.close()
            return False

        if event == "Guardar":
            id_maquina = values["-ID_MAQUINA-"]
            ci_tecnico = values["-CI_TECNICO-"]
            tipo = values["-TIPO-"]
            fecha_str = values["-FECHA-"]
            observaciones = values["-OBSERVACIONES-"]

            if not all([id_maquina, ci_tecnico, tipo, fecha_str, observaciones]):
                sg.popup("Todos los campos son obligatorios.")
                continue
            
            try:
                id_maquina = int(id_maquina)
                tipo = int(tipo)
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

                if is_edit:
                    mantenimiento_actualizado = Mantenimiento(mantenimiento_id, id_maquina, ci_tecnico, tipo, fecha, observaciones)
                    modificar_mantenimiento(mantenimiento_actualizado)
                    sg.popup("Mantenimiento modificado con éxito.")
                else:
                    nuevo_mantenimiento = Mantenimiento(None, id_maquina, ci_tecnico, tipo, fecha, observaciones)
                    crear_mantenimiento(nuevo_mantenimiento)
                    sg.popup("Mantenimiento creado con éxito.")
                
                window.close()
                return True
            except ValueError:
                sg.popup("ID Máquina, Tipo y Fecha deben ser válidos (Fecha en formato YYYY-MM-DD).")
            except Exception as e:
                show_error(f"Error al guardar el mantenimiento: {e}")

def tecnicos_window():
    """Ventana principal para la gestión de técnicos."""

    def refresh_table():
        try:
            return [[t.ci, t.nombre, t.apellido, t.telefono] for t in obtener_tecnicos()]
        except Exception as e:
            show_error(f"Error al cargar los técnicos: {e}")
            return []

    headings = ["CI", "Nombre", "Apellido", "Teléfono"]
    tecnico_data = refresh_table()

    layout = [
        [sg.Text("Gestión de Técnicos", font=("Helvetica", 25))],
        [sg.Table(values=tecnico_data, headings=headings, max_col_width=35,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification="right",
                    num_rows=15,
                    key="-TABLE-",
                    row_height=35,
                    tooltip="Lista de Técnicos")],
        [sg.Button("Crear Técnico"), sg.Button("Modificar Técnico"), sg.Button("Eliminar Técnico"), sg.Button("Salir")]
    ]

    window = sg.Window("Técnicos", layout, resizable=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Salir":
            break

        selected_row = values["-TABLE-"]

        if event == "Crear Técnico":
            if create_or_edit_tecnico_window():
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Modificar Técnico":
            if not selected_row:
                sg.popup("Por favor, seleccione un técnico de la tabla para modificar.")
                continue
            
            tecnico_ci = tecnico_data[selected_row[0] - 1][0]
            if create_or_edit_tecnico_window(tecnico_ci=tecnico_ci):
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Eliminar Técnico":
            if not selected_row:
                sg.popup("Por favor, seleccione un técnico de la tabla para eliminar.")
                continue

            tecnico_ci = tecnico_data[selected_row[0] - 1][0]
            tecnico_nombre = tecnico_data[selected_row[0] - 1][1]
            
            confirm = sg.popup_yes_no(f"¿Está seguro de que desea eliminar al técnico \"{tecnico_nombre}\"", title="Confirmar Eliminación")
            
            if confirm == "Yes":
                try:
                    eliminar_tecnico(tecnico_ci)
                    sg.popup("Técnico eliminado con éxito.")
                    window["-TABLE-"].update(values=refresh_table())
                except Exception as e:
                    show_error(f"Error al eliminar el técnico: {e}")

    window.close()

def create_or_edit_tecnico_window(tecnico_ci=None):
    """Ventana para crear o editar un técnico. Si se provee tecnico_ci, es modo edición."""
    
    is_edit = tecnico_ci is not None
    title = "Modificar Técnico" if is_edit else "Crear Técnico"
    
    initial_data = {"ci": "", "nombre": "", "apellido": "", "telefono": ""}
    if is_edit:
        try:
            tecnico = obtener_tecnico_por_ci(tecnico_ci)
            if tecnico:
                initial_data["ci"] = tecnico.ci
                initial_data["nombre"] = tecnico.nombre
                initial_data["apellido"] = tecnico.apellido
                initial_data["telefono"] = tecnico.telefono
            else:
                show_error(f"No se encontró el técnico con CI {tecnico_ci}")
                return False
        except Exception as e:
            show_error(f"Error al cargar el técnico: {e}")
            return False

    layout = [
        [sg.Text(title, font=("Helvetica", 20))],
        [sg.Text("CI:", size=(10,1)), sg.Input(initial_data["ci"], key="-CI-", disabled=is_edit)],
        [sg.Text("Nombre:", size=(10,1)), sg.Input(initial_data["nombre"], key="-NOMBRE-")],
        [sg.Text("Apellido:", size=(10,1)), sg.Input(initial_data["apellido"], key="-APELLIDO-")],
        [sg.Text("Teléfono:", size=(10,1)), sg.Input(initial_data["telefono"], key="-TELEFONO-")],
        [sg.Button("Guardar"), sg.Button("Cancelar")]
    ]

    window = sg.Window(title, layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancelar":
            window.close()
            return False

        if event == "Guardar":
            ci = values["-CI-"]
            nombre = values["-NOMBRE-"]
            apellido = values["-APELLIDO-"]
            telefono = values["-TELEFONO-"]

            if not all([ci, nombre, apellido, telefono]):
                sg.popup("Todos los campos son obligatorios.")
                continue
            
            try:
                if is_edit:
                    tecnico_actualizado = Tecnico(ci, nombre, apellido, telefono)
                    modificar_tecnico(tecnico_actualizado)
                    sg.popup("Técnico modificado con éxito.")
                else:
                    nuevo_tecnico = Tecnico(ci, nombre, apellido, telefono)
                    crear_tecnico(nuevo_tecnico)
                    sg.popup("Técnico creado con éxito.")
                
                window.close()
                return True
            except Exception as e:
                show_error(f"Error al guardar el técnico: {e}")

def maquinas_window():
    """Ventana principal para la gestión de máquinas."""

    def refresh_table():
        try:
            return [[m.id, m.modelo, m.id_cliente, m.ubicacion_cliente, m.costo_alquiler_mensual] for m in obtener_maquinas()]
        except Exception as e:
            show_error(f"Error al cargar las máquinas: {e}")
            return []

    headings = ["ID", "Modelo", "ID Cliente", "Ubicación Cliente", "Costo Alquiler Mensual"]
    maquina_data = refresh_table()

    layout = [
        [sg.Text("Gestión de Máquinas", font=("Helvetica", 25))],
        [sg.Table(values=maquina_data, headings=headings, max_col_width=35,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification="right",
                    num_rows=15,
                    key="-TABLE-",
                    row_height=35,
                    tooltip="Lista de Máquinas")],
        [sg.Button("Crear Máquina"), sg.Button("Modificar Máquina"), sg.Button("Eliminar Máquina"), sg.Button("Salir")]
    ]

    window = sg.Window("Máquinas", layout, resizable=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Salir":
            break

        selected_row = values["-TABLE-"]

        if event == "Crear Máquina":
            if create_or_edit_maquina_window():
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Modificar Máquina":
            if not selected_row:
                sg.popup("Por favor, seleccione una máquina de la tabla para modificar.")
                continue
            
            maquina_id = maquina_data[selected_row[0] - 1][0]
            if create_or_edit_maquina_window(maquina_id=maquina_id):
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Eliminar Máquina":
            if not selected_row:
                sg.popup("Por favor, seleccione una máquina de la tabla para eliminar.")
                continue

            maquina_id = maquina_data[selected_row[0] - 1][0]
            maquina_modelo = maquina_data[selected_row[0] - 1][1]
            
            confirm = sg.popup_yes_no(f"¿Está seguro de que desea eliminar la máquina \"{maquina_modelo}\"", title="Confirmar Eliminación")
            
            if confirm == "Yes":
                try:
                    eliminar_maquina(maquina_id)
                    sg.popup("Máquina eliminada con éxito.")
                    window["-TABLE-"].update(values=refresh_table())
                except Exception as e:
                    show_error(f"Error al eliminar la máquina: {e}")

    window.close()

def create_or_edit_maquina_window(maquina_id=None):
    """Ventana para crear o editar una máquina. Si se provee maquina_id, es modo edición."""
    
    is_edit = maquina_id is not None
    title = "Modificar Máquina" if is_edit else "Crear Máquina"
    
    initial_data = {"modelo": "", "id_cliente": "", "ubicacion_cliente": "", "costo_alquiler_mensual": ""}
    if is_edit:
        try:
            maquina = obtener_maquina_por_id(maquina_id)
            if maquina:
                initial_data["modelo"] = maquina.modelo
                initial_data["id_cliente"] = maquina.id_cliente
                initial_data["ubicacion_cliente"] = maquina.ubicacion_cliente
                initial_data["costo_alquiler_mensual"] = maquina.costo_alquiler_mensual
            else:
                show_error(f"No se encontró la máquina con ID {maquina_id}")
                return False
        except Exception as e:
            show_error(f"Error al cargar la máquina: {e}")
            return False

    layout = [
        [sg.Text(title, font=("Helvetica", 20))],
        [sg.Text("Modelo:", size=(20,1)), sg.Input(initial_data["modelo"], key="-MODELO-")],
        [sg.Text("ID Cliente:", size=(20,1)), sg.Input(initial_data["id_cliente"], key="-ID_CLIENTE-")],
        [sg.Text("Ubicación Cliente:", size=(20,1)), sg.Input(initial_data["ubicacion_cliente"], key="-UBICACION_CLIENTE-")],
        [sg.Text("Costo Alquiler Mensual:", size=(20,1)), sg.Input(initial_data["costo_alquiler_mensual"], key="-COSTO_ALQUILER_MENSUAL-")],
        [sg.Button("Guardar"), sg.Button("Cancelar")]
    ]

    window = sg.Window(title, layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancelar":
            window.close()
            return False

        if event == "Guardar":
            modelo = values["-MODELO-"]
            id_cliente = values["-ID_CLIENTE-"]
            ubicacion_cliente = values["-UBICACION_CLIENTE-"]
            costo_alquiler_mensual = values["-COSTO_ALQUILER_MENSUAL-"]

            if not all([modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual]):
                sg.popup("Todos los campos son obligatorios.")
                continue
            
            try:
                id_cliente = int(id_cliente)
                costo_alquiler_mensual = float(costo_alquiler_mensual)

                if is_edit:
                    maquina_actualizada = Maquina(maquina_id, modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual)
                    modificar_maquina(maquina_actualizada)
                    sg.popup("Máquina modificada con éxito.")
                else:
                    nueva_maquina = Maquina(None, modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual)
                    crear_maquina(nueva_maquina)
                    sg.popup("Máquina creada con éxito.")
                
                window.close()
                return True
            except ValueError:
                sg.popup("ID Cliente y Costo Alquiler Mensual deben ser números válidos.")
            except Exception as e:
                show_error(f"Error al guardar la máquina: {e}")

def proveedores_window():
    """Ventana principal para la gestión de proveedores."""

    def refresh_table():
        try:
            return [[p.id, p.nombre, p.contacto] for p in obtener_proveedores()]
        except Exception as e:
            show_error(f"Error al cargar los proveedores: {e}")
            return []

    headings = ["ID", "Nombre", "Contacto"]
    proveedor_data = refresh_table()

    layout = [
        [sg.Text("Gestión de Proveedores", font=("Helvetica", 25))],
        [sg.Table(values=proveedor_data, headings=headings, max_col_width=35,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification="right",
                    num_rows=15,
                    key="-TABLE-",
                    row_height=35,
                    tooltip="Lista de Proveedores")],
        [sg.Button("Crear Proveedor"), sg.Button("Modificar Proveedor"), sg.Button("Eliminar Proveedor"), sg.Button("Salir")]
    ]

    window = sg.Window("Proveedores", layout, resizable=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Salir":
            break

        selected_row = values["-TABLE-"]

        if event == "Crear Proveedor":
            if create_or_edit_proveedor_window():
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Modificar Proveedor":
            if not selected_row:
                sg.popup("Por favor, seleccione un proveedor de la tabla para modificar.")
                continue
            
            proveedor_id = proveedor_data[selected_row[0] - 1][0]
            if create_or_edit_proveedor_window(proveedor_id=proveedor_id):
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Eliminar Proveedor":
            if not selected_row:
                sg.popup("Por favor, seleccione un proveedor de la tabla para eliminar.")
                continue

            proveedor_id = proveedor_data[selected_row[0] - 1][0]
            proveedor_nombre = proveedor_data[selected_row[0] - 1][1]
            
            confirm = sg.popup_yes_no(f"¿Está seguro de que desea eliminar al proveedor \"{proveedor_nombre}\"", title="Confirmar Eliminación")
            
            if confirm == "Yes":
                try:
                    eliminar_proveedor(proveedor_id)
                    sg.popup("Proveedor eliminado con éxito.")
                    window["-TABLE-"].update(values=refresh_table())
                except Exception as e:
                    show_error(f"Error al eliminar el proveedor: {e}")

    window.close()

def create_or_edit_proveedor_window(proveedor_id=None):
    """Ventana para crear o editar un proveedor. Si se provee proveedor_id, es modo edición."""
    
    is_edit = proveedor_id is not None
    title = "Modificar Proveedor" if is_edit else "Crear Proveedor"
    
    initial_data = {"nombre": "", "contacto": ""}
    if is_edit:
        try:
            proveedor = obtener_proveedor_por_id(proveedor_id)
            if proveedor:
                initial_data["nombre"] = proveedor.nombre
                initial_data["contacto"] = proveedor.contacto
            else:
                show_error(f"No se encontró el proveedor con ID {proveedor_id}")
                return False
        except Exception as e:
            show_error(f"Error al cargar el proveedor: {e}")
            return False

    layout = [
        [sg.Text(title, font=("Helvetica", 20))],
        [sg.Text("Nombre:", size=(10,1)), sg.Input(initial_data["nombre"], key="-NOMBRE-")],
        [sg.Text("Contacto:", size=(10,1)), sg.Input(initial_data["contacto"], key="-CONTACTO-")],
        [sg.Button("Guardar"), sg.Button("Cancelar")]
    ]

    window = sg.Window(title, layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancelar":
            window.close()
            return False

        if event == "Guardar":
            nombre = values["-NOMBRE-"]
            contacto = values["-CONTACTO-"]

            if not all([nombre, contacto]):
                sg.popup("Todos los campos son obligatorios.")
                continue
            
            try:
                if is_edit:
                    proveedor_actualizado = Proveedor(proveedor_id, nombre, contacto)
                    modificar_proveedor(proveedor_actualizado)
                    sg.popup("Proveedor modificado con éxito.")
                else:
                    nuevo_proveedor = Proveedor(None, nombre, contacto)
                    crear_proveedor(nuevo_proveedor)
                    sg.popup("Proveedor creado con éxito.")
                
                window.close()
                return True
            except Exception as e:
                show_error(f"Error al guardar el proveedor: {e}")

def insumos_window():
    """Ventana principal para la gestión de insumos."""

    def refresh_table():
        try:
            return [[i.id, i.descripcion, i.tipo, i.precio_unitario, i.id_proveedor] for i in obtener_insumos()]
        except Exception as e:
            show_error(f"Error al cargar los insumos: {e}")
            return []

    headings = ["ID", "Descripción", "Tipo", "Precio Unitario", "ID Proveedor"]
    insumo_data = refresh_table()

    layout = [
        [sg.Text("Gestión de Insumos", font=("Helvetica", 25))],
        [sg.Table(values=insumo_data, headings=headings, max_col_width=35,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification="right",
                    num_rows=15,
                    key="-TABLE-",
                    row_height=35,
                    tooltip="Lista de Insumos")],
        [sg.Button("Crear Insumo"), sg.Button("Modificar Insumo"), sg.Button("Eliminar Insumo"), sg.Button("Salir")]
    ]

    window = sg.Window("Insumos", layout, resizable=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Salir":
            break

        selected_row = values["-TABLE-"]

        if event == "Crear Insumo":
            if create_or_edit_insumo_window():
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Modificar Insumo":
            if not selected_row:
                sg.popup("Por favor, seleccione un insumo de la tabla para modificar.")
                continue
            
            insumo_id = insumo_data[selected_row[0] - 1][0]
            if create_or_edit_insumo_window(insumo_id=insumo_id):
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Eliminar Insumo":
            if not selected_row:
                sg.popup("Por favor, seleccione un insumo de la tabla para eliminar.")
                continue

            insumo_id = insumo_data[selected_row[0] - 1][0]
            insumo_descripcion = insumo_data[selected_row[0] - 1][1]
            
            confirm = sg.popup_yes_no(f"¿Está seguro de que desea eliminar el insumo \"{insumo_descripcion}\"", title="Confirmar Eliminación")
            
            if confirm == "Yes":
                try:
                    eliminar_insumo(insumo_id)
                    sg.popup("Insumo eliminado con éxito.")
                    window["-TABLE-"].update(values=refresh_table())
                except Exception as e:
                    show_error(f"Error al eliminar el insumo: {e}")

    window.close()

def create_or_edit_insumo_window(insumo_id=None):
    """Ventana para crear o editar un insumo. Si se provee insumo_id, es modo edición."""
    
    is_edit = insumo_id is not None
    title = "Modificar Insumo" if is_edit else "Crear Insumo"
    
    initial_data = {"descripcion": "", "tipo": "", "precio_unitario": "", "id_proveedor": ""}
    if is_edit:
        try:
            insumo = obtener_insumo_por_id(insumo_id)
            if insumo:
                initial_data["descripcion"] = insumo.descripcion
                initial_data["tipo"] = insumo.tipo
                initial_data["precio_unitario"] = insumo.precio_unitario
                initial_data["id_proveedor"] = insumo.id_proveedor
            else:
                show_error(f"No se encontró el insumo con ID {insumo_id}")
                return False
        except Exception as e:
            show_error(f"Error al cargar el insumo: {e}")
            return False

    layout = [
        [sg.Text(title, font=("Helvetica", 20))],
        [sg.Text("Descripción:", size=(15,1)), sg.Input(initial_data["descripcion"], key="-DESCRIPCION-")],
        [sg.Text("Tipo:", size=(15,1)), sg.Input(initial_data["tipo"], key="-TIPO-")],
        [sg.Text("Precio Unitario:", size=(15,1)), sg.Input(initial_data["precio_unitario"], key="-PRECIO_UNITARIO-")],
        [sg.Text("ID Proveedor:", size=(15,1)), sg.Input(initial_data["id_proveedor"], key="-ID_PROVEEDOR-")],
        [sg.Button("Guardar"), sg.Button("Cancelar")]
    ]

    window = sg.Window(title, layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancelar":
            window.close()
            return False

        if event == "Guardar":
            descripcion = values["-DESCRIPCION-"]
            tipo = values["-TIPO-"]
            precio_unitario = values["-PRECIO_UNITARIO-"]
            id_proveedor = values["-ID_PROVEEDOR-"]

            if not all([descripcion, tipo, precio_unitario, id_proveedor]):
                sg.popup("Todos los campos son obligatorios.")
                continue
            
            try:
                precio_unitario = float(precio_unitario)
                id_proveedor = int(id_proveedor)

                if is_edit:
                    insumo_actualizado = Insumos(insumo_id, descripcion, tipo, precio_unitario, id_proveedor)
                    modificar_insumo(insumo_actualizado)
                    sg.popup("Insumo modificado con éxito.")
                else:
                    nuevo_insumo = Insumos(None, descripcion, tipo, precio_unitario, id_proveedor)
                    crear_insumo(nuevo_insumo)
                    sg.popup("Insumo creado con éxito.")
                
                window.close()
                return True
            except ValueError:
                sg.popup("Precio Unitario y ID Proveedor deben ser números válidos.")
            except Exception as e:
                show_error(f"Error al guardar el insumo: {e}")

def clientes_window():
    """Ventana principal para la gestión de clientes."""
    
    # Función para refrescar los datos de la tabla
    def refresh_table():
        try:
            return [[c.id, c.nombre, c.direccion, c.telefono, c.correo] for c in obtener_clientes()]
        except Exception as e:
            show_error(f"Error al cargar los clientes: {e}")
            return []

    headings = ["ID", "Nombre", "Dirección", "Teléfono", "Correo"]
    client_data = refresh_table()

    layout = [
        [sg.Text("Gestión de Clientes", font=("Helvetica", 25))],
        [sg.Table(values=client_data, headings=headings, max_col_width=35,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification="right",
                    num_rows=15,
                    key="-TABLE-",
                    row_height=35,
                    tooltip="Lista de Clientes")],
        [sg.Button("Crear Cliente"), sg.Button("Modificar Cliente"), sg.Button("Eliminar Cliente"), sg.Button("Salir")]
    ]

    window = sg.Window("Clientes", layout, resizable=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Salir":
            break

        selected_row = values["-TABLE-"]

        if event == "Crear Cliente":
            if create_or_edit_client_window():
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Modificar Cliente":
            if not selected_row:
                sg.popup("Por favor, seleccione un cliente de la tabla para modificar.")
                continue
            
            client_id = client_data[selected_row[0] - 1][0]
            if create_or_edit_client_window(client_id=client_id):
                window["-TABLE-"].update(values=refresh_table())

        elif event == "Eliminar Cliente":
            if not selected_row:
                sg.popup("Por favor, seleccione un cliente de la tabla para eliminar.")
                continue

            client_id = client_data[selected_row[0] - 1][0]
            client_name = client_data[selected_row[0] - 1][1]
            
            confirm = sg.popup_yes_no(f"¿Está seguro de que desea eliminar al cliente \"{client_name}\"", title="Confirmar Eliminación")
            
            if confirm == "Yes":
                try:
                    eliminar_cliente(client_id)
                    sg.popup("Cliente eliminado con éxito.")
                    window["-TABLE-"].update(values=refresh_table())
                except Exception as e:
                    show_error(f"Error al eliminar el cliente: {e}")

    window.close()

def create_or_edit_client_window(client_id=None):
    """Ventana para crear o editar un cliente. Si se provee client_id, es modo edición."""
    
    is_edit = client_id is not None
    title = "Modificar Cliente" if is_edit else "Crear Cliente"
    
    # Si es modo edición, obtener los datos del cliente
    initial_data = {"nombre": "", "direccion": "", "telefono": "", "correo": ""}
    if is_edit:
        try:
            # Necesitamos una función para obtener un solo cliente por ID
            from clientes.clientes_queries import obtener_cliente_por_id
            cliente = obtener_cliente_por_id(client_id)
            if cliente:
                initial_data["nombre"] = cliente.nombre
                initial_data["direccion"] = cliente.direccion
                initial_data["telefono"] = cliente.telefono
                initial_data["correo"] = cliente.correo
            else:
                show_error(f"No se encontró el cliente con ID {client_id}")
                return False
        except Exception as e:
            show_error(f"Error al cargar el cliente: {e}")
            return False

    layout = [
        [sg.Text(title, font=("Helvetica", 20))],
        [sg.Text("Nombre:", size=(10,1)), sg.Input(initial_data["nombre"], key="-NOMBRE-")],
        [sg.Text("Dirección:", size=(10,1)), sg.Input(initial_data["direccion"], key="-DIRECCION-")],
        [sg.Text("Teléfono:", size=(10,1)), sg.Input(initial_data["telefono"], key="-TELEFONO-")],
        [sg.Text("Correo:", size=(10,1)), sg.Input(initial_data["correo"], key="-CORREO-")],
        [sg.Button("Guardar"), sg.Button("Cancelar")]
    ]

    window = sg.Window(title, layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancelar":
            window.close()
            return False

        if event == "Guardar":
            nombre = values["-NOMBRE-"]
            direccion = values["-DIRECCION-"]
            telefono = values["-TELEFONO-"]
            correo = values["-CORREO-"]

            if not all([nombre, direccion, telefono, correo]):
                sg.popup("Todos los campos son obligatorios.")
                continue
            
            try:
                if is_edit:
                    cliente_actualizado = Cliente(client_id, nombre, direccion, telefono, correo)
                    modificar_cliente(cliente_actualizado)
                    sg.popup("Cliente modificado con éxito.")
                else:
                    nuevo_cliente = Cliente(None, nombre, direccion, telefono, correo)
                    crear_cliente(nuevo_cliente)
                    sg.popup("Cliente creado con éxito.")
                
                window.close()
                return True
            except Exception as e:
                show_error(f"Error al guardar el cliente: {e}")
                # No cerramos la ventana para que el usuario pueda corregir

def main_menu(is_admin: bool):
    """Muestra el menú principal y gestiona la navegación."""
    sg.theme("SandyBeach")

    layout = [
        [sg.Text("Cafés Marloy", justification="center", font=("Helvetica", 25))],
        [sg.Button("Clientes", size=(20, 2))],
        [sg.Button("Insumos", size=(20, 2))],
        [sg.Button("Mantenimientos", size=(20, 2))]
    ]

    if is_admin:
        admin_layout = [
            [sg.Button("Proveedores", size=(20, 2))],
            [sg.Button("Máquinas", size=(20, 2))],
            [sg.Button("Técnicos", size=(20, 2))],
            [sg.Button("Mantenimientos", size=(20, 2))]
        ]
        layout.extend(admin_layout)

    layout.append([sg.Button("Salir", size=(20, 2))])

    window = sg.Window("Menú Principal", layout, element_justification="center")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Salir":
            break
        elif event == "Clientes":
            clientes_window() # <--- LLAMADA A LA NUEVA VENTANA
        elif event == "Insumos":
            insumos_window()
        elif event == "Proveedores" and is_admin:
            proveedores_window()
        elif event == "Máquinas" and is_admin:
            maquinas_window()
        elif event == "Técnicos" and is_admin:
            tecnicos_window()
        elif event == "Mantenimientos":
            mantenimientos_window()

    window.close()

def login_window():
    """Muestra la ventana de login y gestiona la autenticación."""
    sg.theme("SandyBeach")
    layout = [
        [sg.Text("Ingrese su correo y contraseña", justification="center", font=("Helvetica", 25))],
        [sg.Text("Correo", size=(15, 1)), sg.InputText(key="-EMAIL-")],
        [sg.Text("Contraseña", size=(15, 1)), sg.InputText(key="-PASSWORD-", password_char="*")],
        [sg.Submit("Ingresar", button_color=("black", "green")), sg.Cancel("Cancelar"), sg.Button("Crear cuenta", button_color=("black", "green"))]
    ]
    window = sg.Window("Login", layout)

    user_info = None
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancelar":
            break
        elif event == "Crear cuenta":
            create_account_window()
        elif event == "Ingresar":
            email = values["-EMAIL-"]
            password = values["-PASSWORD-"]

            if not email or not password:
                sg.popup("Debe completar todos los campos")
                continue

            try:
                user_info = verify_password(email, password)
                if user_info:
                    sg.popup("Bienvenido")
                    break
                else:
                    sg.popup("Correo o contraseña incorrectos")
            except Exception as e:
                show_error(f"Error de autenticación: {e}")
    
    window.close()
    return user_info

def create_account_window():
    """Muestra la ventana para crear una nueva cuenta."""
    sg.theme("SandyBeach")
    layout = [
        [sg.Text("Ingrese su correo y contraseña", justification="center", font=("Helvetica", 25))],
        [sg.Text("Correo", size=(15, 1)), sg.InputText(key="-EMAIL-", do_not_clear=False)],
        [sg.Text("Contraseña", size=(15, 1)), sg.InputText(key="-PASSWORD-", password_char="*", do_not_clear=False)],
        [sg.Checkbox("Es Administrador", key="-IS_ADMIN-")],
        [sg.Submit("Registrarse", button_color=("black", "green")), sg.Cancel("Cancelar")]
    ]
    window = sg.Window("Crear cuenta", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancelar":
            break
        elif event == "Registrarse":
            email = values["-EMAIL-"]
            password = values["-PASSWORD-"]
            is_admin = values["-IS_ADMIN-"]

            if not email or not password:
                sg.popup("Debe completar todos los campos")
                continue

            try:
                user_id = create_account(email, password, is_admin)
                if user_id is not None:
                    sg.popup("Usuario creado exitosamente")
                    break
                else:
                    sg.popup("El correo ya existe. Por favor, elija otro.")
            except Exception as e:
                show_error(f"Error al crear la cuenta: {e}")
    
    window.close()

if __name__ == "__main__":
    user = login_window()
    if user:
        main_menu(user["es_administrador"])