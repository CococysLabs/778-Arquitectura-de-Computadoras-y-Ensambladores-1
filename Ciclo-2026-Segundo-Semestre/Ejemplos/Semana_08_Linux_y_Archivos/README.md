# Semana 08: Linux y archivos

Filas 45–50: SVC, syscalls AArch64 y read/write/openat/exit. Fuente: `5_Diseño_Curricular.xlsx`, hoja `Diseño`, `C5`: Segundo Semestre 2026.

| Archivo | Qué enseña |
| --- | --- |
| [03_read_file.s](ARM64/03_read_file.s) | Copia el archivo de datos por bloques, incluido el centinela $. |
| [04_process_buffer.s](ARM64/04_process_buffer.s) | Recorre el contenido hasta $ o EOF. |
| [09_read_input.s](ARM64/09_read_input.s) | Lee stdin por bloques de hasta 64 bytes, hasta EOF. |
| [08_read_numbers.s](ARM64/08_read_numbers.s) | Rutina auxiliar de apertura, lectura y conversión de una columna de enteros. |

## Ejecución

Abre la raíz `Ejemplos/`, instala los requisitos de la [guía ARM64](../documentacion/arm64.md) y ejecuta:

```bash
make -f Makefile.qemu SRC=Semana_08_Linux_y_Archivos/ARM64/03_read_file.s run
```

En Linux AArch64 nativo utiliza `Makefile.arm64` en el mismo comando. Cambia `SRC` por otro ejecutable de la tabla. Los auxiliares sin `_start` no se ejecutan solos: sus contratos y pruebas están en la guía común.

Los lectores usan una sola copia de [datos sintéticos](../datos/lecturas.csv), con ruta relativa a `Ejemplos/`. El ejemplo de pila consume los auxiliares de las semanas 06 y 08; esto no implica interoperabilidad con C.

Consulta las [pruebas](../pruebas/README.md), el [estado de validación](../documentacion/interna/VALIDACION.md) y el [índice general](../README.md). La ejecución física en Raspberry Pi sigue pendiente.
