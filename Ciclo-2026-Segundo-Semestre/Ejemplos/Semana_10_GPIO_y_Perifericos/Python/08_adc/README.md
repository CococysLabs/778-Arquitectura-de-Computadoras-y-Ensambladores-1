# Conversión analógica: ADS1115 y PCF8591

## Objetivo y funcionamiento

Leer señales analógicas con dos conversores I²C y distinguir código digital y tensión.

Para el segundo conversor: `uv run --locked --extra hardware Semana_10_GPIO_y_Perifericos/Python/08_adc/pcf8591.py`. El ADS1115 usa los parámetros por defecto de la biblioteca declarada; documenta cualquier cambio de ganancia realizado durante la práctica.

## Requisitos

Pi 3/4, ADS1115 o PCF8591 y fuente analógica dentro del rango permitido por la ficha del conversor. Consulta [preparación y versiones](../../../documentacion/preparar_entorno.md). La ejecución física en Pi 3/4 está pendiente de comprobación; la sintaxis y las pruebas con dobles no acreditan compatibilidad eléctrica.

## Conexiones físicas

Desconecta la alimentación antes de modificar conexiones.

| Señal | Raspberry Pi |
| --- | --- |
| SDA | GPIO2, pin físico 3 |
| SCL | GPIO3, pin físico 5 |
| GND | GND, pin físico 6 |
| VDD/VCC del módulo compatible | 3,3 V, pin físico 1 |
| Entrada del ADS1115 | A3 |
| Entrada del PCF8591 | A0 |

Usa un conversor a la vez: ambos ejemplos asumen dirección `0x48`. Verifica que el módulo funciona a 3,3 V y que ninguna línea I²C tiene pull-up a 5 V. No sobrepases los límites de entrada aunque la escala programable del ADS1115 sea mayor que VDD.

## Instalación

Desde `Ejemplos/`:

```bash
uv sync --locked --extra hardware
```

Instala también los requisitos del sistema descritos en la [guía del entorno](../../../documentacion/preparar_entorno.md).

## Ejecución

Desde `Ejemplos/`:

```bash
uv run --locked --extra hardware Semana_10_GPIO_y_Perifericos/Python/08_adc/ads1115.py
```

Usa Ctrl+C para detener los bucles. Los ejemplos cierran o liberan sus recursos al terminar.

## Resultados esperados

ADS1115 imprime la tensión y el código de A3 cada segundo. PCF8591 imprime el código de A0, entre 0 y 255; se descarta el dato de la conversión anterior antes de leer el actual.

## Limitaciones

El código digital del ADS1115 procede de la representación que entrega la biblioteca y no equivale a los 8 bits del PCF8591. La tensión del PCF8591 requeriría conocer su referencia; este ejemplo no la estima.

## Problemas frecuentes

Si no aparece el dispositivo, activa I²C y comprueba dirección y alimentación. Una lectura saturada exige revisar la tensión de entrada y la ganancia. Un valor PCF8591 no es una medición en voltios.

## Comprobación

Contrasta los resultados con el circuito real. Consulta las [pruebas de lógica](../../../pruebas/README.md) y el [registro de validación](../../../documentacion/interna/REGISTRO_PYTHON.md) para distinguir resultados comprobados y pendientes.
