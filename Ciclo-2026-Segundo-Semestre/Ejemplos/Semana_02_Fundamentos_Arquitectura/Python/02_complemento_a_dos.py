"""Un byte con signo representa enteros de -128 a 127."""

for numero in (-128, -5, 0, 127):
    byte = numero.to_bytes(1, byteorder="little", signed=True)
    sin_signo = int.from_bytes(byte, byteorder="little", signed=False)
    recuperado = int.from_bytes(byte, byteorder="little", signed=True)
    print(f"{numero:4d} -> {sin_signo:08b} -> sin signo: {sin_signo:3d}, con signo: {recuperado}")

# Python usa enteros sin ancho fijo; la máscara limita la inversión a ocho bits.
complemento = ((~5) + 1) & 0xFF
print(f"Complemento a dos de 5 en 8 bits: {complemento:08b}")
