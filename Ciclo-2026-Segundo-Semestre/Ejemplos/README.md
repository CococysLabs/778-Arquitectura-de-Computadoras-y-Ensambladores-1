# Ejemplos del curso 778 — Segundo semestre de 2026

Recursos de clase para estudiar interfaces de entrada/salida con Python y programación en ensamblador AArch64. Cada bloque documenta requisitos, ejecución y resultados esperados.

| Bloque | Contenido | Entorno |
| --- | --- | --- |
| [Python](Python/README.md) | GPIO, pulsadores, PWM, temporización, DHT11, LCD, HC-SR04, ADC, MQTT y MongoDB | Python 3.13; los circuitos requieren Pi 3/4 y los ejemplos de comunicación requieren servicios. |
| [ARM64](ARM64/README.md) | Mensajes, bifurcaciones, bucles, archivos, conversiones, pila, entrada estándar y menú | GNU assembler y Linux AArch64 nativo o QEMU. |
| [Pruebas](pruebas/README.md) | Verificaciones de lógica, servicios, ensamblado, ejecución y depuración | Herramientas indicadas en cada bloque. |

## Primeros pasos

1. Abre el README del lenguaje que utilizarás.
2. Instala solo sus requisitos y respeta el directorio de ejecución indicado.
3. Comprueba conexiones y límites eléctricos antes de alimentar un circuito.
4. Contrasta la salida con el resultado esperado y distingue datos sintéticos de mediciones.
5. Revisa los estados de comprobación en [VALIDACION.md](VALIDACION.md).

Los nombres y la numeración son convenciones propuestas para este conjunto, sin atribuirles obligatoriedad institucional. Los identificadores no representan semanas del semestre.

## Estado y procedencia

Las pruebas disponibles de lógica, servicios locales y ejecución AArch64 se registran con su alcance real. Las pruebas físicas en Raspberry Pi y la calibración de periféricos siguen pendientes; no se presentan como verificadas.

Consulta [atribuciones y permisos](ATRIBUCIONES.md), el [inventario de Python](INVENTARIO_PYTHON.md) y la [documentación de ARM64](ARM64/README.md). El inventario y registro Python conservan el alcance histórico de su primera etapa; la validación actual del conjunto está en [VALIDACION.md](VALIDACION.md).

Se excluyen soluciones de exámenes, tareas evaluadas, prácticas resueltas, proyecto completo, shell reservado e imágenes sin atribución comprobada.
