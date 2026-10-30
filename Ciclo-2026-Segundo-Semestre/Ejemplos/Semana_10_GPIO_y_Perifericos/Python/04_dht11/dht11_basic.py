"""Leer temperatura y humedad de un DHT11 conectado a GPIO20."""

import time

import adafruit_dht
import board

DHT_PIN = board.D20
sensor = adafruit_dht.DHT11(DHT_PIN)

try:
    while True:
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
        time.sleep(2)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    sensor.exit()
