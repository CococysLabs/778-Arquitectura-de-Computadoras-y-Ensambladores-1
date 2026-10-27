"""Alternar el LED una vez por pulsación estable del botón."""

import time

import RPi.GPIO as GPIO

BUTTON_PIN = 17
LED_PIN = 18
DEBOUNCE_MS = 200

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

led_state = False
stable_level = GPIO.HIGH
last_level = GPIO.HIGH
last_change = time.monotonic()

try:
    while True:
        level = GPIO.input(BUTTON_PIN)
        now = time.monotonic()
        if level != last_level:
            last_level = level
            last_change = now
        if level != stable_level and now - last_change >= DEBOUNCE_MS / 1000:
            stable_level = level
            if stable_level == GPIO.LOW:
                led_state = not led_state
                GPIO.output(LED_PIN, led_state)
                print(f"LED {'encendido' if led_state else 'apagado'}")
        time.sleep(0.02)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    GPIO.cleanup()
