# Comunicación MQTT

## Objetivo y funcionamiento

Conectar un cliente a un broker, publicar y recibir mensajes y observar la diferencia entre MQTT 3.1.1 y MQTT 5. MQTTX es un cliente gráfico opcional; no es una dependencia de estos programas.

| Archivo | Función |
| --- | --- |
| `client.py` | Espera confirmación de conexión, permanece 2 s y desconecta. |
| `publish.py` | Publica un saludo con hora de ejecución. |
| `subscribe.py` | Espera mensajes después de confirmar la suscripción. |
| `sub_pub.py` | Publica cada 2 s en MQTT 5 y recibe mensajes de otros clientes. |

## Requisitos

Python 3.13, Paho MQTT 2.1.0 y un broker de laboratorio. Puede ejecutarse en una computadora sin Raspberry Pi. `sub_pub.py` requiere MQTT 5. Consulta las [versiones comprobadas](../documentacion/preparar_entorno.md).

## Conexiones físicas

No requiere GPIO ni sensores. Cliente y broker deben comunicarse por red.

## Instalación

Desde `Python/`:

```bash
uv sync --locked --extra mqtt
```

Configura un broker propio de laboratorio en localhost. Si utilizas Mosquitto en un contenedor desechable, expón el puerto únicamente en `127.0.0.1`, no en todas las interfaces. No se incluyen credenciales ni servidores personales.

## Configuración y ejecución

En cada terminal establece los mismos valores:

```bash
export MQTT_HOST=127.0.0.1
export MQTT_PORT=1883
export MQTT_TOPIC=curso778/demo
```

`MQTT_HOST` debe contener un nombre de host o IP, sin prefijo `mqtt://`. Las variables se leen del entorno de la terminal; estos ejemplos no cargan un archivo `.env`.

En una terminal, desde `Python/`:

```bash
uv run --locked --extra mqtt 09_mqtt/subscribe.py
```

Cuando aparezca «Suscripción confirmada», en otra terminal:

```bash
uv run --locked --extra mqtt 09_mqtt/publish.py
```

Para las otras demostraciones:

```bash
uv run --locked --extra mqtt 09_mqtt/client.py
uv run --locked --extra mqtt 09_mqtt/sub_pub.py
```

Detén las suscripciones con Ctrl+C.

## Resultados esperados

El suscriptor muestra el saludo publicado. El cliente simple confirma conexión y desconexión. En MQTT 5, `noLocal=True` impide que una conexión reciba sus propias publicaciones: utiliza otro cliente para enviar un mensaje y comprobar la recepción.

El texto publicado no contiene una lectura física. QoS 0 no asegura recepción del suscriptor. Los bytes no UTF-8 se muestran con caracteres de sustitución.

## Limitaciones y seguridad

Esta demostración usa TCP sin TLS ni autenticación y debe limitarse a una red de laboratorio controlada. No envíes datos personales ni credenciales a un broker público. Una conexión exitosa no implica entrega a todos los receptores.

Las pruebas de servicios locales están separadas de los dobles de lógica: [instrucciones de prueba](../../pruebas/README.md).

## Problemas frecuentes

- Conexión rechazada: revisa puerto, broker y dirección. Un contenedor necesita publicar su puerto.
- No llegan mensajes: confirma tópico idéntico y espera la confirmación de suscripción antes de publicar.
- `sub_pub.py` no recibe sus mensajes: es el efecto esperado de `noLocal`.
- El broker rechaza la suscripción: revisa permisos y soporte de MQTT 5.
- Los programas no configuran reconexión persistente de aplicación ni almacenamiento de mensajes: reinícialos tras resolver un fallo.
