# Salida digital: parpadeo de un LED

## Objetivo y funcionamiento

Configurar una salida GPIO y alternar sus niveles con una pausa de un segundo.

Estos programas son ejemplos de clase, no soluciones de evaluaciones.



## Requisitos

Raspberry Pi 3/4, protoboard, LED y resistencia de 330 Ω. Python 3.13 es el objetivo de verificación. Consulta las [versiones y limitaciones del entorno](../../../documentacion/preparar_entorno.md). El funcionamiento físico requiere validación en una Pi; las pruebas con dobles no sustituyen el circuito.

## Conexiones físicas

Desconecta la alimentación antes de cablear. Los GPIO admiten lógica de 3,3 V, no 5 V. Usa numeración BCM en el código.

| Componente | Conexión |
| --- | --- |
| GPIO21, pin físico 40 | Resistencia de 330 Ω y ánodo del LED |
| Cátodo del LED | GND, pin físico 39 |

## Instalación

Desde la carpeta `Ejemplos/`, con uv y Python 3.13 disponibles:

```bash
uv sync --locked --extra hardware
```

Sigue la [preparación del entorno](../../../documentacion/preparar_entorno.md) para instalar requisitos del sistema y comprobar acceso a GPIO.

## Ejecución

Desde `Ejemplos/`, ejecuta un programa a la vez:

```bash
uv run --locked --extra hardware Semana_10_GPIO_y_Perifericos/Python/00_blink/blink.py
```

Detén el programa con Ctrl+C. Se liberan los GPIO al terminar.

## Resultados esperados

El LED permanece un segundo encendido y uno apagado. La consola informa ambos estados.

## Limitaciones

Las pausas dependen del planificador de Linux; no son temporización de precisión.

## Problemas frecuentes

Si no enciende, revisa la polaridad, la resistencia y GPIO21: el código usa numeración BCM, no el número físico 21.

## Comprobación

Comprueba el comportamiento descrito y repite el cierre con Ctrl+C. Las pruebas de lógica están en [pruebas](../../../pruebas/README.md); la validación física sigue pendiente hasta registrar una sesión real en Raspberry Pi.
