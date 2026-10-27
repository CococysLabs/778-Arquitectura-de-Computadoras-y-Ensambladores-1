# Ejemplos Python: GPIO, sensores y comunicación

Ejemplos de clase del curso 778 para estudiar interfaces de entrada/salida, concurrencia, sensores e intercambio de datos. Las carpetas y los nombres son convenciones propuestas para este conjunto; no se presentan como reglas institucionales obligatorias.

Empieza por [preparar el entorno](documentacion/preparar_entorno.md) y [revisar conexiones GPIO](documentacion/gpio_y_sensores.md).

| Tema | Programas | Propósito | Requisitos |
| --- | --- | --- | --- |
| [00: Blink](00_blink/README.md) | `blink.py` | Salida digital | Pi 3/4, LED y resistencia |
| [01: Pulsadores](01_input_button/README.md) | `button_polling.py`, `button_callback.py`, `button_short_long.py` | Entrada, rebotes y duración | Pi, botón, LED y resistencia |
| [02: PWM](02_pwm/README.md) | `buzzer_tones.py`, `servo_sweep.py` | Frecuencia y ciclo de trabajo | Pi y buzzer o servo |
| [03: Temporización](03_timer_task/README.md) | `heartbeat_thread.py`, `timer_rearm.py` | Concurrencia y cierre | Pi y LED |
| [04: DHT11](04_dht11/README.md) | `dht11_basic.py`, `dht11_periodic.py` | Muestreo digital | Pi y DHT11 |
| [05: LCD](05_lcd_i2c/README.md) | `lcd_basic.py`, `lcd_multiline.py`, `lcd_screens.py` | Visualización por I²C | Pi, LCD y adaptación eléctrica |
| [07: HC-SR04](07_hc_sr04/README.md) | `hc_sr04_distance.py`; auxiliar `hcsr04.py` | Tiempo de eco | Pi, sensor y divisor de tensión |
| [08: ADC](08_adc/README.md) | `ads1115.py`, `pcf8591.py` | Conversión analógica | Pi y conversor I²C |
| [09: MQTT](09_mqtt/README.md) | `client.py`, `publish.py`, `subscribe.py`, `sub_pub.py` | Mensajería | Python y broker local |
| [10: MongoDB](10_mongodb/README.md) | `connect.py`, `insert.py`, `query.py`, `simulate_sensor.py`; auxiliar `config.py` | Persistencia y consultas | Python y MongoDB local |

La numeración conserva los identificadores del material de origen; no representa semanas del semestre ni presupone una lección 06.

## Ejecución

Ejecuta los comandos de cada README desde esta carpeta. Por ejemplo:

```bash
uv run --locked --extra mqtt 09_mqtt/client.py
```

Instala solo el extra necesario: `hardware`, `mqtt` o `mongodb`. Los programas físicos no funcionan en un PC por instalar sus dependencias.

## Comprobación y límites

Las pruebas de lógica utilizan dobles explícitos. Las pruebas de integración requieren servicios reales y se activan por separado. Ninguna prueba con datos sintéticos acredita lecturas de sensores.

Consulta las [instrucciones de pruebas](../pruebas/README.md) y el [registro de resultados](../REGISTRO_PYTHON.md). La ejecución física y la instalación ARM64 en Pi 3/4 siguen pendientes.

## Procedencia

Adaptado de [PoncheDeFrutas/ARQUI1_2S2026](https://github.com/PoncheDeFrutas/ARQUI1_2S2026/tree/2efa6ebe56a2d74e59c16bf6cf2bbe1050c8ca96/01_PYTHON), commit `2efa6ebe56a2d74e59c16bf6cf2bbe1050c8ca96`, con autorización del titular sobre su código propio.

No se incluyen el proyecto completo, imágenes reservadas ni material de evaluación. La licencia institucional del aporte permanece pendiente de confirmación; no se atribuye automáticamente la licencia de otros repositorios.
