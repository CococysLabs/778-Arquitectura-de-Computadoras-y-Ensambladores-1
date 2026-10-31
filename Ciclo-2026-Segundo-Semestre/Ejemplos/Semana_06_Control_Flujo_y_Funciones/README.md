# Semana 06: Control de flujo y funciones

Comparaciones, branches, ciclos, llamadas y modularización.

| Archivo | Qué enseña |
| --- | --- |
| [01_if.s](ARM64/01_if.s) | Comparación y bifurcación; muestra la rama para el valor 5. |
| [02_while.s](ARM64/02_while.s) | Ciclo hasta 100; inspecciona x0 en finWhile con GDB. |
| [10_select_menu.s](ARM64/10_select_menu.s) | Selección de opciones, validación de líneas y EOF. |
| [05_atoi.s](ARM64/05_atoi.s) | Rutina auxiliar de conversión decimal a entero con límites. |
| [06_itoa.s](ARM64/06_itoa.s) | Rutina auxiliar de conversión de entero a texto y contrato de buffer. |

## Ejecución

Abre la raíz `Ejemplos/`, instala los requisitos de la [guía ARM64](../documentacion/arm64.md) y ejecuta:

```bash
make -f Makefile.qemu SRC=Semana_06_Control_Flujo_y_Funciones/ARM64/01_if.s run
```

En Linux AArch64 nativo utiliza `Makefile.arm64` en el mismo comando. Cambia `SRC` por otro ejecutable de la tabla. Los auxiliares sin `_start` no se ejecutan solos: sus contratos están en la guía común.

El menú usa las rutinas comunes de E/S; las conversiones se estudian como funciones reutilizables.

[Índice general](../README.md).
