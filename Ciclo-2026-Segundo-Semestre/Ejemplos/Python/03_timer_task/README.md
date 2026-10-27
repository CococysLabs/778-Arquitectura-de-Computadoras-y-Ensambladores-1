# Concurrencia: hilo y temporizador rearmable

## Objetivo y funcionamiento

Ejecutar una tarea periódica sin bloquear el trabajo principal y detenerla antes de liberar GPIO.

Estos programas son ejemplos de clase, no soluciones de evaluaciones.

Para comparar, ejecuta `uv run --locked --extra hardware 03_timer_task/timer_rearm.py`. El cierre del hilo usa un evento; el temporizador protege el rearme y la cancelación con un bloqueo.

## Requisitos

Raspberry Pi 3/4, LED y resistencia de 330 Ω. Python 3.13 es el objetivo de verificación. Consulta las [versiones y limitaciones del entorno](../documentacion/preparar_entorno.md). El funcionamiento físico requiere validación en una Pi; las pruebas con dobles no sustituyen el circuito.

## Conexiones físicas

Desconecta la alimentación antes de cablear. Los GPIO admiten lógica de 3,3 V, no 5 V. Usa numeración BCM en el código.

| Componente | Conexión |
| --- | --- |
| LED | GPIO21 (pin físico 40), resistencia de 330 Ω y ánodo |
| Cátodo | GND (pin físico 39) |

## Instalación

Desde la carpeta `Python/`, con uv y Python 3.13 disponibles:

```bash
uv sync --locked --extra hardware
```

Sigue la [preparación del entorno](../documentacion/preparar_entorno.md) para instalar requisitos del sistema y comprobar acceso a GPIO.

## Ejecución

Desde `Python/`, ejecuta un programa a la vez:

```bash
uv run --locked --extra hardware 03_timer_task/heartbeat_thread.py
```

Detén el programa con Ctrl+C. Se liberan los GPIO al terminar.

## Resultados esperados

El hilo alterna el LED cada 0,5 s mientras el programa principal imprime una vez por segundo. El temporizador cambia el LED cada 3 s y crea la siguiente ejecución al terminar la anterior.

## Limitaciones

No son tareas de tiempo real: el intervalo incluye retrasos del sistema y, en el temporizador, el trabajo de cada callback.

## Problemas frecuentes

Si otro programa controla el mismo pin, ciérralo antes de iniciar. Para salir usa Ctrl+C en la terminal del proceso; espera el cierre antes de volver a ejecutarlo.

## Comprobación

Comprueba el comportamiento descrito y repite el cierre con Ctrl+C. Las pruebas de lógica están en [pruebas](../../pruebas/README.md); la validación física sigue pendiente hasta registrar una sesión real en Raspberry Pi.
