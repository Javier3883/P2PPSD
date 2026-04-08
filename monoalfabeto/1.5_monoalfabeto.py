#!/usr/bin/env python3
import sys
import os

ALFABETO = list("ABCDEFGHIKLMNOPQRSTUVWXYZ")  # 25 letras, I=J


def ayuda():
    print("""
Uso:
  python G.N_monoalfabeto.py --seed <1|2> --desp <D> --cifrar   <archivo.txt>
  python G.N_monoalfabeto.py --seed <1|2> --desp <D> --descifrar <archivo.txt>
  python G.N_monoalfabeto.py --help

Argumentos:
  --seed <1|2>            Transposicion de columnas de la matriz (por defecto: 2)
                            1 -> columnas IMPARES rotan entre si (1 <-> 3)
                            2 -> columnas PARES rotan entre si  (0 -> 2 -> 4 -> 0)
  --desp <D>              Desplazamiento diagonal fijo (por defecto: 3)
  --cifrar <archivo.txt>  Lee el archivo y cifra su contenido
  --descifrar <arch.txt>  Lee el archivo y descifra su contenido
  --help                  Muestra esta ayuda

Notas:
  - El archivo .txt debe contener solo letras mayusculas A-Z, sin espacios ni simbolos
  - I y J se tratan como la misma letra (el alfabeto tiene 25 letras)
  - Es un cifrado MONOALFABETO: cada letra siempre cifra a la misma letra
  - Para descifrar se debe usar la misma semilla y el mismo desplazamiento
""")


def construir_matriz(semilla):
    # Matriz base: alfabeto en orden
    m = [ALFABETO[i*5:(i+1)*5][:] for i in range(5)]

    if semilla == 1:
        # Columnas impares (1, 3) rotan entre si
        # columna 1 → posicion de columna 3, columna 3 → posicion de columna 1
        for f in range(5):
            m[f][1], m[f][3] = m[f][3], m[f][1]

    elif semilla == 2:
        # Columnas pares (0, 2, 4) rotan entre si
        # columna 0 → posicion de columna 2, columna 2 → posicion de columna 4, columna 4 → posicion de columna 0
        for f in range(5):
            m[f][0], m[f][2], m[f][4] = m[f][4], m[f][0], m[f][2]

    return m


def mostrar_matriz(matriz, semilla, desp):
    print("\n  Matriz 5x5 (seed={}, desp={})".format(semilla, desp))
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


# --- main ---

args = sys.argv[1:]

if not args or "--help" in args:
    ayuda()
    sys.exit(0)

# semilla
if "--seed" not in args:
    semilla = 2
else:
    idx = args.index("--seed")
    try:
        semilla = int(args[idx + 1])
        if semilla not in (1, 2):
            raise ValueError
    except (IndexError, ValueError):
        print("Error: --seed debe ser 1 o 2.")
        sys.exit(1)

# desplazamiento
if "--desp" not in args:
    desp = 3
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

    texto     = leer_txt(ruta)
    resultado = cifrar(texto, matriz, desp)
    nombre    = os.path.splitext(os.path.basename(ruta))[0]

    mostrar_matriz(matriz, semilla, desp)
    print("\n  Archivo    : " + ruta)
    print("\n  Original   : " + texto)
    print("\n  Cifrado    : " + resultado)

    with open(f"{nombre}_cif.txt", "w") as archivo:
        archivo.write(resultado)
    print("\n  Guardado   : {}_cif.txt".format(nombre))
    print()

elif "--descifrar" in args:
    idx = args.index("--descifrar")
    try:
        ruta = args[idx + 1]
    except IndexError:
        print("Error: --descifrar necesita la ruta de un archivo .txt")
        sys.exit(1)

    texto     = leer_txt(ruta)
    resultado = descifrar(texto, matriz, desp)
    nombre    = os.path.splitext(os.path.basename(ruta))[0]

    mostrar_matriz(matriz, semilla, desp)
    print("\n  Archivo    : " + ruta)
    print("\n  Cifrado    : " + texto)
    print("\n  Descifrado : " + resultado)

    with open(f"{nombre}_dec.txt", "w") as archivo:
        archivo.write(resultado)
    print("\n  Guardado   : {}_dec.txt".format(nombre))
    print()

else:
    print("Error: indica --cifrar <archivo.txt> o --descifrar <archivo.txt>. Usa --help.")
    sys.exit(1)