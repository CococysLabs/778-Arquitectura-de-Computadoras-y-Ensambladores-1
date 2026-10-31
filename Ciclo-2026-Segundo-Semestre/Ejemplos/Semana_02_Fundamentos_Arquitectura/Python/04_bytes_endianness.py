"""El orden de bytes cambia; el valor recuperado conserva su significado."""

numero = 0x12345678
for orden in ("little", "big"):
    datos = numero.to_bytes(4, byteorder=orden)
    print(f"{orden}: {datos.hex(' ')}")
    print(f"Recuperado ({orden}): 0x{int.from_bytes(datos, byteorder=orden):08X}")

print("Los bytes se muestran desde el offset 0 hasta el 3; no son direcciones físicas.")
