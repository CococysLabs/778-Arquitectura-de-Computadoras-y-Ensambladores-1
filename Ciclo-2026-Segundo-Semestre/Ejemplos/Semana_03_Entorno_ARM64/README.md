# Semana 03: Entorno ARM64

Filas 15–20: Linux, toolchain GNU, QEMU, Makefiles, GDB y ELF. Fuente: `5_Diseño_Curricular.xlsx`, hoja `Diseño`, `C5`: Segundo Semestre 2026.

| Archivo | Qué enseña |
| --- | --- |
| [00_hello_world.s](ARM64/00_hello_world.s) | Mensaje mínimo para recorrer ensamblado, enlace, ejecución y depuración. |

## Ejecución

Abre la raíz `Ejemplos/`, instala los requisitos de la [guía ARM64](../documentacion/arm64.md) y ejecuta:

```bash
make -f Makefile.qemu SRC=Semana_03_Entorno_ARM64/ARM64/00_hello_world.s run
```

En Linux AArch64 nativo utiliza `Makefile.arm64` en el mismo comando. Cambia `SRC` por otro ejecutable de la tabla. Los auxiliares sin `_start` no se ejecutan solos: sus contratos y pruebas están en la guía común.

Consulta las [pruebas](../pruebas/README.md), el [estado de validación](../VALIDACION.md) y el [índice general](../README.md). La ejecución física en Raspberry Pi sigue pendiente.
