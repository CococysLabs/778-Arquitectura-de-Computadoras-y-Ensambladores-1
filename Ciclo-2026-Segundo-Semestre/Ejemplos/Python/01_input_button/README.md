# Entradas digitales: pulsadores y antirrebote

## Objetivo y funcionamiento

Comparar sondeo, callbacks y clasificación de pulsaciones utilizando una entrada con resistencia pull-up.

Estos programas son ejemplos de clase, no soluciones de evaluaciones.

| Programa | Funcionamiento |
| --- | --- |
| `button_polling.py` | Sondea cada 20 ms; exige 200 ms de nivel estable. |
| `button_callback.py` | Callback de flanco descendente; ventana antirrebote de 120 ms. |
| `button_short_long.py` | Exige 50 ms de nivel estable y distingue duración al soltar. |

Sustituye el nombre del archivo en el comando para ejecutar las otras variantes.

## Requisitos

Raspberry Pi 3/4, pulsador, LED y resistencia de 330 Ω. Python 3.13 es el objetivo de verificación. Consulta las [versiones y limitaciones del entorno](../documentacion/preparar_entorno.md). El funcionamiento físico requiere validación en una Pi; las pruebas con dobles no sustituyen el circuito.

## Conexiones físicas

Desconecta la alimentación antes de cablear. Los GPIO admiten lógica de 3,3 V, no 5 V. Usa numeración BCM en el código.

| Componente | Conexión |
| --- | --- |
| Pulsador | Entre GPIO17 (pin físico 11) y GND (pin 6) |
| LED | GPIO18 (pin 12), resistencia de 330 Ω y ánodo; cátodo a GND |

`PUD_UP` mantiene HIGH al soltar y LOW al presionar.

## Instalación

Desde la carpeta `Python/`, con uv y Python 3.13 disponibles:

```bash
uv sync --locked --extra hardware
```

Sigue la [preparación del entorno](../documentacion/preparar_entorno.md) para instalar requisitos del sistema y comprobar acceso a GPIO.

## Ejecución

Desde `Python/`, ejecuta un programa a la vez:

```bash
uv run --locked --extra hardware 01_input_button/button_polling.py
```

Detén el programa con Ctrl+C. Se liberan los GPIO al terminar.

## Resultados esperados

Una pulsación estable alterna el LED. Mantener el botón presionado no genera cambios repetidos en el ejemplo de sondeo. En el tercer programa, una pulsación de al menos 1500 ms apaga el LED al soltarlo.

## Limitaciones

Las pulsaciones menores que la ventana de antirrebote pueden descartarse. El callback aplica una ventana temporal; no garantiza filtrado de cualquier forma de ruido eléctrico.

## Problemas frecuentes

Si siempre indica presionado, revisa que el pulsador conecte GPIO17 a GND y comprueba qué terminales están unidos internamente. Si falla el detector de flanco, revisa permisos, otros procesos GPIO y la versión del sistema.

## Comprobación

Comprueba el comportamiento descrito y repite el cierre con Ctrl+C. Las pruebas de lógica están en [pruebas](../../pruebas/README.md); la validación física sigue pendiente hasta registrar una sesión real en Raspberry Pi.
