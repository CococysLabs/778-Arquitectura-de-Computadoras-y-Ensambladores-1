"""Publicar y recibir en MQTT 5, sin recibir los mensajes propios."""

import os
import threading
import time

import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions


def on_message(client, userdata, message):
    print(f"Recibido: {message.payload.decode('utf-8', errors='replace')}")


def main():
    topic = os.getenv("MQTT_TOPIC", "curso778/demo")
    if not topic or any(char in topic for char in ("+", "#", "\0")):
        raise SystemExit("MQTT_TOPIC debe ser un tópico sin comodines ni NUL.")
    ready = threading.Event()
    accepted = False

    def on_connect(client, userdata, flags, reason_code, properties):
        nonlocal accepted
        accepted = False
        ready.clear()
        if reason_code.is_failure:
            ready.set()
            return
        result, mid = client.subscribe(topic, options=SubscribeOptions(qos=0, noLocal=True))
        if result != mqtt.MQTT_ERR_SUCCESS:
            ready.set()

    def on_subscribe(client, userdata, mid, reason_codes, properties):
        nonlocal accepted
        accepted = bool(reason_codes) and not any(code.is_failure for code in reason_codes)
        ready.set()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.reconnect_delay_set(1, 30)
    try:
        client.connect(os.getenv("MQTT_HOST", "127.0.0.1"),
                       int(os.getenv("MQTT_PORT", "1883")))
        client.loop_start()
        if not ready.wait(10) or not accepted:
            raise RuntimeError("El broker no confirmó la suscripción MQTT 5.")
        print(f"Conectado y suscrito a {topic}.")
        counter = 0
        while True:
            info = client.publish(topic, f"Mensaje {counter}")
            if info.rc != mqtt.MQTT_ERR_SUCCESS:
                raise RuntimeError(f"Publicación rechazada por el cliente: {info.rc}")
            info.wait_for_publish(timeout=5)
            if not info.is_published():
                raise RuntimeError("La publicación no terminó dentro de 5 s.")
            counter += 1
            time.sleep(2)
    except KeyboardInterrupt:
        print("Programa terminado.")
    except (OSError, ValueError, RuntimeError) as error:
        raise SystemExit(f"No se pudo completar el intercambio MQTT: {error}")
    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
