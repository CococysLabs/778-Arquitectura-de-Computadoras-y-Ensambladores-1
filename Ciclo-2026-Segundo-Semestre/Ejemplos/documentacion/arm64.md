# Ensamblador AArch64 en Linux

Ejemplos del curso 778 sobre registros, bifurcaciones, buffers, entrada/salida, conversiones y pila. Se ejecutan con syscalls Linux AArch64, sin enlazar libc. Los nombres son convenciones propuestas para este conjunto, no requisitos institucionales demostrados.

## Requisitos e instalación

En Debian/Ubuntu x86-64, para compilación cruzada y emulación:

```bash
sudo apt update
sudo apt install make binutils-aarch64-linux-gnu qemu-user gdb-multiarch
```

Se verificó con GNU Binutils 2.42, QEMU 8.2.2 y GDB 15.1. No hace falta Raspberry Pi para ejecutar estos ejemplos en QEMU.

En Raspberry Pi 3/4 con sistema Linux de 64 bits:

```bash
sudo apt install make binutils gdb
uname -m
```

El sistema debe informar `aarch64`. La ejecución nativa en Raspberry Pi física sigue pendiente; no se deduce de la prueba emulada. No se requieren conexiones GPIO ni periféricos.

## Compilación y ejecución

Ejecuta todos los comandos **desde la raíz `Ejemplos/`**:

```bash
make -f Makefile.qemu SRC=Semana_03_Entorno_ARM64/ARM64/00_hello_world.s run
```

En una Raspberry Pi de 64 bits:

```bash
make -f Makefile.arm64 SRC=Semana_03_Entorno_ARM64/ARM64/00_hello_world.s run
```

Cambia `SRC` por uno de los trece programas del índice. Los Makefiles rechazan las rutinas auxiliares como programas independientes. El archivo por defecto es `Semana_03_Entorno_ARM64/ARM64/00_hello_world.s`.

El ensamblador genera un objeto con símbolos de depuración, el enlazador produce un ELF y QEMU lo ejecuta. Objetos, ejecutables y dependencias quedan en `build/Semana_XX_Tema/ARM64/`, excluido de Git. Los archivos `.d` registran las inclusiones para reconstruir cuando cambia una rutina.

## Programas ejecutables

| Programa | Objetivo y entrada | Resultado esperado |
| --- | --- | --- |
| `Semana_03_Entorno_ARM64/ARM64/00_hello_world.s` | Escribir un mensaje con una syscall | `Hello, World!` y salto de línea; código 0. |
| `Semana_04_Registros_e_Instrucciones_A64/ARM64/01_registros.s` | X/W, MOVZ/MOVK y XZR | X9=42, X10=0x123456789abcdef0 y X11=0 en `resultados`. |
| `Semana_04_Registros_e_Instrucciones_A64/ARM64/02_aritmetica.s` | Aritmética de 20 y 6; suma con overflow con signo | 26, 14, 120, 3 y 3; NZCV=1001. |
| `Semana_04_Registros_e_Instrucciones_A64/ARM64/03_logica_y_desplazamientos.s` | Lógica, máscaras y desplazamientos | AND=0A, OR=AF, XOR=A5, BIC=A0, LSL=154, LSR=55 (hex); ASR=-4. |
| `Semana_05_Memoria_y_Direccionamiento/ARM64/01_memoria_y_offsets.s` | LDR/STR, arreglo, offsets y extensión | Arreglo `[10, 25, 30, 40]`; byte sin signo 251 y con signo -5. |
| `Semana_05_Memoria_y_Direccionamiento/ARM64/02_pre_post_indexing.s` | Lectura/escritura con actualización de base | Arreglo `[10, 20, 77, 40]`; offsets guardados 8, 16, 24 y final 16. |
| `Semana_06_Control_Flujo_y_Funciones/ARM64/01_if.s` | Comparar un entero con 10; valor inicial 5 | `x es menor o igual que 10`. Al cambiar el valor a 11, muestra la rama mayor. |
| `Semana_06_Control_Flujo_y_Funciones/ARM64/02_while.s` | Incrementar un registro hasta 100 | Sin texto; en `finWhile`, antes del cierre, x0 vale 100. Código 0. |
| `Semana_08_Linux_y_Archivos/ARM64/03_read_file.s` | Copiar `datos/lecturas.csv` por bloques de 4096 bytes | Reproduce todos los bytes, incluido `$`; un archivo vacío no imprime datos. |
| `Semana_08_Linux_y_Archivos/ARM64/04_process_buffer.s` | Recorrer bytes hasta el primer `$` o EOF | Imprime lo anterior a `$`; sin centinela procesa hasta EOF. |
| `Semana_07_Funciones_y_Pila/ARM64/07_sum_and_subtract.s` | Leer una columna numérica y recorrer un vector reservado en pila | Con los datos incluidos: `Suma: 150` y `Resta: -150`. |
| `Semana_08_Linux_y_Archivos/ARM64/09_read_input.s` | Leer stdin por bloques de hasta 64 bytes | Muestra cada bloque recibido sin añadir bytes del buffer; termina en EOF. |
| `Semana_06_Control_Flujo_y_Funciones/ARM64/10_select_menu.s` | Seleccionar una opción por línea: 1, 2 o 3 | 1 imprime `Hola`, 2 `Mundo`, 3 `Adiós` y termina. Rechaza otras entradas. EOF termina. |

Los mensajes de error se escriben en stderr. Los fallos de entrada/salida terminan con código 1; el programa numérico utiliza código 2 para archivo inválido, tamaño/capacidad excedidos o desbordamiento.

### Lectura de archivo y acumulación

`datos/lecturas.csv` contiene datos sintéticos, una sola columna de enteros:

```text
10
20
30
40
50
$
```

Ejecuta:

```bash
make -f Makefile.qemu SRC=Semana_08_Linux_y_Archivos/ARM64/03_read_file.s run
make -f Makefile.qemu SRC=Semana_08_Linux_y_Archivos/ARM64/04_process_buffer.s run
make -f Makefile.qemu SRC=Semana_07_Funciones_y_Pila/ARM64/07_sum_and_subtract.s run
```

La extensión CSV se conserva del origen; no se admiten comas ni varias columnas en el lector numérico. Este lector acepta enteros de 0 a 9223372036854775807, saltos LF/CRLF y líneas vacías. El `$` final es opcional y puede seguir inmediatamente al último número; después solo se permiten saltos de línea. No acepta signos, espacios ni caracteres no numéricos en una entrada.

El límite del archivo numérico es **4096 bytes**, comprobado antes de convertir, y el vector admite **2048 enteros** de ocho bytes. No hay truncamiento silencioso: los excesos y el desbordamiento de la suma se informan como error. Una entrada vacía produce suma y resta iguales a cero.

Los ejemplos 03 y 04 procesan múltiples bloques y no tienen el límite total de 4096 bytes del lector numérico.

### Teclado y menú

```bash
make -f Makefile.qemu SRC=Semana_08_Linux_y_Archivos/ARM64/09_read_input.s run
make -f Makefile.qemu SRC=Semana_06_Control_Flujo_y_Funciones/ARM64/10_select_menu.s run
```

Para proporcionar varias opciones en una tubería sin mezclar la salida de Make con la del programa:

```bash
make -f Makefile.qemu SRC=Semana_06_Control_Flujo_y_Funciones/ARM64/10_select_menu.s
printf '9\n1\n2\n3\n' | qemu-aarch64 build/Semana_06_Control_Flujo_y_Funciones/ARM64/10_select_menu
```

La opción 9 debe rechazarse. El menú valida toda la línea; `12` no equivale a opción 1. Una línea que exceda 64 bytes se consume y se rechaza completa. Se acepta CRLF. En una terminal Linux, Ctrl+D sobre una línea vacía indica EOF; Ctrl+C interrumpe el proceso.

El ejemplo 09 muestra bloques de bytes, no implementa edición ni delimitación de líneas. Una entrada larga puede repartirse en varios bloques y un carácter UTF-8 puede quedar dividido entre ellos.

Los cinco ejemplos nuevos de semanas 04 y 05 terminan sin imprimir texto; sus resultados se inspeccionan en la etiqueta `resultados`. Consulta [semana 04](../Semana_04_Registros_e_Instrucciones_A64/README.md) y [semana 05](../Semana_05_Memoria_y_Direccionamiento/README.md). Para ensamblar, inspeccionar ELF y practicar GDB desde cero, sigue [semana 03](../Semana_03_Entorno_ARM64/README.md).

## Rutinas auxiliares e interfaces

Estos archivos no tienen `_start` y se incluyen mediante `.include`; no deben compilarse como ejecutables independientes.

| Rutina | Entrada | Salida y efectos |
| --- | --- | --- |
| `05_atoi.s: atoi` | x0=inicio, x1=fin exclusivo de bytes | x0=valor, x1=primer byte sin consumir, x2=0 o -1. Consume dígitos, no el separador. Rechaza vacío y desbordamiento. Modifica x0-x7. |
| `06_itoa.s: itoa` | x0=entero con signo, x1=fin exclusivo, x2=inicio del buffer | x0=0 o -1; si funciona, x1=inicio del texto y x2=longitud. Admite INT64_MIN, no añade NUL. En fallo puede dejar texto parcial dentro del buffer. Modifica x0-x7. |
| `08_read_numbers.s: read_numbers` | x0=vector del llamador, x1=capacidad en enteros | x0=cantidad o error negativo. El vector puede quedar parcialmente escrito si falla; el llamador no debe usarlo entonces. Modifica x0-x8. |
| `io.s: write_all` | x0=descriptor, x1=buffer, x2=bytes | x0=0 o errno negativo. Completa escrituras parciales y reintenta EINTR. Modifica x0-x3/x8. |
| `io.s: read_retry` | x0=descriptor, x1=buffer, x2=capacidad | x0=bytes, 0=EOF o errno negativo. Reintenta EINTR; conserva x1/x2. Modifica x0/x3/x8. |
| `io.s: read_line` | x0=buffer, x1=capacidad | x0=longitud sin salto final, -1=error, -2=exceso; x1 indica si se encontró EOF. No añade NUL. Modifica x0-x3/x8. |

Las rutinas que retornan preservan x19-x29 y SP, manteniendo la alineación de pila de 16 bytes. Las rutinas anidadas conservan x30. El vector numérico se reserva y libera en el llamador, sin devolver un puntero a una pila liberada.

`read_numbers` devuelve -1 al fallar la apertura, -2 al leer/cerrar, -3 por archivo excesivo, -4 por formato o desbordamiento y -5 por capacidad del vector. Su llamador agrupa estos casos en un diagnóstico y código de salida 2.

## Depuración con GDB

Primero compila y después, en una terminal:

```bash
make -f Makefile.qemu SRC=Semana_06_Control_Flujo_y_Funciones/ARM64/02_while.s
qemu-aarch64 -g 1234 build/Semana_06_Control_Flujo_y_Funciones/ARM64/02_while
```

En otra terminal, desde `Ejemplos/`:

```bash
gdb-multiarch build/Semana_06_Control_Flujo_y_Funciones/ARM64/02_while
```

Dentro de GDB:

```text
set architecture aarch64
target remote localhost:1234
break finWhile
continue
print /d $x0
info registers sp pc x30
detach
quit
```

El contador debe mostrar 100 antes de que el programa ponga x0 a cero para salir. El puerto de depuración carece de autenticación: úsalo solo en un entorno de laboratorio controlado, sin exponerlo a redes externas.

Los perfiles incluidos en `.vscode/` son opcionales. Para utilizarlos, abre la raíz `Ejemplos/` como carpeta de VS Code y selecciona un archivo ejecutable. El perfil nativo requiere abrir esa carpeta mediante Remote-SSH en la Pi. F5, StackScope y la depuración nativa física siguen pendientes de comprobación visual; la sesión CLI QEMU/GDB sí se verificó.

## Problemas frecuentes

- Archivo no encontrado: inicia desde `Ejemplos/`; las rutas son relativas al directorio de ejecución.
- `Exec format error`: usa QEMU en x86-64 o un sistema nativo AArch64 de 64 bits.
- Rutina sin `_start`: selecciona un programa del índice, no un auxiliar.
- Puerto 1234 ocupado: termina la sesión anterior antes de iniciar otra.
- Error numérico: revisa formato, límite de 4096 bytes y rango; no se aceptan negativos como entrada aunque la resta produzca un resultado negativo.
- Salida redirigida no disponible: se informa error en lugar de presentar datos incompletos como correctos.

## Limpiar compilaciones

```bash
make -f Makefile.qemu clean
```

Elimina únicamente los resultados de compilación de `build/` con la configuración predeterminada. No se incluyen binarios en el repositorio.
