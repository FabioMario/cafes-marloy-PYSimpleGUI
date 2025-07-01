import PySimpleGUI as sg
import mysql.connector
from auth import hash_password, verify_password
from config import DB_CONFIG

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        sg.popup_error(f"Error al conectar a la base de datos: {err}")
        return None

def login():
    sg.theme('SandyBeach')
    layout = [
        [sg.Text('Ingrese su correo y contraseña', justification='center', font=("Helvetica", 25))],
        [sg.Text('Correo', size=(15, 1)), sg.InputText(key='-EMAIL-')],
        [sg.Text('Contraseña', size=(15, 1)), sg.InputText(key='-PASSWORD-', password_char='*')],
        [sg.Submit('Ingresar', button_color=('black', 'green')), sg.Cancel('Cancelar'), sg.Button('Crear cuenta', button_color=('black', 'green'))]
    ]
    window = sg.Window('Login', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        elif event == 'Crear cuenta':
            create_account()
        elif event == 'Ingresar':
            email = values['-EMAIL-']
            password = values['-PASSWORD-']

            if not email or not password:
                sg.popup('Debe completar todos los campos')
                continue

            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT contraseña FROM login WHERE correo = %s", (email,))
                    result = cursor.fetchone()

                    if result:
                        hashed_password_from_db = result[0]
                        if verify_password(password, hashed_password_from_db):
                            sg.popup('Bienvenido')
                            # Aquí podrías añadir lógica para iniciar la sesión del usuario
                            break
                        else:
                            sg.popup('Correo o contraseña incorrectos')
                    else:
                        sg.popup('Correo o contraseña incorrectos')
                except mysql.connector.Error as err:
                    sg.popup_error(f"Error al consultar la base de datos: {err}")
                finally:
                    conn.close()
    window.close()

def create_account():
    sg.theme('SandyBeach')
    layout = [
        [sg.Text('Ingrese su correo y contraseña', justification='center', font=("Helvetica", 25))],
        [sg.Text('Correo', size=(15, 1)), sg.InputText(key='-EMAIL-', do_not_clear=False)],
        [sg.Text('Contraseña', size=(15, 1)), sg.InputText(key='-PASSWORD-', password_char='*', do_not_clear=False)],
        [sg.Checkbox('Es Administrador', key='-IS_ADMIN-')],
        [sg.Submit('Registrarse', button_color=('black', 'green')), sg.Cancel('Cancelar')]
    ]
    window = sg.Window('Crear cuenta', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        elif event == 'Registrarse':
            email = values['-EMAIL-']
            password = values['-PASSWORD-']
            is_admin = values['-IS_ADMIN-']

            if not email or not password:
                sg.popup('Debe completar todos los campos')
                continue

            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    salty_hash = hash_password(password)
                    # Asegúrate de que el campo 'contraseña' en tu tabla 'login' sea de tipo BLOB o VARBINARY
                    # para almacenar el hash binario.
                    cursor.execute("INSERT INTO login (correo, contraseña, es_administrador) VALUES (%s, %s, %s)", (email, salty_hash, is_admin))
                    conn.commit()
                    sg.popup('Usuario creado exitosamente')
                    break
                except mysql.connector.IntegrityError:
                    sg.popup('El correo ya existe. Por favor, elija otro.')
                except mysql.connector.Error as err:
                    sg.popup_error(f"Error al crear el usuario: {err}")
                finally:
                    conn.close()
    window.close()

if __name__ == '__main__':
    login()
