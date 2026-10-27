"""Publicar un mensaje de demostración sin información personal."""

import os
import time

import paho.mqtt.publish as publish


def main():
    topic = os.getenv("MQTT_TOPIC", "curso778/demo")
    if not topic or any(char in topic for char in ("+", "#", "\0")):
        raise SystemExit("MQTT_TOPIC debe ser un tópico sin comodines ni NUL.")
    message = f"Hola MQTT {time.strftime('%H:%M:%S')}"
    try:
        publish.single(topic, payload=message,
                       hostname=os.getenv("MQTT_HOST", "127.0.0.1"),
                       port=int(os.getenv("MQTT_PORT", "1883")))
    except (OSError, ValueError, RuntimeError) as error:
        raise SystemExit(f"No se pudo publicar: {error}")
    print(f"Publicación completada: {message}")
    print("Esto no confirma la recepción por un suscriptor.")


if __name__ == "__main__":
    main()
