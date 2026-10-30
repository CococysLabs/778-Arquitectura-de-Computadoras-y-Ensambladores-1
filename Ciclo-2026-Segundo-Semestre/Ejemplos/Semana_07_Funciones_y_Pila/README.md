# Semana 07: Funciones y pila

Filas 39–42: SP, alineación, marcos, parámetros y preservación de registros. Fuente: `5_Diseño_Curricular.xlsx`, hoja `Diseño`, `C5`: Segundo Semestre 2026.

| Archivo | Qué enseña |
| --- | --- |
| [07_sum_and_subtract.s](ARM64/07_sum_and_subtract.s) | Reserva un vector en pila y llama rutinas; produce Suma: 150 y Resta: -150. |

## Ejecución

Abre la raíz `Ejemplos/`, instala los requisitos de la [guía ARM64](../documentacion/arm64.md) y ejecuta:

```bash
make -f Makefile.qemu SRC=Semana_07_Funciones_y_Pila/ARM64/07_sum_and_subtract.s run
```

En Linux AArch64 nativo utiliza `Makefile.arm64` en el mismo comando. Cambia `SRC` por otro ejecutable de la tabla. Los auxiliares sin `_start` no se ejecutan solos: sus contratos y pruebas están en la guía común.

Los lectores usan una sola copia de [datos sintéticos](../datos/lecturas.csv), con ruta relativa a `Ejemplos/`. El ejemplo de pila consume los auxiliares de las semanas 06 y 08; esto no implica interoperabilidad con C.

Consulta las [pruebas](../pruebas/README.md), el [estado de validación](../documentacion/interna/VALIDACION.md) y el [índice general](../README.md). La ejecución física en Raspberry Pi sigue pendiente.
