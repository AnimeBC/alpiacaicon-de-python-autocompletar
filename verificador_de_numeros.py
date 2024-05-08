import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import pyautogui

# Variable de control para evitar duplicación de automatización
is_automating = False

def load_file():
    global is_automating
    if is_automating:
        return
    is_automating = True

    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        df = pd.read_excel(file_path)
        global phone_numbers
        phone_numbers = df['NUMERO'].tolist()
        validate_and_set_index()

    is_automating = False

def validate_and_set_index():
    global is_automating
    if is_automating:
        return
    is_automating = True

    global current_index
    index_text = start_index_entry.get().strip()
    if index_text.isdigit():
        index = int(index_text)
        if 0 <= index < len(phone_numbers):
            current_index = index
            update_index_label()
        else:
            messagebox.showerror("Error", "Índice fuera de rango.")
            current_index = 0  # Reset to default if out of range
    elif index_text:
        messagebox.showerror("Error", "Por favor, ingrese solo números.")
        current_index = 0
    else:
        current_index = 0
    update_index_label()

    is_automating = False
def start_automation():
    validate_and_set_index()
    if phone_numbers and current_index < len(phone_numbers):
        automate_form(str(phone_numbers[current_index]))
    else:
        messagebox.showerror("Error", "Índice fuera de rango o lista de números vacía.")

def next_number():
    global current_index
    if current_index + 1 < len(phone_numbers):
        current_index += 1
        automate_form(str(phone_numbers[current_index]))
        update_index_label()

def previous_number():
    global current_index
    if current_index > 0:
        current_index -= 1
        automate_form(str(phone_numbers[current_index]))
        update_index_label()

def update_index_label():
    if 0 <= current_index < len(phone_numbers):
        current_index_label.config(text=phone_numbers[current_index])
    else:
        current_index_label.config(text="N/A")

def automate_form(phone_number, pin="2468"):
    pyautogui.sleep(2)
    coordinates = {
        'service_type': (1100, 410),
        'phone_number': (1150, 450),
        'pin': (1150, 540),
        'submit': (1100, 570)
    }
    pyautogui.click(*coordinates['service_type'])
    pyautogui.sleep(1)
    pyautogui.press('up', presses=10)
    pyautogui.press('down', presses=5)
    pyautogui.press('enter')

    pyautogui.click(*coordinates['phone_number'])
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(['backspace'] * 10)
    pyautogui.write(phone_number)
    pyautogui.sleep(1)

    pyautogui.click(*coordinates['pin'])
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(['backspace'] * 10)
    pyautogui.write(pin)
    pyautogui.sleep(1)

    pyautogui.click(*coordinates['submit'])
    pyautogui.sleep(2)

def click_at_specific_location():
    specific_coordinates = (1040, 493)
    pyautogui.click(*specific_coordinates)
    pyautogui.sleep(1)

def execute_step_3():
    another_coordinates = (1080, 445)
    pyautogui.click(*another_coordinates)
    pyautogui.sleep(1)

app = tk.Tk()
app.title("Formulario de Automatización")
app.geometry("450x200")  # Ajusta el tamaño aquí según sea necesario
app.resizable(width=False, height=False)  # Deshabilita el redimensionamiento
app.configure(bg='#1e1e2d')

# Posicionar la ventana en el centro izquierdo de la pantalla
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calcula la posición para centrar verticalmente
vertical_position = (screen_height // 2) - 200  # 100 es la mitad de la altura de la ventana

app.geometry(f'450x200+0+{vertical_position}')  # '0+' es para el lado izquierdo de la pantalla
app.attributes('-topmost', True)  # Hacer que la ventana siempre esté en la parte superior


style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Helvetica', 10), padding=3, borderwidth=2, relief='solid', foreground='black')
style.configure('TLabel', font=('Helvetica', 10), background='#1e1e2d', foreground='#ffffff')
style.configure('TEntry', font=('Helvetica', 10), foreground='black', background='#333333')

file_entry = ttk.Entry(app, font=('Helvetica', 10), width=15)
file_entry.grid(row=0, column=0, padx=5, pady=20)
browse_button = ttk.Button(app, text="Buscar archivo", command=load_file)
browse_button.grid(row=0, column=1, padx=5)

start_index_entry = ttk.Entry(app, font=('Helvetica', 10), width=8)
start_index_entry.grid(row=1, column=0, padx=5)
start_button = ttk.Button(app, text="Iniciar Automatización", command=start_automation)
start_button.grid(row=1, column=1, padx=5)

previous_button = ttk.Button(app, text="Número Anterior", command=previous_number)
previous_button.grid(row=2, column=0, sticky='w', padx=(50,0), pady=10)
current_index_label = ttk.Label(app, text="N/A", width=10)
current_index_label.grid(row=2, column=1, padx=5)
next_button = ttk.Button(app, text="Siguiente Número", command=next_number)
next_button.grid(row=2, column=2, sticky='e', padx=(0,50))

step_2_button = ttk.Button(app, text="Ejecutar Paso 2", command=click_at_specific_location)
step_2_button.grid(row=3, column=0, sticky='w', padx=(50,0), pady=10)
step_3_button = ttk.Button(app, text="Ejecutar Paso 3", command=execute_step_3)
step_3_button.grid(row=3, column=2, sticky='e', padx=(0,50))
app.mainloop()