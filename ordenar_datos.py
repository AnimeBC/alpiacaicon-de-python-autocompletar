import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from openpyxl.utils import get_column_letter

def open_file(entry):
    file_path = filedialog.askopenfilename(
        filetypes=(("Excel files", "*.xlsx;*.xls"), ("All files", "*.*"))
    )
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def adjust_column_width(writer, df):
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        max_len = max((
            series.astype(str).map(len).max(),  # length of largest item
            len(str(series.name))  # length of column name/header
        )) + 1  # adding a little extra space
        worksheet.column_dimensions[get_column_letter(idx+1)].width = max_len

def extract_data():
    file_path = entry1.get()
    if not file_path:
        print("No se ha seleccionado un archivo.")
        return

    try:
        # Leer el archivo Excel
        df = pd.read_excel(file_path)

        # Normalizar los nombres de las columnas
        df.columns = df.columns.str.strip().str.upper()

        # Filtrar los tipos de venta
        tipos_de_venta_validos = ['ALTA POST', 'FTHH INTERNET', 'LINEA ADICIONAL', 'MIGRACION', 'PORTA POST', 'RENOVACION POST', 'REPOSICION']
        df = df[df['TIPO DE VENTA'].isin(tipos_de_venta_validos)]

        # Convertir 'FECHA DE ACTIVACION' a datetime y formatear
        df['FECHA DE ACTIVACION'] = pd.to_datetime(df['FECHA DE ACTIVACION']).dt.strftime('%d/%m/%Y')

        # Añadiendo espacios en blanco como columnas vacías
        for i in range(1, 35):  # Para agregar espacios desde BLANK1 hasta BLANK34
            df[f'BLANK{i}'] = ''

        # Definir el orden deseado de las columnas incluyendo espacios en blanco
        columnas_requeridas = [
            'FECHA DE ACTIVACION', 'NOM Y APELLIDOS', 'DNI', 'NUMERO', 'PLAN', 'TIPO DE VENTA', 'OPERADOR', 
            'BLANK1', 'BLANK2', '50% DSCTO', 'NUMERO DE REFERENCIA', 'BLANK3', 'BLANK4', 'AUTOLIQUIDABLE SISTEMA', 'VENDEDOR'
        ] + [f'BLANK{i}' for i in range(5, 35)]
        # Verificar que todas las columnas necesarias estén en el DataFrame
        if not all(col in df.columns for col in columnas_requeridas):
            missing = [col for col in columnas_requeridas if col not in df.columns]
            print(f"Faltan las siguientes columnas en el archivo: {missing}")
            return

        # Seleccionar y reordenar las columnas
        df_final = df[columnas_requeridas]

        # Guardar el nuevo DataFrame en un archivo Excel
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if save_path:
            with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False)
                adjust_column_width(writer, df_final)
            print("Datos guardados en:", save_path)
    except Exception as e:
        print("Error al procesar el archivo:", e)

# Configuración inicial de la ventana
root = tk.Tk()
root.title("Aplicación Neón")
root.geometry("600x400")
root.configure(bg='#1e1e2d')

# Estilo personalizado para los widgets usando ttk
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Helvetica', 12, 'bold'), borderwidth='1', relief='solid')
style.map('TButton', background=[('active', '#333333')], foreground=[('active', '#ffffff')])
style.configure('TLabel', font=('Helvetica', 14, 'bold'), background='#1e1e2d', foreground='#d5d5d5')
style.configure('TEntry', font=('Helvetica', 12), borderwidth='1', relief='solid', foreground='#d5d5d5', background='#333333')

# Configurar columnas y filas para control de expansión
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=0)

root.resizable(False, False)

# Crear un Frame central
center_frame = tk.Frame(root, bg='#1e1e2d', relief='raised')
center_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
label = ttk.Label(center_frame, text="Aplicación para el primer paso", style='TLabel')
label.pack(pady=20, expand=True)

# Widget setup con ajustes de padding
label1 = ttk.Label(root, text="Archivo 1", style='TLabel')
label1.grid(row=1, column=0, padx=20, pady=10, sticky='w')
entry1 = ttk.Entry(root, width=40, style='TEntry')
entry1.grid(row=2, column=0, padx=20, pady=5, sticky='ew')
button1 = ttk.Button(root, text="Abrir Archivo 1", command=lambda: open_file(entry1))
button1.grid(row=3, column=0, padx=20, pady=10, sticky='ew')

# Botón para extraer datos
extract_data_button = ttk.Button(root, text="Sacar datos", command=extract_data)
extract_data_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky='ew')

root.mainloop()
