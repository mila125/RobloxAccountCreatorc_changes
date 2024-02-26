import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Función para cambiar la descripción del perfil
def cambiar_descripcion(driver, nueva_descripcion):
    try:
        # Navega a la página de perfil
        driver.get("https://www.roblox.com/users/profile")

        # Espera un momento para que se cargue la página
        time.sleep(3)

        # Busca el elemento del cuadro de texto de la descripción del perfil
        descripcion_input = driver.find_element_by_id("descriptionTextBox")

        # Limpia el cuadro de texto
        descripcion_input.clear()

        # Ingresa la nueva descripción
        descripcion_input.send_keys(nueva_descripcion)

        # Guarda los cambios presionando Enter (puedes usar el botón de guardar si está disponible)
        descripcion_input.send_keys(Keys.RETURN)

        print("Descripción del perfil actualizada exitosamente.")
    except Exception as e:
        print("Error al cambiar la descripción del perfil:", e)

# Ejemplo de uso
driver = webdriver.Edge()  # Cambiar al navegador de tu elección
driver.get("https://www.roblox.com/home")  # Inicia sesión en Roblox manualmente

# Espera un momento para que se inicie sesión manualmente
time.sleep(40)  # Puedes ajustar este tiempo según sea necesario

# Llama a la función para cambiar la descripción del perfil
nueva_descripcion = "¡Hola! Soy nuevo aquí."
cambiar_descripcion(driver, nueva_descripcion)

# Cierra el navegador
driver.quit()
