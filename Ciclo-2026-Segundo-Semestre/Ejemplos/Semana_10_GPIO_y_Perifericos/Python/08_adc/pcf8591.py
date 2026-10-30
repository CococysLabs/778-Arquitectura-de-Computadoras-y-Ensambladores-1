"""Leer el canal A0 de un PCF8591 mediante I²C."""

import time

import smbus

ADDRESS = 0x48
CHANNEL_A0 = 0x40
bus = smbus.SMBus(1)

try:
    while True:
        bus.write_byte(ADDRESS, CHANNEL_A0)
        bus.read_byte(ADDRESS)  # La primera lectura corresponde a la conversión anterior.
        value = bus.read_byte(ADDRESS)
        print(f"Valor del canal A0: {value}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    bus.close()
