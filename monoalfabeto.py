import os
import sys

if "--help" in sys.argv or "-h" in sys.argv:
    print(
        "Este programa implementa un cifrado monoalfabético con un pseudoaleatorio basado en una semilla proporcionada por el usuario.\n"
        "Opciones de uso:\n"
        "1. Ingrese un número entero para la semilla cuando se le solicite.\n"
        "2. El programa generará un diccionario de sustitución basado en el texto 'MONOALFABETO' y la semilla proporcionada.\n"
        "3. El resultado del cifrado se mostrará al final junto con el diccionario de sustitución ordenado.\n\n"
        "Nota: El texto a cifrar está predefinido como 'MONOALFABETO', pero puede modificarse en la variable 'texto'.\n"
        "El programa utiliza un método de generación de números pseudoaleatorios para asignar letras del alfabeto a otras letras.\n"
        "El programa asegura que no haya repeticiones en las asignaciones de letras.\n"
        "El usuario debe ingresar un número entero para la semilla.\n"
        "El programa muestra el diccionario de sustitución ordenado alfabéticamente.\n"
        "El resultado final del cifrado se muestra al final del programa.\n")
    sys.exit()

 
if len(sys.argv) > 1:
    config_file = sys.argv[1]
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            texto = f.read()
        print(f"\nCifrando configuración de: {config_file}\n")
    except FileNotFoundError:
        print(f"Error: El archivo '{config_file}' no existe.", file=sys.stderr)
        sys.exit()

else:
    texto = "MONOALFABETO"
    print("\n Cifrando texto de: MONOALFABETO \n")





def cifrado_monoalfabeto(texto):
    texto = texto.upper()
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    a = 4825785162
    c = int(input("Ingrese un número entero para la semilla: ")) * 857412552
    m = 15**32
    semilla = len(texto) * 38

    letras_texto = []
    for letra in texto:
        if letra in alfabeto and letra not in letras_texto:
            letras_texto.append(letra) # añade cada letra única que esté en el alfabeto, sin repetir.

    for letra in alfabeto:
        if letra not in letras_texto:
            letras_texto.append(letra) # añade las letras del alfabeto que no están en el texto, para comprobar un funcionamiento correcto de monoalfabeto

    dic = {} # Diccionario para almacenar las asignaciones de letras
    usadas = []  # lista del texto ya asignadas

    i = 0  

    while i < 26:
        letra_alf = alfabeto[i] # letra actual del alfabeto 
        semilla = (a * semilla + 77 * c) % m # número pseudoaleatorio
        idx_txt = semilla % len(letras_texto) # convertir número a un índice valido
        letra_txt = letras_texto[idx_txt] # letra candidata a sustituir

        while letra_txt in usadas: # si la letra ya fue usada, generar número pseudoaleatorio hasta encontrar una letra no usada
            if len(usadas) == len(letras_texto):
                break
            semilla = (a * semilla + 77 * c) % m
            idx_txt = semilla % len(letras_texto)
            letra_txt = letras_texto[idx_txt]
        
        if len(usadas) == len(letras_texto): # Si todas las letras han sido usadas, salir del bucle
            break

        dic[letra_alf] = letra_txt 
        usadas.append(letra_txt)

        i += 1

  
    resultado = ""
    for letra in texto:
        if letra in dic:
            resultado += dic[letra]


    print("\nDiccionario de sustitución:")
    for clave in sorted(dic.keys()):
        print(clave, "--", dic[clave])

    return resultado

if __name__ == "__main__" :
    
    print("Clave entera:\t\"123\"")
    nombre = os.path.basename(sys.argv[1])
    nombre = os.path.splitext(nombre)[0]

    cifrado = cifrado_monoalfabeto(texto)

    print("\nTexto cifrado:\n", cifrado)

    with open(f"{nombre}_cif.txt", "w") as archivo :
        archivo.write(cifrado)
