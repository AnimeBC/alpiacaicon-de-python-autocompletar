import os

def verificar_secuencia_imagenes(carpeta):
    # Lista para almacenar los números extraídos de los nombres de archivos
    numeros = []
    
    # Recorrer todos los archivos en la carpeta especificada
    for archivo in os.listdir(carpeta):
        # Asegurarse de que el archivo es una imagen PNG
        if archivo.endswith(".png"):
            # Extraer la parte del nombre del archivo que precede al primer guión bajo
            numero = archivo.split('_')[0]
            if numero.isdigit():
                numeros.append(int(numero))
    
    # Ordenar la lista de números y verificar la secuencia
    numeros.sort()
    
    # Crear una lista de los números esperados basada en el rango de números encontrados
    numeros_esperados = list(range(min(numeros), max(numeros) + 1))
    
    # Encontrar números faltantes
    faltantes = [num for num in numeros_esperados if num not in numeros]
    
    if faltantes:
        print("Números de orden faltantes o mal secuenciados:", faltantes)
    else:
        print("Todos los números están correctamente secuenciados.")

# Ruta de la carpeta donde se almacenan las imágenes
ruta_carpeta = r'C:\Users\PC_\Documents\tienda pastrana\automatizacion\capturas'
verificar_secuencia_imagenes(ruta_carpeta)
