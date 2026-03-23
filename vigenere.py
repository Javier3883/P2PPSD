
def matriz_vigenere():
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    matriz = []

    for i in range(len(alfabeto)):
        fila = ""
        for j in range(len(alfabeto)):
            letra = alfabeto[(i + j) % len(alfabeto)]
            fila += letra + " "
        matriz.append(fila)

    return matriz


def clave():
    clave = input("Ingrese la clave para un cifrado de Vigenere: ")
    clave = clave.upper()
    if len(clave) == 0:
        print("La clave no puede estar vacía ")
        return clave()
    elif len(clave) > 7:
        print("La clave es demasiado larga")
        return clave()
    return clave


def programa(texto_cifrar):
    matrix_completa = matriz_vigenere()
    clave_llamada = clave()
    resultado_cifrado = ""
    
    for i in range(len(texto_cifrar)):
        letra_t = texto_cifrar[i]
        indice_columna = matrix_completa[0].index(letra_t)
        letra_clave = clave_llamada[i % len(clave_llamada)]
        indice_fila = 0
        for i in range(len(matrix_completa)):
            if matrix_completa[i][0] == letra_clave:
                indice_fila = i
                break
        
        # LETRA CIFRADA
        letra_cifrada = matrix_completa[indice_fila][indice_columna]
        resultado_cifrado += letra_cifrada

    return resultado_cifrado 

"""
if __name__ == "__main__":
        
    with open("1.5_fragmento1.txt", "r", encoding="utf-8") as f:
        texto = f.read()


    matriz = matriz_vigenere()
    print("Matriz de Vigenere: ")
    for fila in matriz :
        print(fila)
    print("\n")

    print("Algoritmo cifrado: ")
    print("\n")
    print("Clave: \"ada\"")
    cifrado = programa(texto)
    print(cifrado)

    with open("1.5_fragmento3_cif.txt", "w") as archivo :
        archivo.write(cifrado)
"""