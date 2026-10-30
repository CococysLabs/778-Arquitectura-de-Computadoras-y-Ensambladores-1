# Pruebas de Python y ARM64

## Fundamentos de arquitectura sin hardware

Desde `Ejemplos/`, sin instalar extras:

```bash
python3.13 -m unittest discover -s pruebas -p test_fundamentos.py -v
```

Cuatro pruebas ejecutan los programas de semana 02 y verifican su salida: bases numéricas, complemento a dos de ocho bits, máscaras/desplazamientos y bytes en ambos órdenes.

## Ensamblado, ejecución y depuración ARM64

Instala las herramientas de la [guía ARM64](../documentacion/arm64.md). Desde la raíz `Ejemplos/`:

```bash
python3.13 -m unittest discover -s pruebas -p test_arm64.py -v
PRUEBAS_GDB=1 python3.13 -m unittest discover -s pruebas -p test_arm64.py -v
```

También se comprueba la reconstrucción al cambiar una rutina compartida o de otra semana. La primera orden ejecuta QEMU y omite las cuatro pruebas que requieren sesiones TCP de GDB. La segunda activa también las cuatro pruebas reales de depuración. Las pruebas crean archivos y binarios temporales fuera del repositorio y los eliminan al terminar. Verifican EOF, menú, buffers, formato, límites numéricos, pila y registros preservados. También ejecutan los cinco programas nuevos de semanas 04 y 05, inspeccionan ELF y desensamblado de Hello World y comprueban con GDB registros, flags, arreglos y actualización de punteros.

La ejecución nativa en Raspberry Pi y los perfiles visuales de VS Code siguen pendientes. Consulta la [validación vigente](../documentacion/interna/VALIDACION.md).

## Pruebas de lógica sin hardware

Desde la raíz `Ejemplos/`, con los extras de servicios instalados en `.venv`:

```bash
.venv/bin/python -m unittest discover -s pruebas -p test_python.py -v
```

Preparación del entorno, desde `Ejemplos/`: `uv sync --locked --extra mqtt --extra mongodb`. No se necesita instalar GPIO para estos dobles.

Las pruebas comprueban transiciones de pulsadores, antirrebote, duración, cierre de hilo y temporizador, liberación de LCD/ADC, reintentos DHT, conversión PCF8591, tiempos de espera del eco, payload MQTT inválido y validación/cierre MongoDB. Los dobles utilizan estímulos sintéticos: no constituyen mediciones ni funcionamiento de hardware.

## Integración con servicios locales reales

`test_servicios.py` se omite por defecto. Requiere un broker con MQTT 5 en `127.0.0.1:18883` y MongoDB en `127.0.0.1:27078`. Solo utiliza datos sintéticos y una base MongoDB de nombre aleatorio que se elimina al terminar.

Si dispones de Docker, inicia servicios desechables:

```bash
docker run --rm -d --name curso778-mqtt-prueba -p 127.0.0.1:18883:1883 eclipse-mosquitto:2.0 sh -c 'printf "listener 1883\nallow_anonymous true\npersistence false\n" > /tmp/lab.conf; exec mosquitto -c /tmp/lab.conf'
docker run --rm -d --name curso778-mongo-prueba -p 127.0.0.1:27078:27017 mongo:8.0 --bind_ip_all
```

Espera a que ambos servicios estén listos antes de ejecutar, desde la raíz `Ejemplos/`:

```bash
PRUEBAS_SERVICIOS=1 .venv/bin/python -m unittest discover -s pruebas -p test_servicios.py -v
```

Puedes ajustar los puertos mediante `PRUEBA_MQTT_PORT` y `PRUEBA_MONGO_PORT`. Los hosts de prueba están fijados a localhost. No apuntes estas pruebas a infraestructura institucional o datos reales.

Las pruebas ejecutan los programas originales de esta carpeta de ejemplos, intercambian mensajes, comprueban documentos almacenados y verifican cierre con Ctrl+C. No sustituyen servidores por dobles. MongoDB necesita tiempo para iniciar: si aún no acepta conexiones, espera y repite.

Al terminar:

```bash
docker stop curso778-mqtt-prueba curso778-mongo-prueba
```

La opción `--rm` elimina los contenedores al detenerlos; las imágenes descargadas permanecen en la caché de Docker.

## Comprobaciones estáticas

Desde la raíz `Ejemplos/`:

```bash
python3.13 pruebas/verificar_repositorio.py
```

Compila en memoria las fuentes de ejemplos y pruebas; comprueba enlaces relativos Markdown, patrones de secretos, archivos excluidos y diferencias de formato. No consulta enlaces externos ni garantiza ausencia total de secretos.

## Suite completa

Con los servicios locales iniciados, desde `Ejemplos/`:

```bash
PRUEBAS_GDB=1 PRUEBAS_SERVICIOS=1 .venv/bin/python -m unittest discover -s pruebas -v
```

## Validación física pendiente

Repite en una Pi 3/4 de 64 bits la instalación del extra `hardware`; registra modelo, versión del sistema, Python y dependencias. Comprueba circuitos, calibración de servo, lecturas y cierre. Los módulos que se importan en x86-64 no acreditan acceso al hardware.

Consulta el [registro de resultados](../documentacion/interna/REGISTRO_PYTHON.md) para conocer qué comprobaciones se ejecutaron.
