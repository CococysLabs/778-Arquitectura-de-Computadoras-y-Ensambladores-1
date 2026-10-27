# Pruebas de Python

## Pruebas de lógica sin hardware

Desde esta carpeta, con los extras de servicios instalados en `Python/.venv`:

```bash
../Python/.venv/bin/python -m unittest -v test_python
```

Preparación del entorno, desde `Python/`: `uv sync --locked --extra mqtt --extra mongodb`. No se necesita instalar GPIO para estos dobles.

Las pruebas comprueban transiciones de pulsadores, antirrebote, duración, cierre de hilo y temporizador, liberación de LCD/ADC, reintentos DHT, conversión PCF8591, tiempos de espera del eco, payload MQTT inválido y validación/cierre MongoDB. Los dobles utilizan estímulos sintéticos: no constituyen mediciones ni funcionamiento de hardware.

## Integración con servicios locales reales

`test_servicios.py` se omite por defecto. Requiere un broker con MQTT 5 en `127.0.0.1:18883` y MongoDB en `127.0.0.1:27078`. Solo utiliza datos sintéticos y una base MongoDB de nombre aleatorio que se elimina al terminar.

Si dispones de Docker, inicia servicios desechables:

```bash
docker run --rm -d --name curso778-mqtt-prueba -p 127.0.0.1:18883:1883 eclipse-mosquitto:2.0 sh -c 'printf "listener 1883\nallow_anonymous true\npersistence false\n" > /tmp/lab.conf; exec mosquitto -c /tmp/lab.conf'
docker run --rm -d --name curso778-mongo-prueba -p 127.0.0.1:27078:27017 mongo:8.0 --bind_ip_all
```

Espera a que ambos servicios estén listos antes de ejecutar, desde esta carpeta:

```bash
PRUEBAS_SERVICIOS=1 ../Python/.venv/bin/python -m unittest -v test_servicios
```

Puedes ajustar los puertos mediante `PRUEBA_MQTT_PORT` y `PRUEBA_MONGO_PORT`. Los hosts de prueba están fijados a localhost. No apuntes estas pruebas a infraestructura institucional o datos reales.

Las pruebas ejecutan los programas originales de esta carpeta de ejemplos, intercambian mensajes, comprueban documentos almacenados y verifican cierre con Ctrl+C. No sustituyen servidores por dobles. MongoDB necesita tiempo para iniciar: si aún no acepta conexiones, espera y repite.

Al terminar:

```bash
docker stop curso778-mqtt-prueba curso778-mongo-prueba
```

La opción `--rm` elimina los contenedores al detenerlos; las imágenes descargadas permanecen en la caché de Docker.

## Comprobaciones estáticas

Desde esta carpeta:

```bash
python3.13 verificar_repositorio.py
```

Compila en memoria las fuentes de ejemplos y pruebas; comprueba enlaces relativos Markdown, patrones de secretos, archivos excluidos y diferencias de formato. No consulta enlaces externos ni garantiza ausencia total de secretos.

## Validación física pendiente

Repite en una Pi 3/4 de 64 bits la instalación del extra `hardware`; registra modelo, versión del sistema, Python y dependencias. Comprueba circuitos, calibración de servo, lecturas y cierre. Los módulos que se importan en x86-64 no acreditan acceso al hardware.

Consulta el [registro de resultados](../REGISTRO_PYTHON.md) para conocer qué comprobaciones se ejecutaron.
