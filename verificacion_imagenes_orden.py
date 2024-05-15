import os

ruta_capturas = r'C:\Users\PC_\Documents\tienda pastrana\automatizacion\capturas'

def verificar_numeros_faltantes(ruta):
    numeros_presentes = set()
    numeros_faltantes = []

    for filename in os.listdir(ruta):
        if filename.endswith('.png'):
            partes_nombre = filename.split('_')
            if len(partes_nombre) == 2:
                numero = partes_nombre[0]
                numeros_presentes.add(numero)

    for i in range(1, len(os.listdir(ruta)) + 1):
        if str(i) not in numeros_presentes:
            numeros_faltantes.append(i)

    return numeros_faltantes

numeros_faltantes = verificar_numeros_faltantes(ruta_capturas)

if numeros_faltantes:
    print("Los siguientes números están faltantes en los nombres de archivo:")
    for numero in numeros_faltantes:
        print(numero)
else:
    print("No falta ningún número en los nombres de archivo.")
