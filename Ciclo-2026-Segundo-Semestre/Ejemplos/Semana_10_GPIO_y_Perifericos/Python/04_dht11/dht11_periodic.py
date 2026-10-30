"""Muestrear un DHT11 cada dos segundos, incluso después de un error."""

import time

import adafruit_dht
import board

DHT_PIN = board.D20
READ_INTERVAL = 2.0
sensor = adafruit_dht.DHT11(DHT_PIN)
last_attempt = None

try:
    while True:
        now = time.monotonic()
        if last_attempt is None or now - last_attempt >= READ_INTERVAL:
            # Un fallo también cuenta como intento para no saturar el sensor.
            last_attempt = now
            try:
                temperature_c = sensor.temperature
                humidity = sensor.humidity
                if temperature_c is None or humidity is None:
                    print("Lectura incompleta del DHT11.")
                else:
                    print(f"Temperatura: {temperature_c:.1f} °C")
                    print(f"Humedad: {humidity:.1f} %")
            except RuntimeError as error:
                print(f"No se pudo leer el DHT11: {error}")
        time.sleep(0.2)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    sensor.exit()
