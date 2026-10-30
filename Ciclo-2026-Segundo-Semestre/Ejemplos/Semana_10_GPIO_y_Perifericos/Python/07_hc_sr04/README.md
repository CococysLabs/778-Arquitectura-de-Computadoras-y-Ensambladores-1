# HC-SR04: medición por tiempo de eco

## Objetivo y funcionamiento

Convertir la duración de un pulso de eco en distancia y limitar la espera si el sensor no responde.

`hcsr04.py` es un controlador auxiliar importado por el programa principal; no produce mediciones al ejecutarlo por separado. `read()` devuelve `float` o `None`, y `cleanup()` libera únicamente los dos pines usados.

## Requisitos

Pi 3/4, HC-SR04 estándar de 5 V, resistencias de 2,2 kΩ y 3,3 kΩ para dividir ECHO, protoboard y cables. Consulta [preparación y versiones](../../../documentacion/preparar_entorno.md). La ejecución física en Pi 3/4 está pendiente de comprobación; la sintaxis y las pruebas con dobles no acreditan compatibilidad eléctrica.

## Conexiones físicas

Desconecta la alimentación antes de modificar conexiones.

| Señal | Conexión |
| --- | --- |
| VCC | 5 V, pin físico 2 |
| GND | GND, pin físico 6 |
| TRIG | GPIO23, pin físico 16 |
| ECHO | Resistencia de 2,2 kΩ hacia GPIO24 (pin físico 18); desde ese nodo, 3,3 kΩ a GND |

El divisor reduce aproximadamente 5 V a 3,0 V. Nunca conectes ECHO de 5 V directamente al GPIO. Comprueba tensiones, tolerancias y la variante concreta del sensor antes de unir la señal a la Pi.

## Instalación

Desde `Ejemplos/`:

```bash
uv sync --locked --extra hardware
```

Instala también los requisitos del sistema descritos en la [guía del entorno](../../../documentacion/preparar_entorno.md).

## Ejecución

Desde `Ejemplos/`:

```bash
uv run --locked --extra hardware Semana_10_GPIO_y_Perifericos/Python/07_hc_sr04/hc_sr04_distance.py
```

Usa Ctrl+C para detener los bucles. Los ejemplos cierran o liberan sus recursos al terminar.

## Resultados esperados

Aparece una distancia en centímetros cuando llega un eco, o el mensaje «No se recibió un eco válido». Hay una pausa de 60 ms entre mediciones.

## Limitaciones

Se supone velocidad del sonido de 343 m/s. La espera de 20 ms por fase limita el pulso admitido a unos 343 cm teóricos; el alcance útil depende del objeto, la temperatura y la planificación de Linux. No es un instrumento calibrado.

## Problemas frecuentes

Sin eco, comprueba alimentación, divisor y conexiones TRIG/ECHO. Si las lecturas fluctúan, usa una superficie amplia y mantén el objeto estable; no reemplaces `None` por una distancia inventada.

## Comprobación

Contrasta los resultados con el circuito real. Consulta las [pruebas de lógica](../../../pruebas/README.md) y el [registro de validación](../../../REGISTRO_PYTHON.md) para distinguir resultados comprobados y pendientes.
