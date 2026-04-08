#!/usr/bin/env python3
import sys
import os

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



def analisis_frecuencias(texto):
    frec = {}
    for letra in texto:
        if letra in frec:
            frec[letra] += 1
        else:
            frec[letra] = 1
    
    total_letras = sum(frec.values())
    frecuencias = {letra: (cantidad / total_letras) * 100 for letra, cantidad in frec.items()}
    return frecuencias 


def analisis_digrafos(texto):
    frec = {}
    for i in range(len(texto) - 1):
        digrafo = texto[i:i+2]
        frec[digrafo] = frec.get(digrafo, 0) + 1
    
    total_digrafos = sum(frec.values())
    frecuencias = {d: (cant / total_digrafos) * 100 for d, cant in frec.items()}
    return frecuencias


def trigrafos(texto):
    frec = {}
    for i in range(len(texto) - 2):
        trigrafo = texto[i:i+3]
        frec[trigrafo] = frec.get(trigrafo, 0) + 1
    
    total_trigrafos = sum(frec.values())
    frecuencias = {t: (cant / total_trigrafos) * 100 for t, cant in frec.items()}
    return frecuencias

def tetragrafos(texto):
    frec = {}
    for i in range(len(texto) - 3):
        tetragrafo = texto[i:i+4]
        frec[tetragrafo] = frec.get(tetragrafo, 0) + 1
    
    total_cuatrigrafos = sum(frec.values())
    frecuencias = {c: (cant / total_cuatrigrafos) * 100 for c, cant in frec.items()}
    return frecuencias

def pentagrafos(texto):
    frec = {}
    for i in range(len(texto) - 4):
        pentagrafo = texto[i:i+5]
        frec[pentagrafo] = frec.get(pentagrafo, 0) + 1
    
    total_pentagrafos = sum(frec.values())
    frecuencias = {p: (cant / total_pentagrafos) * 100 for p, cant in frec.items()}
    return frecuencias


def obtener_valor(item):
    return item[1]


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Uso: python script.py <ruta_al_archivo.txt>")
        sys.exit(1)

    ruta = sys.argv[1]

    texto = leer_txt(ruta)
    nombre = os.path.splitext(os.path.basename(ruta))[0]

    print("\n  Archivo      : " + ruta)
    print("\n  Original     : " + texto)

    resultado_frecuencias = analisis_frecuencias(texto)
    resultado_digrafos = analisis_digrafos(texto)
    resultado_trigrafos = trigrafos(texto)
    resultado_tetragrafos = tetragrafos(texto)
    resultado_pentagrafos = pentagrafos(texto)


    
    print("\n--- Análisis de frecuencias ---\n")

    print("Frecuencias de letras:")
    for letra, porcentaje in sorted(resultado_frecuencias.items(), key=obtener_valor, reverse=True):
        print(f"{letra}: {porcentaje:.2f}%")

    print("\nFrecuencias de dígrafos:")
    for digrafo, porcentaje in sorted(resultado_digrafos.items(), key=obtener_valor, reverse=True):
        print(f"{digrafo}: {porcentaje:.2f}%")

    print("\nFrecuencias de trigrafos:")
    for trigrafo, porcentaje in sorted(resultado_trigrafos.items(), key=obtener_valor, reverse=True):
        print(f"{trigrafo}: {porcentaje:.2f}%")

    print("\nFrecuencias de tetragrafos:")
    for tetragrafo, porcentaje in sorted(resultado_tetragrafos.items(), key=obtener_valor, reverse=True):
        print(f"{tetragrafo}: {porcentaje:.2f}%")
    
    print("\nFrecuencias de pentagrafos:")
    for pentagrafo, porcentaje in sorted(resultado_pentagrafos.items(), key=obtener_valor, reverse=True):
        print(f"{pentagrafo}: {porcentaje:.2f}%")