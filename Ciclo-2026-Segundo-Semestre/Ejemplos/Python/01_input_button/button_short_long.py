"""Distinguir pulsaciones cortas y largas al soltar un botón."""

import time

import RPi.GPIO as GPIO

BUTTON_PIN = 17
LED_PIN = 18
LONG_MS = 1500
DEBOUNCE_MS = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

led_state = False
stable_level = GPIO.HIGH
last_level = GPIO.HIGH
last_change = time.monotonic()
press_start = None

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
                press_start = now
            elif press_start is not None:
                duration_ms = (now - press_start) * 1000
                led_state = False if duration_ms >= LONG_MS else not led_state
                GPIO.output(LED_PIN, led_state)
                print(f"Pulsación de {duration_ms:.0f} ms: LED "
                      f"{'encendido' if led_state else 'apagado'}")
                press_start = None
        time.sleep(0.02)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    GPIO.cleanup()
