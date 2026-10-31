# Semana 04: registros e instrucciones A64

Programas cortos de registros, aritmética, lógica y desplazamientos; no requieren C ni periféricos.

| Archivo | Resultados en la etiqueta `resultados` |
| --- | --- |
| [01_registros.s](ARM64/01_registros.s) | X9=42 tras escribir W9; X10=`0x123456789abcdef0` con MOVZ/MOVK; X11=0 desde XZR. |
| [02_aritmetica.s](ARM64/02_aritmetica.s) | Con 20 y 6: X11=26 (ADD), X12=14 (SUB), X13=120 (MUL), X14=3 (SDIV) y X15=3 (UDIV). W18=`0x80000000` tras sumar 1 a INT32_MAX; flags N=1, Z=0, C=0, V=1. |
| [03_logica_y_desplazamientos.s](ARM64/03_logica_y_desplazamientos.s) | Con `AA` y `0F`: X11=`0A` (AND), X12=`AF` (ORR), X13=`A5` (EOR), X14=`A0` (BIC), X15=`154` (LSL), X16=`55` (LSR), X18=−4 (ASR de −8). Valores de lógica expresados en hexadecimal. |

## Compilar y observar

Instala los requisitos de la [guía ARM64](../documentacion/arm64.md). Todos los comandos parten de `Ejemplos/`:

```bash
make -f Makefile.qemu SRC=Semana_04_Registros_e_Instrucciones_A64/ARM64/01_registros.s run
```

Termina con código 0 y sin texto. Los resultados se observan en GDB, antes de ejecutar la salida del programa. Para ello, en una terminal:

```bash
qemu-aarch64 -g 1234 build/Semana_04_Registros_e_Instrucciones_A64/ARM64/01_registros
```

En otra terminal:

```bash
gdb-multiarch -q build/Semana_04_Registros_e_Instrucciones_A64/ARM64/01_registros
```

Dentro de GDB:

```text
set architecture aarch64
target remote localhost:1234
break resultados
continue
info registers x9 x10 x11 x12 x13 x14 x15 x16 x17 x18 cpsr
print /x $x10
detach
quit
```

Repite cambiando el archivo y ejecutable por `02_aritmetica` o `03_logica_y_desplazamientos`. En aritmética, `print /x ($cpsr & 0xf0000000)` produce `0x90000000` (NZCV). En lógica, `print /d $x18` muestra −4. Usa el puerto de GDB solo en un entorno controlado.

Escribir W9 elimina los 32 bits altos de X9. SDIV trunca hacia cero. LSL opera aquí sobre 64 bits: `0xAA << 1` es `0x154`, no se recorta a ocho bits. Como preparación puedes ejecutar el [ejemplo Python de bits](../Semana_02_Fundamentos_Arquitectura/Python/03_operaciones_bits.py), sin duplicarlo.

En Linux AArch64 nativo cambia a `Makefile.arm64`; esa ejecución física sigue pendiente.

[Índice general](../README.md).
