# PWM: tonos y barrido de un servo

## Objetivo y funcionamiento

Relacionar frecuencia y ciclo de trabajo con un buzzer pasivo y un servomotor.

Estos programas son ejemplos de clase, no soluciones de evaluaciones.

Para el servo ejecuta `uv run --locked --extra hardware 02_pwm/servo_sweep.py`. Empieza con el servo sin carga y comprueba sus límites antes de permitir el barrido completo.

## Requisitos

Raspberry Pi 3/4; buzzer pasivo de bajo consumo compatible con 3,3 V o servo con fuente externa regulada según su ficha técnica. Python 3.13 es el objetivo de verificación. Consulta las [versiones y limitaciones del entorno](../documentacion/preparar_entorno.md). El funcionamiento físico requiere validación en una Pi; las pruebas con dobles no sustituyen el circuito.

## Conexiones físicas

Desconecta la alimentación antes de cablear. Los GPIO admiten lógica de 3,3 V, no 5 V. Usa numeración BCM en el código.

| Señal | Conexión |
| --- | --- |
| PWM del buzzer o señal del servo | GPIO12 (pin físico 32) |
| GND del circuito | GND de la Pi (pin físico 34) |
| Alimentación del servo | Fuente externa adecuada; nunca un GPIO |

Conecta un componente a la vez. Une las masas de la fuente externa y la Pi; no unas sus salidas de alimentación. Un buzzer que exceda la corriente permitida necesita una etapa de manejo.

## Instalación

Desde la carpeta `Python/`, con uv y Python 3.13 disponibles:

```bash
uv sync --locked --extra hardware
```

Sigue la [preparación del entorno](../documentacion/preparar_entorno.md) para instalar requisitos del sistema y comprobar acceso a GPIO.

## Ejecución

Desde `Python/`, ejecuta un programa a la vez:

```bash
uv run --locked --extra hardware 02_pwm/buzzer_tones.py
```

Detén el programa con Ctrl+C. Se liberan los GPIO al terminar.

## Resultados esperados

El buzzer repite los tonos 262, 330, 392 y 523 Hz, con 0,5 s por tono. `servo_sweep.py` recorre los ciclos de trabajo entre 2,5 % y 12,5 % y regresa.

## Limitaciones

`RPi.GPIO.PWM` genera PWM por software, incluso en un pin con función PWM hardware. Puede haber fluctuaciones. Los extremos equivalentes a 0° y 180° dependen del servo; calibra `DUTY_MIN` y `DUTY_MAX` sin forzar topes.

## Problemas frecuentes

Si el buzzer solo hace clic, comprueba que sea pasivo. Si el servo vibra, revisa alimentación, tierra común y calibración; detén el programa si alcanza un tope mecánico.

## Comprobación

Comprueba el comportamiento descrito y repite el cierre con Ctrl+C. Las pruebas de lógica están en [pruebas](../../pruebas/README.md); la validación física sigue pendiente hasta registrar una sesión real en Raspberry Pi.
