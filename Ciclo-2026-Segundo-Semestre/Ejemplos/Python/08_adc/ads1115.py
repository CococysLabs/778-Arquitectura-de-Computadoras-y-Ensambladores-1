"""Leer tensión y código digital del canal A3 de un ADS1115."""

import time

import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

i2c = board.I2C()
try:
    ads = ADS1115(i2c)
    channel3 = AnalogIn(ads, ads1x15.Pin.A3)
    while True:
        print(f"Tensión del canal A3: {channel3.voltage:.2f} V")
        print(f"Valor del canal A3: {channel3.value}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    i2c.deinit()
