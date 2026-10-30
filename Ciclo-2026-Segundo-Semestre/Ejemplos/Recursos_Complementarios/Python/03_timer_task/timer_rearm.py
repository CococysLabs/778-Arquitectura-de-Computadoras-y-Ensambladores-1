"""Rearmar un temporizador sin acceder a GPIO después del cierre."""

import threading
import time

import RPi.GPIO as GPIO

LED_PIN = 21
PERIOD = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
stop_event = threading.Event()
timer_lock = threading.Lock()
led_state = False
timer = None


def task():
    global led_state, timer
    # La cancelación y el rearme comparten el mismo bloqueo.
    with timer_lock:
        if stop_event.is_set():
            return
        led_state = not led_state
        GPIO.output(LED_PIN, led_state)
        print(f"Temporizador: LED {'encendido' if led_state else 'apagado'}")
        timer = threading.Timer(PERIOD, task)
        timer.start()


try:
    timer = threading.Timer(PERIOD, task)
    timer.start()
    print("Temporizador rearmable cada 3 segundos.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa terminado.")
finally:
    with timer_lock:
        stop_event.set()
        current_timer = timer
        if current_timer is not None:
            current_timer.cancel()
    if current_timer is not None and current_timer.ident is not None:
        current_timer.join()
    GPIO.cleanup()
