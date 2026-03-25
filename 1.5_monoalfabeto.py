#!/usr/bin/env python3
import sys
import random
import os

ALFABETO = list("ABCDEFGHIKLMNOPQRSTUVWXYZ")  # 25 letras, I=J


def ayuda():
    print("""
Uso:
  python cifrado.py --seed <N> --desp <D> --cifrar   <archivo.txt>
  python cifrado.py --seed <N> --desp <D> --descifrar <archivo.txt>
  python cifrado.py --help

Argumentos:
  --seed <N>              Semilla para generar la matriz (por defecto: 123)
  --desp <D>              Desplazamiento diagonal fijo (por defecto: 1)
  --cifrar <archivo.txt>  Lee el archivo y cifra su contenido
  --descifrar <arch.txt>  Lee el archivo y descifra su contenido
  --help                  Muestra esta ayuda

Notas:
  - El archivo .txt debe contener solo letras mayusculas A-Z, sin espacios ni simbolos
  - I y J se tratan como la misma letra (el alfabeto tiene 25 letras)
  - Es un cifrado MONOALFABETO: cada letra siempre cifra a la misma letra
  - El desplazamiento es fijo para todas las letras (no depende de la posicion)
  - Para descifrar se debe usar la misma semilla y el mismo desplazamiento
""")


def construir_matriz(semilla):
    letras = ALFABETO[:]
    random.seed(semilla)
    random.shuffle(letras)
    return [letras[i*5:(i+1)*5] for i in range(5)]


def mostrar_matriz(matriz, semilla):
    print("\n  Matriz 5x5 (semilla={})".format(semilla))
    print("  +---+---+---+---+---+")
    for fila in matriz:
        print("  | " + " | ".join(fila) + " |")
        print("  +---+---+---+---+---+")
    print()


def orden_diagonal():
    celdas = []
    for d in range(9):
        for f in range(5):
            c = d - f
            if 0 <= c < 5:
                celdas.append((f, c))
    return celdas


def buscar(letra, matriz):
    for f in range(5):
        for c in range(5):
            if matriz[f][c] == letra:
                return (f, c)


def desplazar(f, c, pasos):
    orden = orden_diagonal()
    pos = orden.index((f, c))
    return orden[(pos + pasos) % 25]


def cifrar(texto, matriz, desp):
    resultado = []
    for ch in texto:
        f, c = buscar(ch, matriz)
        nf, nc = desplazar(f, c, desp)
        resultado.append(matriz[nf][nc])
    return "".join(resultado)


def descifrar(texto, matriz, desp):
    resultado = []
    for ch in texto:
        f, c = buscar(ch, matriz)
        nf, nc = desplazar(f, c, -desp)
        resultado.append(matriz[nf][nc])
    return "".join(resultado)

def leer_txt(ruta):
        if not ruta.endswith(".txt"):
            print("Error: el archivo debe tener extension .txt")
            sys.exit(1)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return f.read().rstrip("\n").replace("J", "I")
        except FileNotFoundError:
            print("Error: no se encontro el archivo '{}'".format(ruta))
            sys.exit(1)


if __name__ == "__main__":

    args = sys.argv[1:]

    if not args or "--help" in args:
        ayuda()
        sys.exit(0)

    # semilla
    if "--seed" not in args:
        semilla = 123
    else:
        idx = args.index("--seed")
        try:
            semilla = int(args[idx + 1])
        except (IndexError, ValueError):
            print("Error: --seed necesita un numero entero.")
            sys.exit(1)

    # desplazamiento
    if "--desp" not in args:
        desp = 1
    else:
        idx = args.index("--desp")
        try:
            desp = int(args[idx + 1])
        except (IndexError, ValueError):
            print("Error: --desp necesita un numero entero.")
            sys.exit(1)

    matriz = construir_matriz(semilla)


    if "--cifrar" in args:
        idx = args.index("--cifrar")
        try:
            ruta = args[idx + 1]
        except IndexError:
            print("Error: --cifrar necesita la ruta de un archivo .txt")
            sys.exit(1)

        texto  = leer_txt(ruta)
        resultado = cifrar(texto, matriz, desp)
        nombre = os.path.splitext(os.path.basename(ruta))[0]

        mostrar_matriz(matriz, semilla)
        print("  Archivo      : " + ruta)
        print("  Desplazamiento: {}".format(desp))
        print("  Original     : " + texto)
        print("  Cifrado      : " + resultado)

        with open(f"{nombre}_cif.txt", "w") as archivo:
            archivo.write(resultado)
        print("  Guardado     : {}_cif.txt".format(nombre))
        print()

    elif "--descifrar" in args:
        idx = args.index("--descifrar")
        try:
            ruta = args[idx + 1]
        except IndexError:
            print("Error: --descifrar necesita la ruta de un archivo .txt")
            sys.exit(1)

        texto  = leer_txt(ruta)
        resultado = descifrar(texto, matriz, desp)
        nombre = os.path.splitext(os.path.basename(ruta))[0]

        mostrar_matriz(matriz, semilla)
        print("  Archivo      : " + ruta)
        print("  Desplazamiento: {}".format(desp))
        print("  Cifrado      : " + texto)
        print("  Descifrado   : " + resultado)

        with open(f"{nombre}_dec.txt", "w") as archivo:
            archivo.write(resultado)
        print("  Guardado     : {}_dec.txt".format(nombre))
        print()

    else:
        print("Error: indica --cifrar <archivo.txt> o --descifrar <archivo.txt>. Usa --help.")
        sys.exit(1)