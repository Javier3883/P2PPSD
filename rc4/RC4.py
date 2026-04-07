import array
from typing import Any

def KSA(S: list[int], key: list[int]) -> list[int]:
    """Key-scheduling algorithm."""
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S: list[int], message: list[Any]) -> int:
    """Pseudo-random generation algorithm."""
    KS = array.array('i', [0] * len(message))
    i = j = k = 0
    while k < len(message):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        KS[k] = S[t]
        k += 1
    return KS