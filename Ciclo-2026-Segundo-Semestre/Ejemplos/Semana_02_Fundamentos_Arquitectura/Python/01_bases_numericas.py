"""El mismo entero puede escribirse en distintas bases."""

numero = 42
print(f"Decimal: {numero}")
print(f"Binario: {numero:08b}")
print(f"Hexadecimal: {numero:02X}")
print(f"Desde binario 00101010: {int('00101010', 2)}")
print(f"Desde hexadecimal 2A: {int('2A', 16)}")
