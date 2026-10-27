"""Escuchar mensajes MQTT y cerrar la sesión con Ctrl+C."""

import os

import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    text = message.payload.decode("utf-8", errors="replace")
    print(f"Mensaje recibido: {text}")


def main():
    topic = os.getenv("MQTT_TOPIC", "curso778/demo")
    if not topic or any(char in topic for char in ("+", "#", "\0")):
        raise SystemExit("MQTT_TOPIC debe ser un tópico sin comodines ni NUL.")
    failed = False

    def on_connect(client, userdata, flags, reason_code, properties):
        nonlocal failed
        if reason_code.is_failure:
            failed = True
            print(f"Conexión rechazada: {reason_code}")
            client.disconnect()
            return
        result, mid = client.subscribe(topic)
        if result != mqtt.MQTT_ERR_SUCCESS:
            failed = True
            print("No se pudo solicitar la suscripción.")
            client.disconnect()

    def on_subscribe(client, userdata, mid, reason_codes, properties):
        nonlocal failed
        failed = any(code.is_failure for code in reason_codes)
        if failed:
            print("El broker rechazó la suscripción.")
            client.disconnect()
        else:
            print(f"Suscripción confirmada: {topic}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    try:
        client.connect(os.getenv("MQTT_HOST", "127.0.0.1"),
                       int(os.getenv("MQTT_PORT", "1883")))
        client.loop_forever()
    except KeyboardInterrupt:
        print("Programa terminado.")
    except (OSError, ValueError, RuntimeError) as error:
        raise SystemExit(f"No se pudo mantener la suscripción: {error}")
    finally:
        client.disconnect()
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
