"""Controlador didáctico del HC-SR04; devuelve centímetros o None."""

import time

import RPi.GPIO as GPIO


class HCSR04:
    SPEED_OF_SOUND = 34300
    TIMEOUT = 0.02

    def __init__(self, trig_pin: int, echo_pin: int):
        if trig_pin == echo_pin:
            raise ValueError("TRIG y ECHO requieren pines distintos.")
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(trig_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(echo_pin, GPIO.IN)

    def read(self) -> float | None:
        GPIO.output(self.trig_pin, GPIO.LOW)
        time.sleep(0.0002)
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, GPIO.LOW)

        deadline = time.monotonic() + self.TIMEOUT
        while GPIO.input(self.echo_pin) == GPIO.LOW:
            if time.monotonic() >= deadline:
                return None
        start = time.monotonic()

        deadline = start + self.TIMEOUT
        while GPIO.input(self.echo_pin) == GPIO.HIGH:
            if time.monotonic() >= deadline:
                return None
        end = time.monotonic()
        return (end - start) * self.SPEED_OF_SOUND / 2

    def cleanup(self):
        GPIO.cleanup((self.trig_pin, self.echo_pin))
