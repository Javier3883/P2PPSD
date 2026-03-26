#!/usr/bin/env python3
import sys
import os

def ayuda():
    print("""
Uso:
  python G.N_vigenere.py --clave <CLAVE> --cifrar   <archivo.txt>
  python G.N_vigenere.py --clave <CLAVE> --descifrar <archivo.txt>
  python G.N_vigenere.py --help

Argumentos:
  --clave <CLAVE>           Clave para el cifrado (por defecto: "PATA")
  --cifrar <archivo.txt>    Cifra el contenido del archivo
  --descifrar <arch.txt>    Descifra el contenido del archivo
  --help                    Muestra esta ayuda

Notas:
  - El archivo .txt debe contener letras A-Z.
  - Es un cifrado VIGENERE: cada letra se cifra con una letra de la clave.
  - La clave se repite para cubrir todo el texto.
""")

def matriz_vigenere():
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    matriz = []
    for i in range(len(alfabeto)):
        fila = []
        for j in range(len(alfabeto)):
            letra = alfabeto[(i + j) % len(alfabeto)]
            fila.append(letra)
        matriz.append(fila)
    return matriz


def mostrar_matriz(matriz, clave_usada):
    print("\n  Matriz Vigenere (Clave={})".format(clave_usada))
    linea = "  +"
    for _ in range(len(matriz[0])):
        linea += "---+"
    
    print(linea)
    for fila in matriz:
        cuerpo_fila = "  | "
        for letra in fila:
            cuerpo_fila += letra + " | "
        print(cuerpo_fila)
        print(linea)
    print()


def programa_encriptar(texto_cifrar, clave_llamada):
    matrix_completa = matriz_vigenere()
    resultado_cifrado = ""
    alfabeto_guia = matrix_completa[0]
    
    for i in range(len(texto_cifrar)):
        letra_t = texto_cifrar[i]
        indice_columna = alfabeto_guia.index(letra_t)
        letra_clave = clave_llamada[i % len(clave_llamada)]
        
        indice_fila = 0
        for j in range(len(matrix_completa)):
            if matrix_completa[j][0] == letra_clave:
                indice_fila = j
                break
        
        letra_cifrada = matrix_completa[indice_fila][indice_columna]
        resultado_cifrado += letra_cifrada

    return resultado_cifrado


def programa_desencriptar(texto_cifrado, clave_llamada):
    matriz_completa = matriz_vigenere()
    resultado_desencriptado = ""
    alfabeto_guia = matriz_completa[0]
    
    for i in range(len(texto_cifrado)):
        letra_c = texto_cifrado[i]
        letra_clave = clave_llamada[i % len(clave_llamada)]
        
        indice_fila = 0
        for j in range(len(matriz_completa)):
            if matriz_completa[j][0] == letra_clave:
                indice_fila = j
                break
        
        fila_actual = matriz_completa[indice_fila]
        indice_columna = fila_actual.index(letra_c)
        letra_desencriptada = alfabeto_guia[indice_columna]
        resultado_desencriptado += letra_desencriptada

    return resultado_desencriptado


def leer_txt(ruta):
        if not ruta.endswith(".txt"):
            print("Error: el archivo debe tener extension .txt")
            sys.exit(1)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return f.read().rstrip("\n")
        except FileNotFoundError:
            print("Error: no se encontro el archivo '{}'".format(ruta))
            sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or "--help" in args:
        ayuda()
        sys.exit(0)

    # CLAVE
    if "--clave" not in args:
        clave_a_usar = "PATA"
    else:
        idx_c = args.index("--clave")
        try:
            clave_a_usar = args[idx_c + 1].upper()
        except IndexError:
            print("Error: --clave necesita un valor.")
            sys.exit(1)

    matriz = matriz_vigenere()

    if "--cifrar" in args:
        idx = args.index("--cifrar")
        try:
            ruta = args[idx + 1]
        except IndexError:
            print("Error: --cifrar necesita la ruta de un archivo .txt")
            sys.exit(1)

        texto = leer_txt(ruta)
        resultado = programa_encriptar(texto, clave_a_usar)
        nombre = os.path.splitext(os.path.basename(ruta))[0]

        mostrar_matriz(matriz, clave_a_usar)
        print("\n  Archivo      : " + ruta)
        print("\n  Clave        : " + clave_a_usar)
        print("\n  Original     : " + texto)
        print("\n  Cifrado      : " + resultado)

        with open(f"{nombre}_cif.txt", "w", encoding="utf-8") as archivo:
            archivo.write(resultado)
        print("\n  Guardado     : {}_cif.txt".format(nombre))

    elif "--descifrar" in args:
        idx = args.index("--descifrar")
        try:
            ruta = args[idx + 1]
        except IndexError:
            print("Error: --descifrar necesita la ruta de un archivo .txt")
            sys.exit(1)

        texto = leer_txt(ruta)
        resultado = programa_desencriptar(texto, clave_a_usar)
        nombre = os.path.splitext(os.path.basename(ruta))[0]

        mostrar_matriz(matriz, clave_a_usar)
        print("\n  Archivo      : " + ruta)
        print("\n  Clave        : " + clave_a_usar)
        print("\n  Cifrado      : " + texto)
        print("\n  Descifrado   : " + resultado)

        with open(f"{nombre}_dec.txt", "w", encoding="utf-8") as archivo:
            archivo.write(resultado)
        print("\n  Guardado     : {}_dec.txt".format(nombre))

    else:
        print("Error: indica --cifrar o --descifrar. Usa --help.")
        sys.exit(1)