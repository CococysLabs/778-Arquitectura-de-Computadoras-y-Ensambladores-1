"""Alternar un LED conectado a GPIO21 (pin físico 40)."""

import time

import RPi.GPIO as GPIO

LED_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED encendido")
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED apagado")
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    GPIO.cleanup()
