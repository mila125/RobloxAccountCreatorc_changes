import secrets
import string
import time
import os
import sys
import random
import threading
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests

log_file = "log.txt"

def estado(texto):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + texto + "\033[0m")
    with open(log_file, 'a') as log:
        log.write(texto + "\n")

# Configuración
Cuentas = 1  # cuántas cuentas
MaxVentanas = 3
VentanasActuales = 0
driver = webdriver.Edge()  # O el navegador de tu elección
# URLs
url_nombres = "https://raw.githubusercontent.com/H20CalibreYT/RobloxAccountCreator/main/firstnames.txt"
url_apellidos = "https://raw.githubusercontent.com/H20CalibreYT/RobloxAccountCreator/main/lastnames.txt"
url_roblox = "https://www.roblox.com/"

estado("Obteniendo nombres...")
respuesta_nombres = requests.get(url_nombres)
estado("Obteniendo apellidos...")
respuesta_apellidos = requests.get(url_apellidos)

# Comprobar si la carga de nombres fue exitosa
if respuesta_nombres.status_code == 200 and respuesta_apellidos.status_code == 200:
    nombres = list(set(respuesta_nombres.text.splitlines()))
    apellidos = list(set(respuesta_apellidos.text.splitlines()))
else:
    estado("Error al cargar los nombres. Vuelve a ejecutar el script.")
    sys.exit()

# Rutas de archivos
ruta_archivos = os.path.dirname(os.path.abspath(sys.argv[0]))
carpeta_archivos_texto = os.path.join(ruta_archivos, "Cuentas")
archivo_texto = os.path.join(carpeta_archivos_texto, f"Cuentas_{date.today()}.txt")
archivo_texto2 = os.path.join(carpeta_archivos_texto, f"AltManagerLogin_{date.today()}.txt")

# Crear carpeta si no existe
if not os.path.exists(carpeta_archivos_texto):
    os.makedirs(carpeta_archivos_texto)

# Listas de días, meses y años
dias = [str(i + 1) for i in range(10, 28)]
meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
anios = [str(i + 1) for i in range(1980, 2004)]

# Generador de contraseñas
def generar_contraseña(longitud):
    estado("Generando contraseña...")
    caracteres = string.ascii_letters + string.digits + "Ññ¿?¡!#$%&/()=\/¬|°_-[]*~+"
    contraseña = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contraseña

# Generador de nombres de usuario
def generar_usuario(nombres, apellidos):
    estado("Generando nombre de usuario...")
    nombre = secrets.choice(nombres)
    apellido = secrets.choice(apellidos)
    usuario = f"{nombre}{apellido}_{secrets.choice([i for i in range(1, 999)]):03}"
    return usuario

# Función para crear una cuenta
def crear_cuenta(url, nombres, apellidos):
    global driver
    global VentanasActuales
    try:
        estado("Comenzando a crear una cuenta...")
        cookie_encontrada = False
        usuario_encontrado = False
        tiempo_transcurrido = 0

        estado("Inicializando el controlador web...")
        
        driver.set_window_size(1200, 800)
        driver.set_window_position(0, 0)
        driver.get(url)
        time.sleep(2)

        # Elementos HTML
        estado("Buscando elementos en el sitio web...")
        input_usuario = driver.find_element("id", "signup-username")
        error_usuario = driver.find_element("id", "signup-usernameInputValidation")
        input_contraseña = driver.find_element("id", "signup-password")
        dropdown_dia = driver.find_element("id", "DayDropdown")
        dropdown_mes = driver.find_element("id", "MonthDropdown")
        dropdown_año = driver.find_element("id", "YearDropdown")
        boton_masculino = driver.find_element("id", "MaleButton")
        boton_femenino = driver.find_element("id", "FemaleButton")
        boton_registro = driver.find_element("id", "signup-button")

        estado("Seleccionando día...")
        Seleccion = Select(dropdown_dia)
        Seleccion.select_by_value(secrets.choice(dias))
        time.sleep(0.3)

        estado("Seleccionando mes...")
        Seleccion = Select(dropdown_mes)
        Seleccion.select_by_value(secrets.choice(meses))
        time.sleep(0.3)

        estado("Seleccionando año...")
        Seleccion = Select(dropdown_año)
        Seleccion.select_by_value(secrets.choice(anios))
        time.sleep(0.3)

        while not usuario_encontrado:
            estado("Seleccionando nombre de usuario...")
            usuario = generar_usuario(nombres, apellidos)
            input_usuario.clear()
            input_usuario.send_keys(usuario)
            time.sleep(1)
            if error_usuario.text.strip() == "":
                usuario_encontrado = True
        
        estado("Seleccionando contraseña...")
        contraseña = generar_contraseña(25)
        input_contraseña.send_keys(contraseña)
        time.sleep(0.3)

        estado("Registrando cuenta...")
        boton_registro.click()
        time.sleep(3)

        # Esperar hasta que se encuentre la cookie o pase el tiempo máximo
        while not cookie_encontrada and tiempo_transcurrido < 180:
            estado("Esperando la cookie...")
            time.sleep(3)
            tiempo_transcurrido += 3
            for cookie in driver.get_cookies():
                if cookie.get('name') == '.ROBLOSECURITY':
                    cookie_encontrada = True
                    break
        if cookie_encontrada:
            estado("Cookie encontrada...")
            resultado = [cookie.get('value'), usuario, contraseña]
            guardar_info_cuenta(resultado)
            guardar_login_altmanager(resultado)
            if resultado is not None:
                estado("Hay algo : {resultado}")
                time.sleep(3)
                VentanasActuales -= 1
                estado(f"Ventanas abiertas: {VentanasActuales}")
                # Después de cerrar el navegador, establecemos la descripción del perfil
                #estado("Setting profile description...")
                
                driver.get("https://www.roblox.com/users/profile")  # Asegúrate de que el navegador esté en la página correcta
                time.sleep(2)
                set_profile_description(driver, gen_profile_description())
            driver.quit()

            #estado("Successfully profile description set!")
            time.sleep(10)

    except Exception as e:
        estado(f"Error: {e}")
        VentanasActuales -= 1

# Guardar información de la cuenta en archivo de texto
def guardar_info_cuenta(info_cuenta):
    estado("Guardando información de la cuenta...")
    with open(archivo_texto, 'a') as file:
        file.write(f"Usuario: {info_cuenta[1]}\nContraseña: {info_cuenta[2]}\nCookie: {info_cuenta[0]}\n\n\n")

# Guardar información de inicio de sesión para AltManager
def guardar_login_altmanager(info_cuenta):
    global driver
    with open(archivo_texto2, 'a') as file:
        estado("Guardando inicio de sesión de la cuenta (para alt manager)...")
        file.write(f"{info_cuenta[1]}:{info_cuenta[2]}\n")
    estado("Logged in")
    driver.get(url_roblox)
    driver.add_cookie({'name': '.ROBLOSECURITY', 'value': info_cuenta[0], 'domain': '.roblox.com'})
    driver.refresh()
    time.sleep(2)
 
# Crear cuentas
def crear_cuentas():
    
    global VentanasActuales
    try:
        for _ in range(Cuentas):
            while VentanasActuales >= MaxVentanas:
                estado(f"Esperando... {VentanasActuales}/{MaxVentanas}")
                time.sleep(1)

            cuenta_thread = threading.Thread(target=crear_cuenta, args=(url_roblox, nombres, apellidos))
            cuenta_thread.start()
            VentanasActuales += 1
            time.sleep(1)
    except Exception as e:
        estado(f"Error: {e}")
        VentanasActuales -= 1
# Función para establecer la descripción del perfil
def set_profile_description(driver, description):
    try:
        estado("Setting profile description...")
        time.sleep(5)  # Wait for 5 seconds to ensure the page has loaded
        # You can print the page source for debugging
        # print(driver.page_source)
        
        # Check if the description input element exists
        description_input = driver.find_element("id", "descriptionTextBox")
        boton_sd = driver.find_element("id", "SaveInfoSettings")
        # Clear the input field and send keys
        description_input.clear()
        description_input.send_keys(description)
        time.sleep(2)
        
        boton_sd.click()

        time.sleep(2)
        # You can add more debugging statements or print statements here
        
        estado("Profile description set successfully!")
    except Exception as e:
        estado("Failed to set profile description: " + str(e))
# Función para generar una descripción aleatoria de perfil
def gen_profile_description():
    return random.choice(profile_descriptions)
profile_descriptions = [
    "New mods here !",
    "Do yo wanna earn money in Roblox free mods here !",
    "Fanático de Roblox desde hace años.",
    "Streamer ocasional. ¡Sígueme!",
    "Me encanta construir en Roblox Studio.",
    "Explorando el metaverso de Roblox.",
    "Siempre buscando nuevos amigos para jugar.",
    "¡Un saludo a toda la comunidad de Roblox!",
    "¡Listo para explorar y construir!",
    "¿Quieres jugar juntos? ¡Envíame un mensaje!",
]

# Ejecutar la función principal
crear_cuentas()
            
