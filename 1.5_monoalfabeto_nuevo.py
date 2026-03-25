
import os
import sys


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
    print("\nCifrando texto de: MONOALFABETO\n")


def semilla(numero):
    a = 1103515245
    c = 12345
    m = 2**31
    return (a * numero + c) % m

def matriz(): 
    alfabeto = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matriz = []
    for i in range(5):
        fila = []
        for j in range(5):
            fila.append(alfabeto[i*5 + j])
        matriz.append(fila)
    return matriz


def matriz_aleatoria_numeros(b):
    numeros = [i for i in range(25)]
    matriz2 = []
    numero_aleatorio = semilla(b) 
    
    for i in range(5):
        fila = []
        for j in range(5):
            idx = numero_aleatorio % len(numeros)
            fila.append(numeros[idx])
            numeros.pop(idx)
            numero_aleatorio = semilla(numero_aleatorio)
            
            
        matriz2.append(fila)
    return matriz2

def matriz_nueva_origial_ordenada_por_matriz2(matriz1, matriz2):
    matriz3= []
    matriz1 = [letra for fila in matriz1 for letra in fila]
    for i in range(5):
        fila = []
        for j in range(5):
            idx = matriz2[i][j]
            fila.append(matriz1[idx])
        matriz3.append(fila)
    return matriz3

def desplazar_matriz3(matriz3, desplazamiento):
    lista = [matriz3[i][j] for i in range(5) for j in range(5)]
    n = len(lista)
    desplazamiento = desplazamiento % n 
    punto_corte = n - desplazamiento
    lista = lista[punto_corte:] + lista[:punto_corte]

    matriz_desplazada = []
    idx = 0
    for _ in range(5):
        fila = []
        for _ in range(5):
            fila.append(lista[idx])
            idx += 1
        matriz_desplazada.append(fila)

    return matriz_desplazada

def diccionario_matrices(matriz_original, matriz_desplazada):
    dic = {}
    for i in range(5):
        for j in range(5):
            letra_original = matriz_original[i][j]
            letra_desplazada = matriz_desplazada[i][j]
            dic[letra_original] = letra_desplazada
    return dic


def cifrado_monoalfabeto(texto):
    texto_cifrado = ""
    for letra in texto:
        if letra in diccionario_final:
            texto_cifrado += diccionario_final[letra]
    return texto_cifrado


if __name__ == "__main__":
    b = int(input("Ingrese un número entero para la semilla inicial: "))
    matriz1 = matriz()
    matriz2 = matriz_aleatoria_numeros(b)
    matriz3 = matriz_nueva_origial_ordenada_por_matriz2(matriz1, matriz2)
    matriz3_desplazada = desplazar_matriz3(matriz3, semilla(b))
    diccionario_final = diccionario_matrices(matriz1, matriz3_desplazada)
    texto_cifrado = cifrado_monoalfabeto(texto)


    """
    print("\n Matriz original: \n")
    for fila in matriz1:
        print(fila)


    print("\n Matriz de números aleatorios: \n")
    for fila in matriz2:
        print(fila)

    print("\n Matriz nueva ordenada por la matriz de números aleatorios: \n")
    for fila in matriz3:
        print(fila)

    print("\n Matriz desplazada por el valor de la semilla normalizada: \n")
    for fila in matriz3_desplazada:
        print(fila)
    
    """


    print("\n Diccionario de sustitución: \n")
    for clave in sorted(diccionario_final.keys()):
        print(clave, "--", diccionario_final[clave])

    print("\n Texto cifrado: \n")
    print(texto_cifrado)

    if len(sys.argv) > 1:
        nombre = os.path.basename(sys.argv[1])
        nombre = os.path.splitext(nombre)[0]
        salida = f"{nombre}_cif.txt"
    else:
        salida = "1.5_monoalfabeto_cif.txt"

    with open(salida, "w", encoding="utf-8") as archivo:
        archivo.write(texto_cifrado)

