"""Conectar con un broker MQTT y cerrar la sesión."""

import os
import threading
import time

import paho.mqtt.client as mqtt


def main():
    connected = threading.Event()
    accepted = False

    def on_connect(client, userdata, flags, reason_code, properties):
        nonlocal accepted
        accepted = not reason_code.is_failure
        connected.set()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    try:
        client.connect(os.getenv("MQTT_HOST", "127.0.0.1"),
                       int(os.getenv("MQTT_PORT", "1883")))
        client.loop_start()
        if not connected.wait(10) or not accepted:
            raise RuntimeError("El broker no confirmó la conexión.")
        print("Conectado al broker MQTT.")
        time.sleep(2)
    except (OSError, ValueError, RuntimeError) as error:
        raise SystemExit(f"No se pudo completar la conexión MQTT: {error}")
    finally:
        client.disconnect()
        client.loop_stop()
    print("Desconectado.")


if __name__ == "__main__":
    main()
