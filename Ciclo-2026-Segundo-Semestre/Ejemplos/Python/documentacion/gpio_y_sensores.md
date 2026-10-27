# GPIO y sensores con Raspberry Pi 3/4

## Numeración y niveles eléctricos

Los ejemplos utilizan numeración **BCM**. El número BCM del código no es el número físico del conector. Confirma orientación y pin 1 antes de cablear; la documentación de cada tema identifica ambos números.

Los GPIO trabajan con lógica de **3,3 V y no toleran 5 V**. Los pines de alimentación de 5 V no son GPIO. Desconecta la alimentación antes de modificar el circuito y revisa la [documentación de Raspberry Pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html).

No uses un límite de corriente genérico como objetivo de diseño. Comprueba los límites del modelo y del componente. Los motores, relés, servos y cargas de consumo alto requieren alimentación o etapa de potencia adecuada.

## Conexiones de los ejemplos

| Tema | BCM | Pin físico | Observación |
| --- | --- | --- | --- |
| Blink y temporizadores | GPIO21 | 40 | LED con resistencia en serie |
| Pulsador | GPIO17 | 11 | Botón a GND; pull-up interno |
| LED de pulsador | GPIO18 | 12 | Resistencia en serie |
| PWM | GPIO12 | 32 | Buzzer pasivo o señal del servo |
| DHT11 | GPIO20 | 38 | DATA con pull-up a 3,3 V |
| I²C SDA | GPIO2 | 3 | Adaptar niveles si el módulo usa 5 V |
| I²C SCL | GPIO3 | 5 | Adaptar niveles si el módulo usa 5 V |
| HC-SR04 TRIG | GPIO23 | 16 | Pulso de disparo |
| HC-SR04 ECHO | GPIO24 | 18 | Divisor de tensión obligatorio en el sensor estándar de 5 V |

Las conexiones completas, alimentación y GND están en los README de cada carpeta; esta tabla no los sustituye.

## Entradas, salidas y limpieza

Una resistencia pull-up define HIGH cuando el botón está abierto; al unirlo a GND se lee LOW. El antirrebote descarta transiciones demasiado breves. Los ejemplos de sondeo aplican un tiempo de estabilidad; el callback usa la ventana de detección que proporciona RPi.GPIO.

La salida digital alterna HIGH/LOW. PWM por software cambia el ciclo de trabajo, pero no genera una tensión analógica estable ni un pulso garantizado en tiempo real.

Al cerrar, los ejemplos detienen tareas y liberan sus recursos. No conectes dos programas a los mismos pines ni mezcles bibliotecas para controlar simultáneamente el pin del DHT11.

## Sensores y actuadores

- **DHT11:** alimenta según el circuito documentado y espera al menos dos segundos entre intentos. Un fallo de lectura se informa como fallo.
- **HC-SR04:** el ECHO estándar entrega 5 V; usa divisor o adaptación de nivel antes de conectarlo a la Pi.
- **LCD e I²C:** comprueba dirección, tensión de alimentación y tensión de los pull-ups de SDA/SCL.
- **ADC:** respeta los límites eléctricos de entrada independientemente de la ganancia seleccionada.
- **Servo:** utiliza fuente adecuada, GND común y límites calibrados; detén el barrido antes de forzar un tope mecánico.

No se incorporan diagramas de terceros sin atribución y permiso verificados. El cableado se especifica mediante tablas.

## Referencias

- [Raspberry Pi: hardware y GPIO](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- [Documentación de RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
- [HC-SR04 y adaptación de ECHO](https://gpiozero.readthedocs.io/en/stable/api_input.html)
- [Preparación del entorno](preparar_entorno.md)
