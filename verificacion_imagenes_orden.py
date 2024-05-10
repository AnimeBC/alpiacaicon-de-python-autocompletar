import os
import pandas as pd
from tkinter import Tk, Label, Button, filedialog
from tkinter.messagebox import showinfo

# Función para seleccionar el archivo Excel
def cargar_excel():
    global ruta_excel
    ruta_excel = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if ruta_excel:
        label_archivo.config(text=f"Archivo cargado: {os.path.basename(ruta_excel)}")
    else:
        label_archivo.config(text="No se ha cargado ningún archivo.")

# Función para procesar las imágenes
def procesar_imagenes():
    if not ruta_excel:
        showinfo("Error", "Por favor, carga un archivo Excel primero.")
        return

    datos = pd.read_excel(ruta_excel)
    duplicados = {}

    # Se añade un contador para seguir la posición de cada fila
    posicion = 1

    for _, fila in datos.iterrows():
        numero_celular = fila['NUMERO']  # Ajustado para coincidir con el nombre de la columna en Excel

        if pd.isna(numero_celular):
            print(f"Campo vacío encontrado en la posición {posicion}")
            posicion += 1
            continue

        nuevo_nombre_base = f"{posicion}_{numero_celular}"
        if nuevo_nombre_base in duplicados:
            duplicados[nuevo_nombre_base] += 1
            nuevo_nombre = f"{nuevo_nombre_base}_duplicado{duplicados[nuevo_nombre_base]}"
        else:
            duplicados[nuevo_nombre_base] = 0
            nuevo_nombre = nuevo_nombre_base

        encontrado = False
        for archivo in os.listdir(ruta_imagenes):
            if str(numero_celular) in archivo:
                viejo_path = os.path.join(ruta_imagenes, archivo)
                extension = os.path.splitext(archivo)[1]
                nuevo_path = os.path.join(ruta_imagenes, nuevo_nombre + extension)
                os.rename(viejo_path, nuevo_path)
                encontrado = True
                break
        if not encontrado:
            print(f"No se encontró una imagen para el número {numero_celular}")

        posicion += 1

    showinfo("Completado", "Proceso de renombramiento completado.")

# Configuración de la interfaz gráfica
root = Tk()
root.title("Rearrange Images")

ruta_excel = None
ruta_imagenes = r"C:\Users\PC_\Documents\tienda pastrana\automatizacion\capturas"

label_archivo = Label(root, text="No se ha cargado ningún archivo.")
label_archivo.pack(pady=20)

btn_cargar_excel = Button(root, text="Cargar Excel", command=cargar_excel)
btn_cargar_excel.pack(pady=5)

btn_procesar = Button(root, text="Procesar Imágenes", command=procesar_imagenes)
btn_procesar.pack(pady=20)

root.mainloop()
