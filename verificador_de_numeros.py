import pyautogui
import pytesseract
import tkinter as tk
from PIL import Image
# Actualización de la ruta de Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\PC_\Documents\tienda pastrana\automatizacion\tesseract\tesseract.exe'

def automate_form(phone_number, pin="2468"):
    pyautogui.sleep(5)  # Esperar a que la página cargue completamente
    # Coordenadas personalizadas para cada elemento del formulario
    x_service_type = 1100  # X para el desplegable de tipo de servicio
    y_service_type = 410  # Y para el desplegable de tipo de servicio
    
    x_phone_number = 1150  # X para el campo de número de teléfono
    y_phone_number = 450  # Y para el campo de número de teléfono
    
    x_pin = 1150  # X para el campo de PIN
    y_pin = 540  # Y para el campo de PIN
    
    x_submit = 1100  # X para el botón enviar
    y_submit = 570  # Y para el botón enviar

   # Interactuar con el dropdown de tipo de servicio
    pyautogui.click(x_service_type, y_service_type)
    pyautogui.sleep(2)  # Pausa adicional para asegurar que el menú está activo
    # Primero subir todas las opciones para asegurar que se parte desde el principio
    for _ in range(10):  # Asumiendo que no hay más de 10 opciones en total
        pyautogui.press('up')
    pyautogui.sleep(0.5)
    # Ajustar el número de presses según la ubicación real de "Consulta Recaudación"
    pyautogui.press('down', presses=5)  
    pyautogui.sleep(0.5)  # Pausa corta antes de confirmar la selección
    pyautogui.press('enter')
    
    # Interactuar con el campo de número de teléfono
    pyautogui.click(x_phone_number, y_phone_number)
    pyautogui.hotkey('ctrl', 'a')  # Seleccionar todo el texto
    pyautogui.press('backspace')  # Borrar el texto seleccionado
    pyautogui.write(['backspace'] * 10)  # Envía backspace 10 veces para asegurarse de que el campo está vacío
    pyautogui.write(phone_number)  # Escribir el nuevo número de teléfono
    pyautogui.sleep(1)  # Pausa para completar la escritura
    
    # Interactuar con el campo de PIN
    pyautogui.click(x_pin, y_pin)
    pyautogui.hotkey('ctrl', 'a')  # Seleccionar todo el texto
    pyautogui.press('backspace')  # Borrar el texto seleccionado
    pyautogui.write(['backspace'] * 10)  # Envía backspace 10 veces para asegurarse de que el campo está vacío
    pyautogui.write(pin)  # Escribir el nuevo PIN
    pyautogui.sleep(1)  # Pausa para completar la escritura
    
    # Clic en enviar
    pyautogui.click(x_submit, y_submit)
    pyautogui.sleep(3)  # Esperar a que la acción se complete y la página responda
    
    # Capturar una región de la pantalla (ajusta las coordenadas según tus necesidades)
    screenshot = pyautogui.screenshot(region=(x_service_type-100, y_service_type-100, 400, 300))
    text = pytesseract.image_to_string(screenshot)
    print("Datos leídos de la pantalla:", text)
def start_automation():
    phone_number = phone_number_entry.get()
    automate_form(phone_number)

app = tk.Tk()
app.title("Formulario de Automatización")

tk.Label(app, text="Número de teléfono:").pack()
phone_number_entry = tk.Entry(app)
phone_number_entry.pack()

start_button = tk.Button(app, text="Iniciar Automatización", command=start_automation)
start_button.pack()

app.mainloop()
