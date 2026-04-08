#!/usr/bin/env python3
"""
RC4 Implementation with Interactive Encryption/Decryption
"""
 
import sys
import os
 
 
def KSA(key: list[int], S: list[int] = None) -> list[int]:
    """Key-scheduling algorithm (KSA)."""
    if S is None:
        S = list(range(256))
    else:
        S = S.copy()
    
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S
 
 
def PRGA(message_len: int, S: list[int]) -> list[int]:
    """Pseudo-random generation algorithm (PRGA)."""
    S = S.copy()
    KS = []
    i = j = 0
    
    for k in range(message_len):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        KS.append(S[t])
    
    return KS
 
 
def hex_to_key(hex_string: str) -> list[int]:
    """Convert hexadecimal string to list of integers."""
    hex_string = hex_string.replace(" ", "")
    if len(hex_string) % 2 != 0:
        raise ValueError("La clave hexadecimal debe tener un número par de caracteres.")
    return [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]
 
 
def char_to_ascii(char: str) -> int:
    """Convert character to ASCII value."""
    return ord(char)
 
 
def ascii_to_binary(value: int) -> str:
    """Convert ASCII value to 8-bit binary string."""
    return format(value, '08b')
 
 
def decimal_to_hex(value: int) -> str:
    """Convert decimal value to hexadecimal."""
    return format(value, '02x')
 
 
def display_S_state(S: list[int], label: str, detailed: bool = False):
    """Display the state of S array."""
    print(f"\n{label}")
    print("-" * 80)
    if detailed:
        # Show in rows of 16 for readability
        for i in range(0, 256, 16):
            print(f"S[{i:3d}-{min(i+15, 255):3d}]: {' '.join(f'{val:3d}' for val in S[i:i+16])}")
    else:
        # Compact view
        print(f"S = [{', '.join(str(x) for x in S)}]")
 
 
def encrypt_interactive(key: list[int]):
    """Interactive encryption mode - character by character."""
    print("\n" + "=" * 80)
    print("MODO CIFRADO - ENCRIPTACIÓN INTERACTIVA")
    print("=" * 80)
    
    # Display initial state
    S_initial = list(range(256))
    display_S_state(S_initial, "Estado inicial de S:", detailed=False)
    
    # Apply KSA
    S = KSA(key)
    display_S_state(S, "Estado de S después de KSA:", detailed=False)
    
    print("\n" + "=" * 80)
    print("Introduce el texto a cifrar (línea vacía para finalizar):")
    print("=" * 80)
    
    encrypted_result = []
    S_current = S.copy()
    i = j = 0
    
    try:
        while True:
            try:
                char = input()
                if char == "":
                    break
                
                for single_char in char:
                    ascii_val = char_to_ascii(single_char)
                    ascii_bin = ascii_to_binary(ascii_val)
                    
                    # Generate next keystream byte
                    i = (i + 1) % 256
                    j = (j + S_current[i]) % 256
                    S_current[i], S_current[j] = S_current[j], S_current[i]
                    t = (S_current[i] + S_current[j]) % 256
                    keystream_val = S_current[t]
                    keystream_bin = ascii_to_binary(keystream_val)
                    
                    # Encrypt
                    encrypted_val = ascii_val ^ keystream_val
                    encrypted_bin = ascii_to_binary(encrypted_val)
                    encrypted_hex = decimal_to_hex(encrypted_val)
                    
                    # Display results
                    print(f"\nCaracter: '{single_char}'")
                    print(f"  ASCII:          {ascii_val:3d} | Binario: {ascii_bin}")
                    print(f"  Keystream:      {keystream_val:3d} | Binario: {keystream_bin}")
                    print(f"  Cifrado:        Binario: {encrypted_bin} | Hexadecimal: {encrypted_hex}")
                    print(f"  Estado S actualizado: S[{i}]={S_current[i]}, S[{j}]={S_current[j]}, t={t}, S[t]={keystream_val}")
                    
                    encrypted_result.append(encrypted_val)
                    
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\n\nCifrado cancelado.")
        return
    
    # Display final result
    print("\n" + "=" * 80)
    print("RESULTADO FINAL DEL CIFRADO")
    print("=" * 80)
    encrypted_hex = ''.join(decimal_to_hex(val) for val in encrypted_result)
    print(f"Texto cifrado (Hexadecimal): {encrypted_hex}")
    print(f"Longitud: {len(encrypted_result)} bytes")
    print("=" * 80)
 
 
def decrypt_interactive(key: list[int]):
    """Interactive decryption mode - entire hex string at once."""
    print("\n" + "=" * 80)
    print("MODO DESCIFRADO")
    print("=" * 80)
    
    while True:
        hex_input = input("Introduce el texto a descifrar en formato hexadecimal: ").strip()
        
        if hex_input == "":
            print("Descifrado cancelado.")
            return
        
        try:
            # Convert hex to bytes
            hex_input = hex_input.replace(" ", "")
            if len(hex_input) % 2 != 0:
                print("Error: La entrada hexadecimal debe tener un número par de caracteres.")
                continue
            
            encrypted_bytes = [int(hex_input[i:i+2], 16) for i in range(0, len(hex_input), 2)]
            break
        except ValueError:
            print("Error: Entrada hexadecimal inválida. Intenta de nuevo.")
            continue
    
    # Generate keystream
    S = KSA(key)
    KS = PRGA(len(encrypted_bytes), S)
    
    # Decrypt
    decrypted_bytes = [encrypted_bytes[i] ^ KS[i] for i in range(len(encrypted_bytes))]
    
    # Convert to ASCII
    try:
        decrypted_text = ''.join(chr(val) for val in decrypted_bytes)
        print("\n" + "=" * 80)
        print("RESULTADO DEL DESCIFRADO")
        print("=" * 80)
        print(f"Texto descifrado (ASCII): {decrypted_text}")
        print("=" * 80)
    except ValueError:
        print("\nError: No se puede convertir el resultado a ASCII válido.")
        print(f"Bytes descifrados: {decrypted_bytes}")
 
 
def show_help():
    """Muestra la pantalla de ayuda."""
    nombre_programa = os.path.basename(sys.argv[0])
    print("""
================================================================================
\t\t\tAYUDA - RC4 IMPLEMENTATION
================================================================================
 
SINTAXIS:
    python """ + nombre_programa + """ [OPCIONES]
 
OPCIONES:
    --help              Muestra esta ayuda y sale
    --key <clave>       Especifica la clave en formato hexadecimal (OBLIGATORIO)
    --encrypt           Modo cifrado - encriptación interactiva carácter por carácter
    --decrypt           Modo descifrado - desencriptación de texto hexadecimal
    (NO PUEDES USAR --encrypt Y --decrypt JUNTOS, DEBES ESPECIFICAR EXACTAMENTE UNO)
 
FORMATO DE LA CLAVE:
    - Debe introducirse en hexadecimal
    - Ejemplo: "0102030405" o "01 02 03 04 05" (los espacios se ignoran)
    - Mínimo 1 byte (2 caracteres hex), máximo 255 bytes
 
MODO CIFRADO (--encrypt):
    1. Se mostrará el estado inicial de S = [0, 1, 2, ..., 255]
    2. Se mostrará el estado de S después del KSA (Key-Scheduling Algorithm)
    3. Introduce el texto a cifrar línea por línea
    4. Presiona Enter en línea vacía para terminar el cifrado
    5. Para cada carácter se mostrará:
       - Su valor ASCII en decimal y binario
       - El valor del keystream en decimal y binario
       - El resultado cifrado en binario y hexadecimal
       - Cómo se actualiza el estado S durante el proceso
    6. Al finalizar se muestra el texto cifrado completo en hexadecimal
 
MODO DESCIFRADO (--decrypt):
    1. Introduce el texto cifrado en formato hexadecimal (todo de una vez)
    2. Se mostrará directamente el texto descifrado en formato ASCII sin 
    \tpasos intermedios.
 
CONSIDERACIONES:
    - El texto no puede exceder 256 bytes en una sesión continua
    - Los caracteres se interpretan como ASCII
    - La clave debe ser válida en formato hexadecimal
    - Los espacios en la clave hexadecimal se ignoran automáticamente
 
    
================================================================================
""")
 
 
def parse_arguments(args: list[str]) -> tuple:
    """
    Parsea los argumentos de línea de comandos manualmente.
    
    Args:
        args: Lista de argumentos (sys.argv[1:])
    
    Returns:
        Tupla (clave, modo) donde modo es 'encrypt', 'decrypt' o None
    
    Raises:
        SystemExit: Si hay error en los argumentos
    """
    if not args or "--help" in args:
        show_help()
        sys.exit(0)
    
    key_hex = None
    modo = None
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg == "--key":
            if i + 1 >= len(args):
                print("Error: --key requiere un valor (clave en hexadecimal)", file=sys.stderr)
                print(f"Usa 'python3 {os.path.basename(sys.argv[0])} --help' para más información", file=sys.stderr)
                sys.exit(1)
            key_hex = args[i + 1]
            i += 2
            
        elif arg == "--encrypt":
            if modo is not None:
                print("Error: No puedes especificar --encrypt y --decrypt a la vez", file=sys.stderr)
                print(f"Usa 'python3 {os.path.basename(sys.argv[0])} --help' para más información", file=sys.stderr)
                sys.exit(1)
            modo = "encrypt"
            i += 1
            
        elif arg == "--decrypt":
            if modo is not None:
                print("Error: No puedes especificar --encrypt y --decrypt a la vez", file=sys.stderr)
                print(f"Usa 'python3 {os.path.basename(sys.argv[0])} --help' para más información", file=sys.stderr)
                sys.exit(1)
            modo = "decrypt"
            i += 1
            
        elif arg == "--help":
            show_help()
            sys.exit(0)
            
        else:
            print(f"Error: Argumento desconocido '{arg}'", file=sys.stderr)
            print(f"Usa 'python3 {os.path.basename(sys.argv[0])} --help' para más información", file=sys.stderr)
            sys.exit(1)
    
    # Validar que se proporcionó la clave
    if key_hex is None:
        print("Error: Debes especificar la clave con --key", file=sys.stderr)
        print(f"Usa 'python3 {os.path.basename(sys.argv[0])} --help' para más información", file=sys.stderr)
        sys.exit(1)
    
    # Validar que se especificó el modo
    if modo is None:
        print("Error: Debes especificar --encrypt o --decrypt", file=sys.stderr)
        print(f"Usa 'python3 {os.path.basename(sys.argv[0])} --help' para más información", file=sys.stderr)
        sys.exit(1)
    
    return key_hex, modo
 
 
def main():
    """Función principal del programa."""
    try:
        # Parsear argumentos
        args = sys.argv[1:]
        key_hex, modo = parse_arguments(args)
        
        # Convertir clave hexadecimal a lista de decimales
        key = hex_to_key(key_hex)
        
        # Mostrar la clave en ambos formatos
        print(f"\nClave (hexadecimal): {key_hex}")
        print(f"Clave (decimal): {' '.join(str(k) for k in key)}")
        
        # Ejecutar el modo seleccionado
        if modo == "encrypt":
            encrypt_interactive(key)
        elif modo == "decrypt":
            decrypt_interactive(key)
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)
 
 
if __name__ == '__main__':
    main()