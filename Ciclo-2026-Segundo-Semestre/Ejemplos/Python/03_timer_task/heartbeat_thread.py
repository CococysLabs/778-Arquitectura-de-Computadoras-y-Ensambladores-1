"""Parpadear un LED en un hilo mientras continúa el programa principal."""

import threading
import time

import RPi.GPIO as GPIO

LED_PIN = 21
PERIOD = 0.5

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
stop_event = threading.Event()


def heartbeat():
    state = False
    while not stop_event.is_set():
        state = not state
        GPIO.output(LED_PIN, state)
        if stop_event.wait(PERIOD):
            break


thread = threading.Thread(target=heartbeat)
try:
    thread.start()
    while True:
        print("El hilo principal continúa trabajando.")
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    stop_event.set()
    if thread.ident is not None:
        thread.join()
    GPIO.cleanup()
