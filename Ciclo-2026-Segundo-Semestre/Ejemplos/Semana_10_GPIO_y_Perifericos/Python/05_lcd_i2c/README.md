# LCD 16×2 mediante I²C

## Objetivo y funcionamiento

Escribir texto, distribuir mensajes largos y alternar pantallas en un LCD con adaptador I²C.

También puedes ejecutar `lcd_multiline.py` o `lcd_screens.py` cambiando el nombre en el comando. Las pantallas de ejemplo contienen valores fijos: no son mediciones de sensores.

## Requisitos

Pi 3/4, LCD HD44780 16×2 con adaptador PCF8574 y adaptación de nivel si el módulo trabaja a 5 V. Consulta [preparación y versiones](../../../documentacion/preparar_entorno.md). La ejecución física en Pi 3/4 está pendiente de comprobación; la sintaxis y las pruebas con dobles no acreditan compatibilidad eléctrica.

## Conexiones físicas

Desconecta la alimentación antes de modificar conexiones.

| Señal del adaptador | Raspberry Pi |
| --- | --- |
| SDA, mediante adaptación a 3,3 V cuando corresponda | GPIO2, pin físico 3 |
| SCL, mediante adaptación a 3,3 V cuando corresponda | GPIO3, pin físico 5 |
| GND | GND, pin físico 6 |
| VCC | Según la ficha del módulo y su adaptador |

No conectes a la Pi líneas SDA/SCL con pull-ups a 5 V. Un LCD alimentado a 5 V puede necesitar conversor bidireccional de nivel. Activa I²C y confirma dirección antes de ejecutar; el código usa bus 1 y dirección `0x27`.

## Instalación

Desde `Ejemplos/`:

```bash
uv sync --locked --extra hardware
```

Instala también los requisitos del sistema descritos en la [guía del entorno](../../../documentacion/preparar_entorno.md).

## Ejecución

Desde `Ejemplos/`:

```bash
uv run --locked --extra hardware Semana_10_GPIO_y_Perifericos/Python/05_lcd_i2c/lcd_basic.py
```

Usa Ctrl+C para detener los bucles. Los ejemplos cierran o liberan sus recursos al terminar.

## Resultados esperados

`lcd_basic.py` muestra dos líneas durante 10 s y limpia la pantalla. `lcd_multiline.py` deja a la biblioteca distribuir el texto en las dos líneas disponibles. `lcd_screens.py` muestra cada pantalla 5 s y la deja limpia otros 3 s.

## Limitaciones

Un LCD 16×2 no muestra mensajes arbitrariamente largos completos. Su ROM puede no incluir tildes ni el símbolo °; las pantallas alternadas utilizan texto sin esos caracteres.

## Problemas frecuentes

Si aparece una fila de bloques, ajusta el contraste y revisa conexiones. Si el dispositivo no responde, comprueba la dirección con `i2cdetect -y 1` únicamente en el bus del circuito de laboratorio. No asumas que todos los adaptadores usan `0x27`.

## Comprobación

Contrasta los resultados con el circuito real. Consulta las [pruebas de lógica](../../../pruebas/README.md) y el [registro de validación](../../../REGISTRO_PYTHON.md) para distinguir resultados comprobados y pendientes.
