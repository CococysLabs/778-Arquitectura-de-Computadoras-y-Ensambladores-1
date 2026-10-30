# DHT11: temperatura y humedad

## Objetivo y funcionamiento

Leer un sensor digital y comparar un bucle con pausa con un muestreo periódico basado en reloj monotónico.

Ejecuta la variante periódica con `uv run --locked --extra hardware Semana_10_GPIO_y_Perifericos/Python/04_dht11/dht11_periodic.py`. Ambos ejemplos utilizan GPIO20; la numeración del pin debe coincidir con el circuito.

## Requisitos

Pi 3/4, sensor DHT11 y resistencia pull-up de 4,7–10 kΩ si no está integrada en el módulo. Consulta [preparación y versiones](../../../documentacion/preparar_entorno.md). La ejecución física en Pi 3/4 está pendiente de comprobación; la sintaxis y las pruebas con dobles no acreditan compatibilidad eléctrica.

## Conexiones físicas

Desconecta la alimentación antes de modificar conexiones.

| Sensor | Raspberry Pi |
| --- | --- |
| VCC | 3,3 V, pin físico 1 |
| DATA | GPIO20, pin físico 38 |
| GND | GND, pin físico 39 |

En un sensor de cuatro terminales, NC queda libre. Comprueba el orden VCC/DATA/GND del módulo concreto: no todos lo presentan igual. Coloca el pull-up entre DATA y 3,3 V.

## Instalación

Desde `Ejemplos/`:

```bash
uv sync --locked --extra hardware
```

Instala también los requisitos del sistema descritos en la [guía del entorno](../../../documentacion/preparar_entorno.md).

## Ejecución

Desde `Ejemplos/`:

```bash
uv run --locked --extra hardware Semana_10_GPIO_y_Perifericos/Python/04_dht11/dht11_basic.py
```

Usa Ctrl+C para detener los bucles. Los ejemplos cierran o liberan sus recursos al terminar.

## Resultados esperados

La consola muestra temperatura en °C y humedad en %. Ante un fallo de lectura aparece un diagnóstico, sin inventar una medición. `dht11_periodic.py` espera al menos 2 s entre intentos, incluso si el anterior falla.

## Limitaciones

El DHT11 ofrece precisión y frecuencia de muestreo limitadas. Las lecturas dependen del sensor real. No se deben controlar sus pines simultáneamente con RPi.GPIO.

## Problemas frecuentes

Errores ocasionales de lectura son habituales; si persisten revisa pull-up, alimentación y cableado. Si falta el backend de GPIO de Blinka, revisa el sistema y libgpiod según la guía del entorno.

## Comprobación

Contrasta los resultados con el circuito real. Consulta las [pruebas de lógica](../../../pruebas/README.md) y el [registro de validación](../../../REGISTRO_PYTHON.md) para distinguir resultados comprobados y pendientes.
