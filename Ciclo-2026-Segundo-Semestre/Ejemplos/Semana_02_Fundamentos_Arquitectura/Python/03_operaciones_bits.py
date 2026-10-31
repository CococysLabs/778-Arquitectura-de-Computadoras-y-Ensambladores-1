"""Operaciones lógicas y desplazamientos sobre dos patrones conocidos."""

a = 0b10101010
b = 0b00001111
print(f"a:          {a:08b}")
print(f"b:          {b:08b}")
print(f"AND:        {a & b:08b}")
print(f"OR:         {a | b:08b}")
print(f"XOR:        {a ^ b:08b}")
print(f"Borrar b:   {a & ~b:08b}")
print(f"NOT 8 bits: {(~a) & 0xFF:08b}")
print(f"LSL 1:      {a << 1:b} ({a << 1})")
print(f"LSL 8 bits: {(a << 1) & 0xFF:08b}")
print(f"LSR 1:      {a >> 1:08b}")
print(f"-8 >> 1:    {-8 >> 1}")
