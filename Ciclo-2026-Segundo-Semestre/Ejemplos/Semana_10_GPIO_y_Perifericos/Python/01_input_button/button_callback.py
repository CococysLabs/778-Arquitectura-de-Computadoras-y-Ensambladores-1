"""Alternar el LED mediante un callback de flanco descendente."""

import threading
import time

import RPi.GPIO as GPIO

BUTTON_PIN = 17
LED_PIN = 18
BOUNCE_MS = 120

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

led_state = False
stopping = False
callback_lock = threading.Lock()


def on_button(channel):
    global led_state
    with callback_lock:
        if stopping:
            return
        led_state = not led_state
        GPIO.output(LED_PIN, led_state)
        print(f"LED {'encendido' if led_state else 'apagado'}")


registered = False
try:
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=on_button,
                          bouncetime=BOUNCE_MS)
    registered = True
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    with callback_lock:
        stopping = True
    try:
        if registered:
            GPIO.remove_event_detect(BUTTON_PIN)
    finally:
        GPIO.cleanup()
