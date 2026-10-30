# Semana 03: entorno ARM64

Filas 15–20 de `5_Diseño_Curricular.xlsx`, hoja `Diseño`, periodo Segundo Semestre 2026: toolchain GNU, QEMU, Make, GDB y ELF.

Se conserva [00_hello_world.s](ARM64/00_hello_world.s). Un solo programa permite recorrer ensamblado, enlace, ejecución e inspección. El mensaje usa la rutina compartida de escritura; aquí se estudia el entorno, no su implementación.

## Ensamblar y ejecutar

Instala los requisitos de la [guía ARM64](../documentacion/arm64.md). Desde la raíz `Ejemplos/`:

```bash
make -f Makefile.qemu SRC=Semana_03_Entorno_ARM64/ARM64/00_hello_world.s run
```

Resultado: `Hello, World!` seguido de un salto de línea; código de salida 0. El objeto y el ELF quedan en `build/Semana_03_Entorno_ARM64/ARM64/`.

## Inspeccionar el ejecutable

```bash
aarch64-linux-gnu-readelf -h -S -s build/Semana_03_Entorno_ARM64/ARM64/00_hello_world
aarch64-linux-gnu-objdump -d build/Semana_03_Entorno_ARM64/ARM64/00_hello_world
```

Busca `ELF64`, máquina `AArch64`, secciones `.text` y `.data`, símbolo `_start` e instrucciones como `mov`, `bl` y `svc`. El desensamblador puede mostrar alias equivalentes de instrucciones.

## Inspeccionar con GDB

En una terminal, desde `Ejemplos/`:

```bash
qemu-aarch64 -g 1234 build/Semana_03_Entorno_ARM64/ARM64/00_hello_world
```

En otra terminal, también desde `Ejemplos/`:

```bash
gdb-multiarch -q build/Semana_03_Entorno_ARM64/ARM64/00_hello_world
```

Dentro de GDB:

```text
set architecture aarch64
target remote localhost:1234
break *_start+4
continue
x/6i $pc
stepi
info registers x1 pc
x/14cb $x1
detach
quit
```

El breakpoint está en la segunda instrucción de `_start` (cada instrucción A64 ocupa cuatro bytes); X1 ya apunta a los 14 bytes de `Hello, World!\n`. `stepi` ejecuta una instrucción adicional. Las direcciones concretas pueden variar. Al hacer `detach`, QEMU continúa, imprime el mensaje y termina. Usa el puerto de depuración solo en un entorno de laboratorio controlado.

En una Raspberry Pi con Linux de 64 bits utiliza `Makefile.arm64`, `readelf`, `objdump` y `gdb` nativos. La ejecución física sigue pendiente.

[Índice general](../README.md) · [Pruebas](../pruebas/README.md).
