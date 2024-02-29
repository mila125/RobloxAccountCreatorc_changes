from PIL import Image
import os

# Función para ocultar un archivo dentro de una imagen
def ocultar_archivo(archivo_imagen, archivo_ocultar, archivo_salida):
    # Abre la imagen
    imagen = Image.open(archivo_imagen)
    # Abre el archivo a ocultar
    with open(archivo_ocultar, "rb") as f:
        archivo_ocultar_data = f.read()
    # Oculta el archivo dentro de los bytes de la imagen
    imagen_con_datos = imagen.copy()
    imagen_con_datos.info["ArchivoOculto"] = archivo_ocultar
    imagen_con_datos.info["ArchivoOcultoSize"] = len(archivo_ocultar_data)
    imagen_con_datos = imagen_con_datos.tobytes() + archivo_ocultar_data
    # Guarda la imagen resultante
    with open(archivo_salida, "wb") as f:
        f.write(imagen_con_datos)

# Función para extraer un archivo oculto de una imagen
def extraer_archivo(archivo_oculto, archivo_salida):
    # Abre la imagen
    imagen_con_datos = Image.open(archivo_oculto)
    # Extrae los metadatos
    archivo_ocultar = imagen_con_datos.info.get("ArchivoOculto")
    archivo_ocultar_size = imagen_con_datos.info.get("ArchivoOcultoSize")
    # Extrae los datos del archivo oculto
    datos_ocultos = imagen_con_datos.tobytes()[len(imagen_con_datos.info):]
    # Escribe los datos del archivo oculto a un nuevo archivo
    with open(archivo_salida, "wb") as f:
        f.write(datos_ocultos)

# Ejemplo de uso
archivo_imagen = "imagen.png"
archivo_ocultar = "programa.exe"
archivo_salida_ocultar = "imagen_con_programa.png"
archivo_salida_extraer = "programa_extraido.exe"

# Ocultar el archivo .exe dentro de la imagen
#ocultar_archivo(archivo_imagen, archivo_ocultar, archivo_salida_ocultar)

# Extraer el archivo oculto de la imagen
extraer_archivo(archivo_salida_ocultar, archivo_salida_extraer)

# Verificar si los archivos son idénticos
print("Los archivos son idénticos:", filecmp.cmp(archivo_ocultar, archivo_salida_extraer))
