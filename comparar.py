import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
# Configuración inicial de la ventana
root = tk.Tk()
root.title("Aplicación Neón")
root.geometry("600x400")  # Ancho x Alto
root.configure(bg='#1e1e2d')  # Color de fondo oscuro
# Centrar la ventana en la pantalla
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
# Estilo personalizado para los widgets usando ttk
style = ttk.Style()
style.theme_use('clam')
# Configurando los colores y estilos de fuente
style.configure('TButton', font=('Helvetica', 12, 'bold'), borderwidth='1', relief='solid')
style.map('TButton', background=[('active', '#333333')], foreground=[('active', '#ffffff')])
style.configure('TLabel', font=('Helvetica', 14, 'bold'), background='#1e1e2d', foreground='#d5d5d5')
style.configure('TEntry', font=('Helvetica', 12), borderwidth='1', relief='solid', foreground='#d5d5d5', background='#333333')

# Configurar columnas y filas para que se expandan adecuadamente
root.grid_columnconfigure(0, weight=1)  # Permite que la columna se expanda
root.grid_columnconfigure(1, weight=1)  # Permite que la columna se expanda

# Solo las filas que necesitan expandirse deben tener weight
root.grid_rowconfigure(0, weight=0)  # Permite que la fila se expanda donde está el centro_frame
# Las filas con labels, entries y botones no necesitan expandirse, weight=0 (o no establecerlo)
root.grid_rowconfigure(1, weight=0)  # No se expande
root.grid_rowconfigure(2, weight=0)  # No se expande
root.grid_rowconfigure(3, weight=0)  # No se expande
# Impedir redimensionar la ventana
root.resizable(False, False)
# Crear un Frame que actuará como contenedor para el label central usando tk.Frame
center_frame = tk.Frame(root, bg='#1e1e2d', relief='raised')
center_frame.grid(row=0, column=0, columnspan=2,sticky='nsew')
# Crear un label y centrarlo usando pack dentro del frame
label = ttk.Label(center_frame, text="Aplicación para el primer paso", style='TLabel')
label.pack(pady=20, expand=True)

# Widget setup con ajustes de padding
label1 = ttk.Label(root, text="Archivo 1", style='TLabel')
label1.grid(row=1, column=0, padx=20, pady=10, sticky='w')
entry1 = ttk.Entry(root, width=40, style='TEntry')
entry1.grid(row=2, column=0, padx=20, pady=5, sticky='ew')
button1 = ttk.Button(root, text="Abrir Archivo 1", command=lambda: open_file(entry1))
button1.grid(row=3, column=0, padx=20, pady=10, sticky='ew')

label2 = ttk.Label(root, text="Archivo 2", style='TLabel')
label2.grid(row=1, column=1, padx=20, pady=10, sticky='w')
entry2 = ttk.Entry(root, width=40, style='TEntry')
entry2.grid(row=2, column=1, padx=20, pady=5, sticky='ew')
button2 = ttk.Button(root, text="Abrir Archivo 2", command=lambda: open_file(entry2))
button2.grid(row=3, column=1, padx=20, pady=10, sticky='ew')

# Función para abrir el diálogo de selección de archivos y actualizar la entrada
def open_file(entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
# Ejecución de la ventana
root.mainloop()
