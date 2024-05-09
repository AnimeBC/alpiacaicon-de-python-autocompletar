import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Renombrar Imágenes Según Excel")
        self.geometry("400x200")  # Aumenté ligeramente la altura para mejor presentación

        # Variables
        self.excel_file = tk.StringVar()
        self.folder_path = r'C:\Users\PC_\Documents\tienda pastrana\automatizacion\capturas'

        # Widgets
        ttk.Label(self, text="Archivo Excel:").pack(pady=10)
        self.excel_entry = ttk.Entry(self, textvariable=self.excel_file, width=50)
        self.excel_entry.pack(pady=10)
        ttk.Button(self, text="Buscar Excel", command=self.load_excel).pack(pady=10)
        ttk.Button(self, text="Renombrar Imágenes", command=self.rename_images).pack(pady=10)

    def load_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            self.excel_file.set(file_path)

    def rename_images(self):
        if not self.excel_file.get():
            messagebox.showerror("Error", "Por favor, selecciona un archivo Excel primero.")
            return

        # Leer el archivo Excel
        try:
            df = pd.read_excel(self.excel_file.get())
            if 'NUMERO' not in df.columns:
                messagebox.showerror("Error", "No se encontró la columna 'NUMERO' en el archivo Excel.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo Excel: {e}")
            return

        numeros = df['NUMERO'].astype(str).tolist()  # Convertir todo a string para evitar discrepancias de tipo
        mapa_archivos = self.get_file_map()
        cambios = 0

        # Renombrar archivos
        for indice, numero in enumerate(numeros, start=1):
            if numero in mapa_archivos:
                viejo_nombre = mapa_archivos[numero]
                nuevo_nombre = f"{indice}_{numero}.png"
                viejo_path = os.path.join(self.folder_path, viejo_nombre)
                nuevo_path = os.path.join(self.folder_path, nuevo_nombre)
                try:
                    os.rename(viejo_path, nuevo_path)
                    cambios += 1
                except FileNotFoundError:
                    messagebox.showerror("Error", f"No se encontró el archivo: {viejo_nombre}")

        messagebox.showinfo("Completado", f"Se renombraron {cambios} archivos correctamente.")

    def get_file_map(self):
        mapa_archivos = {}
        for archivo in os.listdir(self.folder_path):
            if archivo.endswith(".png"):
                partes = archivo.split('_')
                if len(partes) > 1 and partes[1].split('.')[0].isdigit():
                    numero_tel = partes[1].split('.')[0]
                    mapa_archivos[numero_tel] = archivo
        return mapa_archivos

if __name__ == "__main__":
    app = App()
    app.mainloop()
