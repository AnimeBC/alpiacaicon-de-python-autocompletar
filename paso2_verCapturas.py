import cv2
import pytesseract
import re
import pandas as pd
from tkinter import Tk, Button, filedialog, messagebox
from tkinter.ttk import Progressbar
import os

# Configuración de pytesseract (puede que necesites cambiar la ruta según tu instalación)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Función para extraer el precio y las fechas del texto extraído
def extraer_info(texto):
    # Encuentra el precio después de la palabra clave
    precio_match = re.search(r'Periodo Pendiente de Balance : (\d+\.\d+)', texto)
    precio = precio_match.group(1) if precio_match else "Precio no encontrado"

    # Encuentra las fechas después de la palabra clave "/24 |"
    fechas = re.findall(r'/24 \| (\d{2}/\d{2}/\d{2})', texto)
    fechas = "\n".join(fechas) if fechas else "Fechas no encontradas"

    return precio, fechas

# Función para procesar una imagen
def procesar_imagen(filename, writer):
    # Lee la imagen
    imagen = cv2.imread(filename)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Usa pytesseract para extraer el texto de la imagen
    texto = pytesseract.image_to_string(gris)

    # Extrae el precio y las fechas del texto extraído
    precio, fechas = extraer_info(texto)

    # Guarda los datos en un DataFrame de pandas
    data = {'Archivo': [filename], 'Precio': [precio], 'Fechas': [fechas]}
    df = pd.DataFrame(data)

    # Escribe el DataFrame en el archivo Excel
    sheet_name = os.path.basename(filename)  # Usa el nombre del archivo como nombre de hoja
    df.to_excel(writer, sheet_name=sheet_name, index=False)

# Función para leer y procesar todas las imágenes seleccionadas
def leer_imagenes():
    # Abre un diálogo para seleccionar las imágenes
    filenames = filedialog.askopenfilenames()

    # Abre el archivo Excel fuera del bucle
    with pd.ExcelWriter('resultados.xlsx', mode='a', engine='openpyxl') as writer:
        # Procesa cada imagen
        for filename in filenames:
            procesar_imagen(filename, writer)

    # Muestra un mensaje indicando que se han procesado todas las imágenes
    messagebox.showinfo("Proceso completado", "Se han procesado todas las imágenes.")

# Configuración de la interfaz gráfica
root = Tk()
root.title("Lector de Precio y Fechas de Imágenes")

# Botón para cargar las imágenes y leer la información
btn_cargar = Button(root, text="Cargar Imágenes", command=leer_imagenes)
btn_cargar.pack()

# Barra de progreso para mostrar el progreso de la lectura de imágenes
progressbar = Progressbar(root, orient='horizontal', mode='determinate', length=200)
progressbar.pack()

# Ejecuta el bucle principal de la interfaz gráfica
root.mainloop()
