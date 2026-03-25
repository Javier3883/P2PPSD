with open("1.5_fragmento1.txt", "r", encoding="utf-8") as f:
                original = f.read().rstrip("\n").replace("J", "I")


with open("1.5_fragmento1_cif_dec.txt", "r", encoding="utf-8") as f:
                decode = f.read().rstrip("\n").replace("J", "I")

assert original == decode, "El texto decodificado no coincide con el original"
print("El texto decodificado coincide con el original")