# Semana 05: memoria y direccionamiento

Un arreglo `.quad` contiene cuatro enteros de ocho bytes, alineados a ocho bytes. Las direcciones son virtuales del proceso, no físicas.

| Archivo | Qué enseña y resultado esperado en `resultados` |
| --- | --- |
| [01_memoria_y_offsets.s](ARM64/01_memoria_y_offsets.s) | LDR/STR, offset inmediato e índice por registro escalado. X10=10, X11=20, X14=30; el arreglo pasa a `[10, 25, 30, 40]`. LDRB extiende `FB` con ceros: X16=251; LDRSB lo extiende con signo: X17=−5. |
| [02_pre_post_indexing.s](ARM64/02_pre_post_indexing.s) | Lecturas y escrituras con actualización de base. X10=X11=20. Los offsets guardados en X15/X16/X17 son 8/16/24 bytes respecto a X12; X9 termina en offset 16. Se guarda 99 (también leído en X18) y después 77; el arreglo final es `[10, 20, 77, 40]`. |

## Compilar y observar

Instala los requisitos de la [guía ARM64](../documentacion/arm64.md). Desde `Ejemplos/`:

```bash
make -f Makefile.qemu SRC=Semana_05_Memoria_y_Direccionamiento/ARM64/01_memoria_y_offsets.s run
```

Termina con código 0 y sin texto. Para inspeccionar resultados, inicia en una terminal:

```bash
qemu-aarch64 -g 1234 build/Semana_05_Memoria_y_Direccionamiento/ARM64/01_memoria_y_offsets
```

En otra terminal:

```bash
gdb-multiarch -q build/Semana_05_Memoria_y_Direccionamiento/ARM64/01_memoria_y_offsets
```

Dentro de GDB:

```text
set architecture aarch64
target remote localhost:1234
break resultados
continue
info registers x9 x10 x11 x12 x13 x14 x15 x16 x17 x18
x/4gd &arreglo
x/8xb &arreglo
print /d $x17
detach
quit
```

El arreglo muestra `10 25 30 40`. En little-endian los primeros ocho bytes son `0a 00 00 00 00 00 00 00`; X17 se interpreta como −5. `ldr x9, =arreglo` obtiene una dirección mediante una pseudoinstrucción; `ldr x10, [x9]` lee el contenido de esa dirección.

Repite con `02_pre_post_indexing`. Además de `x/4gd &arreglo`, usa `print /d ($x15-$x12)`, lo mismo para X16/X17 y finalmente `print /d ($x9-$x12)`: deben resultar 8, 16, 24 y 16. Con `[base, #offset]!` se actualiza antes del acceso; con `[base], #offset`, después. Los offsets se expresan en bytes. Usa el puerto GDB solo en un entorno controlado.

En Linux AArch64 nativo cambia a `Makefile.arm64`; esa ejecución física sigue pendiente.

[Índice general](../README.md).
