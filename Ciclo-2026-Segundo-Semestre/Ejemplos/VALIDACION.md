# Validación de los ejemplos Python y ARM64

Referencia del curso: `0d0fe4b1729b3a429f5343e897a7f24a7b080114`.
Origen: `2efa6ebe56a2d74e59c16bf6cf2bbe1050c8ca96`.
Fecha de comprobación: 27 de octubre de 2026.

## Resultados comprobados

| Comprobación | Estado | Evidencia y alcance |
| --- | --- | --- |
| Conservación de Python | Verificado correctamente | Los 51 archivos de la etapa anterior se conservaron en el primer commit de esta rama, con respaldo y manifiesto SHA-256. No se repitieron ni modificaron sus correcciones de código. |
| Lógica Python | Verificado correctamente | 19 pruebas aprobadas nuevamente en el entorno final, Python 3.13.17. Los dobles no son lecturas de hardware. |
| MQTT y MongoDB locales | Verificado correctamente | Cuatro pruebas reales aprobadas en la etapa Python, cuyo código se conserva. Incluyen publicación/suscripción, MQTT 5 y documentos sintéticos persistidos. No se repitieron servicios sin cambios. Véase el [registro original](REGISTRO_PYTHON.md). |
| Dependencias Python | Verificado parcialmente | `uv pip check` comprueba 22 paquetes instalados. Las versiones e importaciones se comprobaron en x86-64; GPIO exige Raspberry Pi. PyMongo mantiene su advertencia de obsolescencia documentada. |
| Construcción ARM64 | Verificado correctamente | Ocho programas ensamblados y enlazados mediante Make y GNU Binutils 2.42. Los auxiliares se incluyen en sus programas; Make rechaza ejecutarlos por separado. |
| Ejecución ARM64 | Verificado correctamente | QEMU 8.2.2 ejecuta los ocho programas. Se comprueban resultados y errores, no solo la creación del ELF. |
| Pruebas ARM64 | Verificado correctamente | 15 pruebas aprobadas, incluida sesión GDB real. Subcasos: ambas ramas de if, archivos vacíos/binarios/múltiples bloques, error al abrir/leer, centinela, EOF, líneas largas, menú, conversiones, capacidad y desbordamientos. |
| Registros y pila | Verificado correctamente | Harness AArch64 comprueba preservación x19-x29 y SP en `atoi`, `itoa` y lector; también límites del buffer de conversión y capacidad del vector. |
| GDB CLI | Verificado correctamente | Sesión real GDB 15.1 con QEMU: breakpoint en `finWhile`, contador x0=100, detach y finalización correcta. |
| Makefiles | Verificado parcialmente | Construcción cruzada, rechazo de auxiliares, dependencias de inclusiones y dry-run nativo correctos; ejecución nativa física pendiente. |
| Sintaxis y Markdown | Verificado correctamente | Compilación Python en memoria y comprobación de enlaces relativos/anclas mediante `pruebas/verificar_repositorio.py`. |
| Alcance, exclusiones y credenciales | Verificado parcialmente | Diff limitado a la carpeta autorizada; sin material evaluado, imágenes, ELF, objetos ni entornos en el aporte. Escaneo de patrones sin credenciales detectadas; no es una auditoría del historial completo. |

No quedan pruebas ejecutadas fallidas pendientes de corrección. Una prueba omitida por falta de herramientas o de activación explícita no equivale a aprobada.

## Pendientes importantes

- **Pendiente por dependencia de hardware o servicios externos:** ejecución física en Pi 3/4, instalación de dependencias ARM64, cableado, sensores y calibración del servo.
- **Verificado parcialmente:** perfiles F5, Remote-SSH y StackScope documentados; su interfaz gráfica no se verificó. La sesión CLI GDB/QEMU sí se ejecutó.
- **Pendiente por dependencia de hardware o servicios externos:** Atlas, DNS SRV, TLS y autenticación de servicios externos; las integraciones realizadas son locales.
- **Verificado parcialmente:** autoría del código propio y procedencia registradas; licencia institucional y aprobación académica siguen pendientes. No impiden conservar la rama para revisión, ni equivalen a autorización de merge.

## Alcance e inventario final

Python conserva 24 programas y dos módulos auxiliares en diez temas. ARM64 incorpora ocho programas, tres auxiliares adaptados y un auxiliar nuevo de entrada/salida.

| Original ARM64 | Destino o decisión |
| --- | --- |
| `00_hello_world.s`, `01_if.s`, `02_while.s` | Mismos nombres en `ARM64/src/`. |
| `03_read_file.s`, `04_process_buffer.s` | Lectura por bloques y errores; mismos nombres. |
| `05_atoi.s`, `06_itoa.s` | Conversiones acotadas; contratos en README. |
| `07_rutina.s` | `07_sum_and_subtract.s`. |
| `08_utils.s` | `08_read_numbers.s`. |
| `09_read_input.s`, `10_select_menu.s`, `lecturas.csv` | Mismos nombres; EOF y menú corregidos. |
| Makefiles y cuatro configuraciones VS Code | Adaptados o conservados bajo `ARM64/`. |
| `11_practica.s`, parciales 12–15, tarea 16, shell 17–19 | Excluidos. |
| `io.s`, `pruebas/test_arm64.py` | Nuevos auxiliares y pruebas. |

No hay cambios fuera de `Ciclo-2026-Segundo-Semestre/Ejemplos/`. Los archivos históricos de inventario y registro Python describen su primera etapa; este documento describe el conjunto actual.

## Reproducir verificaciones

Desde `pruebas/`:

```bash
../Python/.venv/bin/python -m unittest -v test_python
python3.13 -m unittest -v test_arm64
PRUEBAS_GDB=1 python3.13 -m unittest -v test_arm64
python3.13 verificar_repositorio.py
```

Las pruebas de servicios requieren activación y contenedores locales según [pruebas/README.md](pruebas/README.md). Las pruebas ARM64 usan directorios temporales y no sobrescriben `ARM64/src/lecturas.csv`.

## Revisión institucional

La rama se prepara para revisión, sin modificar `main` ni crear un PR automáticamente. Cuando el titular decida abrirlo, debe indicar las pruebas realizadas y los pendientes, revisar las [atribuciones](ATRIBUCIONES.md) y solicitar revisión del equipo CODEOWNERS de esta ruta. La integración debe cumplir las aprobaciones institucionales.
