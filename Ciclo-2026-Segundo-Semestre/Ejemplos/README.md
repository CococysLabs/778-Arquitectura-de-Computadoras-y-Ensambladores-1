# Ejemplos del curso 778 — Segundo semestre de 2026

Ejemplos publicados organizados por su correspondencia con `5_Diseño_Curricular.xlsx`, hoja **Diseño**, celda **C5: Segundo Semestre 2026**, rango **B9:H68**. Se utiliza el número de semana de la columna H; no la etiqueta inconsistente de la hoja Resumen ni los meses de otras planificaciones.

| Semana | Contenido | Correspondencia en Diseño |
| --- | --- | --- |
| [03: Entorno ARM64](Semana_03_Entorno_ARM64/README.md) | Hello World, toolchain GNU, QEMU, Make y GDB. | Filas 15–20 |
| [06: Control de flujo y funciones](Semana_06_Control_Flujo_y_Funciones/README.md) | If, while, menú y conversiones como rutinas reutilizables. | Filas 33–38 |
| [07: Funciones y pila](Semana_07_Funciones_y_Pila/README.md) | Suma/resta, vector en pila y preservación de registros. | Filas 39–42 |
| [08: Linux y archivos](Semana_08_Linux_y_Archivos/README.md) | Archivos, buffers, entrada estándar y lector numérico. | Filas 45–50 |
| [10: GPIO y periféricos](Semana_10_GPIO_y_Perifericos/README.md) | LED, pulsadores, PWM, DHT11, LCD, HC-SR04 y ADC mediante Python. | Filas 57–62; apoyo práctico de E/S |

[Recursos complementarios](Recursos_Complementarios/README.md): temporización con hilos/Timer, MQTT y MongoDB. Se conservan sin atribuirles una correspondencia semanal que el temario no establece. No se crean semanas vacías ni ejemplos nuevos para cubrir temas ausentes.

## Preparación y ejecución

Abre **esta carpeta `Ejemplos/`** en la terminal y en VS Code. Todos los comandos de ejecución parten de esta raíz.

- [ARM64](documentacion/arm64.md): requisitos, comandos, contratos de auxiliares, resultados y depuración. Los dos Makefiles son comunes; `SRC` selecciona el programa semanal y `build/` conserva su ruta.
- [Python](documentacion/python.md): índice de los diez grupos. Usa una sola configuración `pyproject.toml`, `uv.lock`, `.python-version` y `.venv/`; instala solo los extras necesarios.
- [Entorno Python](documentacion/preparar_entorno.md) y [conexiones GPIO](documentacion/gpio_y_sensores.md): requisitos y límites eléctricos.
- [Pruebas](pruebas/README.md) y [validación](VALIDACION.md): comandos reproducibles y alcance real de cada comprobación.

La rutina [io.s](compartidos/ARM64/io.s) y los [datos sintéticos](datos/lecturas.csv) tienen una sola copia compartida. Las otras rutinas se conservan en la semana donde se estudian y los Makefiles resuelven sus inclusiones.

## Conservación y procedencia

Se conservan 24 programas Python, dos módulos auxiliares y ocho programas ARM64 con cuatro archivos de rutinas auxiliares. Los identificadores originales de los ejemplos no representan semanas.

Consulta las [atribuciones](ATRIBUCIONES.md), el [inventario histórico Python](INVENTARIO_PYTHON.md) y su [registro histórico](REGISTRO_PYTHON.md). Sus resultados previos no sustituyen las verificaciones de esta reorganización, documentadas en VALIDACION.

La ejecución física en Raspberry Pi, sensores y calibración sigue pendiente. No se incluyen soluciones de evaluación ni proyectos completos.
