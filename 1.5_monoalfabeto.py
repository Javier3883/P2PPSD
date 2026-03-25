#!/usr/bin/env python3
import sys
import random
import os

ALFABETO = list("ABCDEFGHIKLMNOPQRSTUVWXYZ")  # 25 letras, I=J


def ayuda():
    print("""
Uso:
  python cifrado.py --seed <N> --cifrar   <archivo.txt>
  python cifrado.py --seed <N> --descifrar <archivo.txt>
  python cifrado.py --help

Argumentos:
  --seed <N>                    Semilla entera para generar la matriz (por defecto: 123)
  --cifrar <archivo.txt>        Lee el archivo y cifra su contenido
  --descifrar <archivo.txt>     Descifra el texto dado usando la misma semilla
  --help                        Muestra esta ayuda

Notas:
  - El archivo .txt debe contener solo letras mayusculas A-Z, sin espacios ni simbolos
  - I y J se tratan como la misma letra (el alfabeto tiene 25 letras)
  - La matriz se muestra siempre antes del resultado
  - El desplazamiento diagonal mueve cada letra segun su posicion en el texto,
    con wrap a la diagonal izquierda al salir de la matriz
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


def cifrar(texto, matriz):
    resultado = []
    for pos, ch in enumerate(texto):
        f, c = buscar(ch, matriz)
        nf, nc = desplazar(f, c, pos)
        resultado.append(matriz[nf][nc])
    return "".join(resultado)


def descifrar(texto, matriz):
    resultado = []
    for pos, ch in enumerate(texto):
        f, c = buscar(ch, matriz)
        nf, nc = desplazar(f, c, -pos)
        resultado.append(matriz[nf][nc])
    return "".join(resultado)


if __name__ == "__main__":

    args = sys.argv[1:]

    if not args or "--help" in args:
        ayuda()
        sys.exit(0)

    if "--seed" not in args:
        semilla = 123
    else:
        idx_seed = args.index("--seed")
        try:
            semilla = int(args[idx_seed + 1])
        except (IndexError, ValueError):
            print("Error: --seed necesita un numero entero.")
            sys.exit(1)

    matriz = construir_matriz(semilla)

    if "--cifrar" in args:
        idx = args.index("--cifrar")
        try:
            ruta = args[idx + 1]
        except IndexError:
            print("Error: --cifrar necesita la ruta de un archivo .txt")
            sys.exit(1)
        if not ruta.endswith(".txt"):
            print("Error: el archivo debe tener extension .txt")
            sys.exit(1)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                texto = f.read().rstrip("\n").replace("J", "I")
        except FileNotFoundError:
            print("Error: no se encontro el archivo '{}'".format(ruta))
            sys.exit(1)

        cifrado = cifrar(texto, matriz)
        nombre = os.path.splitext(os.path.basename(ruta))[0]

        mostrar_matriz(matriz, semilla)
        print("  Archivo  : " + ruta)
        print("  Original : " + texto)
        print("  Cifrado  : " + cifrado)

        with open(f"{nombre}_cif.txt", "w") as archivo:
            archivo.write(cifrado)
        print("  Guardado : {}_cif.txt".format(nombre))
        print()

    elif "--descifrar" in args:
        idx = args.index("--descifrar")
        try:
            ruta = args[idx + 1]
        except IndexError:
            print("Error: --descifrar necesita la ruta de un archivo .txt")
            sys.exit(1)
        if not ruta.endswith(".txt"):
            print("Error: el archivo debe tener extension .txt")
            sys.exit(1)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                texto = f.read().rstrip("\n").replace("J", "I")
        except FileNotFoundError:
            print("Error: no se encontro el archivo '{}'".format(ruta))
            sys.exit(1)

        descifrado = descifrar(texto, matriz)
        nombre = os.path.splitext(os.path.basename(ruta))[0]

        mostrar_matriz(matriz, semilla)
        print("  Archivo    : " + ruta)
        print("  Cifrado    : " + texto)
        print("  Descifrado : " + descifrado)

        with open(f"{nombre}_dec.txt", "w") as archivo:
            archivo.write(descifrado)
        print("  Guardado   : {}_dec.txt".format(nombre))
        print()

    else:
        print("Error: indica --cifrar <archivo.txt> o --descifrar <TEXTO>. Usa --help.")
        sys.exit(1)