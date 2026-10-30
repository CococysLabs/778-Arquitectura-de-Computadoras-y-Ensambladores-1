# Semana 02: fundamentos de arquitectura

Apoyo a representación de datos: fila 14 de `5_Diseño_Curricular.xlsx`, hoja `Diseño`, periodo Segundo Semestre 2026. Los ejemplos usan solo Python estándar y muestran resultados en terminal.

| Archivo | Qué enseña y resultado esperado |
| --- | --- |
| [01_bases_numericas.py](Python/01_bases_numericas.py) | El decimal 42 equivale a `00101010` en binario y `2A` en hexadecimal; ambas conversiones de regreso producen 42. |
| [02_complemento_a_dos.py](Python/02_complemento_a_dos.py) | Rango de un byte con signo: −128 a 127. `11111011` representa −5 con signo y 251 sin signo. |
| [03_operaciones_bits.py](Python/03_operaciones_bits.py) | AND, OR, XOR, borrado con máscara, inversión y desplazamientos. Con `AA` y `0F`: AND=`0A`, OR=`AF`, XOR=`A5`, borrado=`A0`. |
| [04_bytes_endianness.py](Python/04_bytes_endianness.py) | `0x12345678` ocupa `78 56 34 12` en little-endian y `12 34 56 78` en big-endian. Al recuperar el valor con el mismo orden, ambos producen el original. |

## Ejecución

Desde la raíz `Ejemplos/`, con Python 3.13; no requiere hardware ni instalar extras:

```bash
python3.13 Semana_02_Fundamentos_Arquitectura/Python/01_bases_numericas.py
python3.13 Semana_02_Fundamentos_Arquitectura/Python/02_complemento_a_dos.py
python3.13 Semana_02_Fundamentos_Arquitectura/Python/03_operaciones_bits.py
python3.13 Semana_02_Fundamentos_Arquitectura/Python/04_bytes_endianness.py
```

Python no limita sus enteros a ocho bits: la máscara `& 0xFF` lo hace explícitamente. Por eso `AA << 1` produce 340 (`154` hexadecimal), mientras que al conservar solo ocho bits queda `54`. El desplazamiento de −8 a la derecha produce −4. Los offsets de bytes son posiciones conceptuales, no direcciones físicas.

Para comprobar resultados: `python3.13 -m unittest discover -s pruebas -p test_fundamentos.py -v`.

[Índice general](../README.md) · [Pruebas](../pruebas/README.md).
