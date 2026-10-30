# Validación de semanas 02–05 — 30 de octubre de 2026

Continuación de la rama `feature/organizar-ejemplos-semanas-2s2026` desde `c4907d02853f04596273f0e4c253db949332f2c7`. Fuente curricular: `5_Diseño_Curricular.xlsx`, hoja `Diseño`, C5: Segundo Semestre 2026; filas 9–32 para semanas 02–05.

## Resultados vigentes

| Comprobación | Resultado y alcance |
| --- | --- |
| Suite completa | **47 pruebas aprobadas, cero fallos y cero omisiones**: 4 de fundamentos, 19 de lógica Python existente, 20 ARM64 y 4 con servicios reales. |
| Semana 02 | Cuatro programas Python ejecutados: bases, complemento a dos, bits y endianness. Se verifica su salida, incluidos −128, −5, 0 y 127 en ocho bits. No requieren extras. |
| Semana 03 | Hello World conservado. readelf confirma ELF AArch64 y objdump el símbolo `_start` y SVC. Sesión GDB real con breakpoint, instrucción individual y memoria del mensaje. |
| Semana 04 | Tres programas ensamblados, enlazados y ejecutados con QEMU. GDB comprueba escritura W/X, MOVZ/MOVK, cero, aritmética, NZCV, máscaras y desplazamientos. |
| Semana 05 | Dos programas ejecutados con QEMU. GDB comprueba arreglo modificado, offsets inmediatos/escalados, extensión con y sin signo y actualización de base antes/después del acceso. |
| Regresión | Se repiten todas las pruebas anteriores: buffers, EOF, menú, límites numéricos, pila, registros preservados y reconstrucción de auxiliares. |
| Makefiles | Trece ejecutables admitidos en ambos Makefiles; dry-run nativo de los trece correcto. Las pruebas de dependencias y reconstrucción también se repitieron tras presentar la lista de programas por semana en líneas legibles. |
| Servicios locales | Tres pruebas MQTT reales con Mosquitto 2.0 y una MongoDB 8.0; solo datos sintéticos y base temporal eliminada al terminar. |
| Conservación | 45 archivos funcionales anteriores comparados byte a byte contra `c4907d0`: programas, auxiliares, datos, dependencias y perfiles VS Code. Se conservan sus contenidos. Makefiles y pruebas se amplían para los nuevos ejemplos. |
| Dependencias | Sin cambios en pyproject.toml ni uv.lock. `uv pip check --python .venv/bin/python` comprueba cuatro paquetes sin incompatibilidades. |
| Documentación | Solo README.md permanece como Markdown en la raíz. Inventario, registro y validación histórica se trasladan aquí; atribuciones y guías técnicas quedan en documentacion/. Enlaces comprobados con el verificador existente. |
| Alcance | Cambios limitados a `Ciclo-2026-Segundo-Semestre/Ejemplos/`; sin nuevos ejemplos C, dependencias ni binarios publicados. |

La prueba introductoria de GDB permitió corregir el breakpoint del README: al conectar QEMU ya está detenido al inicio, por lo que se coloca el breakpoint en `*_start+4` para observar X1 después de cargar la dirección del mensaje. La suite completa se repitió tras ese ajuste.

## Reproducir

Desde `Ejemplos/`, prepara los servicios locales según [pruebas/README.md](../../pruebas/README.md):

```bash
PRUEBAS_GDB=1 PRUEBAS_SERVICIOS=1 .venv/bin/python -m unittest discover -s pruebas -v
python3.13 pruebas/verificar_repositorio.py
uv pip check --python .venv/bin/python
git diff --check
```

Entorno conservado: CPython 3.13.17, Linux x86-64, Binutils 2.42, QEMU 8.2.2 y GDB 15.1. PyMongo conserva su advertencia de obsolescencia previamente registrada.

No se verificaron hardware físico, ejecución ARM64 nativa ni interfaz gráfica de VS Code. Las sesiones QEMU/GDB y los dobles GPIO no acreditan funcionamiento de sensores. El inventario y los resultados siguientes describen etapas anteriores; sus cifras no son el total actual.

---

# Validación de la organización semanal — 30 de octubre de 2026

Base publicada: `cd55239b99654e4bd8dff2b40cab67d632a00a92` de `main`.
Fuente curricular: `5_Diseño_Curricular.xlsx`, hoja `Diseño`, `C5`: «Segundo Semestre 2026», rango `B9:H68`. La hoja `Resumen` no se utilizó para clasificar.

## Resultados de esta reorganización

| Comprobación | Resultado y alcance |
| --- | --- |
| Suite completa | **39 pruebas aprobadas, cero fallos y cero omisiones**: 19 de lógica Python, 16 ARM64 y 4 con servicios reales. |
| Conservación de programas | Los 26 archivos educativos Python permanecen idénticos byte a byte. Las 12 fuentes ARM64 conservan su código; solo cambió `src/lecturas.csv` por `datos/lecturas.csv` en tres lectores. Comparación contra la base publicada. |
| Datos y configuración | `lecturas.csv`, `pyproject.toml`, `uv.lock`, `.python-version` y los cuatro JSON de VS Code conservan su contenido. Se reubicaron para usar una sola raíz. |
| Dependencias Python | `uv sync --locked --extra mqtt --extra mongodb` correcto; `uv pip check --python .venv/bin/python` comprueba los cuatro paquetes instalados sin incompatibilidades. No se cambiaron versiones. |
| ARM64 con QEMU | Los ocho ejecutables se ensamblan, enlazan y ejecutan; pasan casos de EOF, entrada inválida, buffers, límites y errores de E/S. |
| Pila y auxiliares | Pasan las comprobaciones existentes de SP, x19–x29, conversiones, capacidad y desbordamientos. |
| Makefiles | Rechazan auxiliares como ejecutables, rastrean inclusiones entre semanas y reconstruyen al cambiar cualquiera de los cuatro auxiliares. El Makefile nativo se comprueba mediante dry-run. |
| GDB CLI | Sesión real con QEMU, breakpoint en `finWhile`, x0=100 y cierre correcto. |
| MQTT local | Tres pruebas reales con Mosquitto 2.0: conexión, publicación/suscripción y MQTT 5 con mensaje de otro cliente. |
| MongoDB local | Una prueba real con MongoDB 8.0: conexión, inserción, consulta y simulación. Base aleatoria con datos sintéticos eliminada al terminar. |
| Documentación y VS Code | Rutas de los 18 comandos `uv run` documentados existentes; JSON y rutas base de los perfiles comprobados. Interfaz gráfica no verificada. |
| Sintaxis, enlaces y alcance | Verificador de repositorio y `git diff --check` correctos; cambios limitados a `Ciclo-2026-Segundo-Semestre/Ejemplos/`. Sin entornos, objetos ni binarios en el aporte. |

Entorno: Linux x86-64, CPython 3.13.17, GNU Binutils 2.42, QEMU 8.2.2 y GDB 15.1. PyMongo 3.12.0 mantiene su advertencia de obsolescencia ya documentada; las pruebas pasan sin ocultarla.

Las comprobaciones iniciales dentro del aislamiento encontraron dependencias ausentes y una restricción de sockets. Se instalaron los extras bloqueados y se repitió la suite completa con acceso a los servicios locales y GDB. Los dos contenedores de prueba se detuvieron al finalizar.

## Reproducir

Desde la raíz `Ejemplos/`, prepara los servicios desechables como indica [pruebas/README.md](../../pruebas/README.md) y ejecuta:

```bash
uv sync --locked --extra mqtt --extra mongodb
PRUEBAS_GDB=1 PRUEBAS_SERVICIOS=1 .venv/bin/python -m unittest discover -s pruebas -v
python3.13 pruebas/verificar_repositorio.py
uv pip check --python .venv/bin/python
git diff --check
```

Los tests usan datos temporales y no sobrescriben `datos/lecturas.csv`. Para omitir integraciones locales no actives `PRUEBAS_SERVICIOS`; las omisiones no equivalen a pruebas aprobadas.

## Límites de esta comprobación

No se verificaron Raspberry Pi física, periféricos, calibración del servo ni ejecución ARM64 nativa. Tampoco la interfaz F5/Remote-SSH/StackScope, Atlas, DNS SRV, TLS o autenticación externa. Los dobles GPIO y los datos sintéticos no acreditan mediciones físicas.

La organización contiene solo semanas con correspondencia demostrable: 03, 06, 07, 08 y 10. Hilos/Timer, MQTT y MongoDB quedan en recursos complementarios; no se presentan como integración C+AArch64 de semana 11.

---

Los resultados siguientes pertenecen a la incorporación original. Se conservan como historial, con rutas actualizadas; la validación vigente es la sección superior.

# Registro histórico: incorporación original

Referencia del curso: `0d0fe4b1729b3a429f5343e897a7f24a7b080114`.
Origen: `2efa6ebe56a2d74e59c16bf6cf2bbe1050c8ca96`.
Fecha de comprobación: 27 de octubre de 2026.

## Resultados de la incorporación del 27 de octubre

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
| `00_hello_world.s`, `01_if.s`, `02_while.s` | Mismos nombres, ahora en las semanas 03 y 06. |
| `03_read_file.s`, `04_process_buffer.s` | Lectura por bloques y errores; mismos nombres. |
| `05_atoi.s`, `06_itoa.s` | Conversiones acotadas; contratos en README. |
| `07_rutina.s` | `07_sum_and_subtract.s`. |
| `08_utils.s` | `08_read_numbers.s`. |
| `09_read_input.s`, `10_select_menu.s`, `lecturas.csv` | Mismos nombres; EOF y menú corregidos. |
| Makefiles y cuatro configuraciones VS Code | Ahora compartidos en la raíz `Ejemplos/`. |
| `11_practica.s`, parciales 12–15, tarea 16, shell 17–19 | Excluidos. |
| `io.s`, `pruebas/test_arm64.py` | Nuevos auxiliares y pruebas. |

No hay cambios fuera de `Ciclo-2026-Segundo-Semestre/Ejemplos/`. Los archivos históricos de inventario y registro Python describen su primera etapa; este documento describe el conjunto actual.

## Reproducir verificaciones

Desde la raíz `Ejemplos/`:

```bash
.venv/bin/python -m unittest discover -s pruebas -p test_python.py -v
python3.13 -m unittest discover -s pruebas -p test_arm64.py -v
PRUEBAS_GDB=1 python3.13 -m unittest discover -s pruebas -p test_arm64.py -v
python3.13 pruebas/verificar_repositorio.py
```

Las pruebas de servicios requieren activación y contenedores locales según [pruebas/README.md](../../pruebas/README.md). Las pruebas ARM64 usan directorios temporales y no sobrescriben `datos/lecturas.csv`.

## Revisión institucional

La rama se prepara para revisión, sin modificar `main` ni crear un PR automáticamente. Cuando el titular decida abrirlo, debe indicar las pruebas realizadas y los pendientes, revisar las [atribuciones](../ATRIBUCIONES.md) y solicitar revisión del equipo CODEOWNERS de esta ruta. La integración debe cumplir las aprobaciones institucionales.
