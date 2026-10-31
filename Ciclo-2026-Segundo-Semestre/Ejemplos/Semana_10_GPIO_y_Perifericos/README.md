# Semana 10: GPIO y periféricos

Ejemplos Python de GPIO, sensores y periféricos para Raspberry Pi.

| Grupo | Qué enseña |
| --- | --- |
| [00_blink](Python/00_blink/README.md) | Salida GPIO digital y parpadeo. |
| [01_input_button](Python/01_input_button/README.md) | Polling, callbacks, rebotes y duración de pulsación. |
| [02_pwm](Python/02_pwm/README.md) | Frecuencia y ciclo de trabajo con buzzer y servo. |
| [04_dht11](Python/04_dht11/README.md) | Lectura digital de temperatura y humedad. |
| [05_lcd_i2c](Python/05_lcd_i2c/README.md) | Pantallas de texto mediante I²C. |
| [07_hc_sr04](Python/07_hc_sr04/README.md) | GPIO de disparo/eco, distancia y tiempos de espera. |
| [08_adc](Python/08_adc/README.md) | Lecturas de ADS1115 y PCF8591 mediante I²C. |

## Ejecución

Desde la raíz `Ejemplos/`, prepara Python 3.13 en una Raspberry Pi 3/4 y sigue las conexiones de cada README:

```bash
uv sync --locked --extra hardware
uv run --locked --extra hardware Semana_10_GPIO_y_Perifericos/Python/00_blink/blink.py
```

Cambia la ruta por el programa del grupo que estudiarás. Ejecuta un circuito a la vez y termina con Ctrl+C. Revisa la [preparación](../documentacion/preparar_entorno.md) y los [límites eléctricos y conexiones](../documentacion/gpio_y_sensores.md).

[Volver al índice](../README.md).
