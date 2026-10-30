"""Medir distancia con TRIG en GPIO23 y ECHO adaptado a GPIO24."""

import time

from hcsr04 import HCSR04

sensor = HCSR04(23, 24)
try:
    while True:
        distance = sensor.read()
        if distance is None:
            print("No se recibió un eco válido.")
        else:
            print(f"Distancia: {distance:.1f} cm")
        time.sleep(0.06)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    sensor.cleanup()
