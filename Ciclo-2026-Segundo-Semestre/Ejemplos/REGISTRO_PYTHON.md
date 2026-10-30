# Registro de adaptación de Python

Registro histórico de la incorporación original. Se actualizaron las rutas; los resultados de la reorganización semanal están en [VALIDACION.md](VALIDACION.md).

Base del curso: `0d0fe4b1729b3a429f5343e897a7f24a7b080114`.
Origen: `PoncheDeFrutas/ARQUI1_2S2026`, commit `2efa6ebe56a2d74e59c16bf6cf2bbe1050c8ca96`.

## Grupo 1: GPIO, pulsadores, PWM y temporización

Archivos: `Semana_10_GPIO_y_Perifericos/Python/00_blink/`, `Semana_10_GPIO_y_Perifericos/Python/01_input_button/`, `Semana_10_GPIO_y_Perifericos/Python/02_pwm/` y `Recursos_Complementarios/Python/03_timer_task/`; pruebas en `pruebas/test_python.py`.

Correcciones: cableado de Blink coincide con GPIO21; pulsación estable por transición; reloj monotónico; liberación de detector; cancelación del temporizador rearmado antes de liberar GPIO; cierre interrumpible del hilo. La documentación distingue PWM por software y exige calibración del servo.

Resultado: **Verificado correctamente**, cinco pruebas de lógica con dobles en Python 3.13.17. **Pendiente por dependencia de hardware o servicios externos**, ejecución eléctrica en Pi 3/4. Los dobles no prueban pines, temporización física ni el backend GPIO.

## Grupo 2: DHT11, LCD, HC-SR04 y ADC

Archivos: `Semana_10_GPIO_y_Perifericos/Python/04_dht11/`, `Semana_10_GPIO_y_Perifericos/Python/05_lcd_i2c/`, `Semana_10_GPIO_y_Perifericos/Python/07_hc_sr04/`, `Semana_10_GPIO_y_Perifericos/Python/08_adc/` y pruebas de sensores.

Correcciones: intervalo DHT incluso tras fallo; tiempo de espera independiente por fase del eco; pausa de 60 ms entre disparos; descarte de conversión anterior PCF8591 y cierre de SMBus; liberación de I²C en ADS1115; textos LCD compatibles con una ROM básica. Los README contienen conexiones, direcciones, límites y advertencias eléctricas.

Resultado: **Verificado correctamente**, nueve pruebas acumuladas de lógica con dobles. **Pendiente por dependencia de hardware o servicios externos**, lectura física de DHT11, LCD, HC-SR04 y ADC. Las mediciones usadas en pruebas son estímulos de prueba, no resultados físicos.

## Grupo 3: MQTT y MongoDB

Archivos: `Recursos_Complementarios/Python/09_mqtt/`, `Recursos_Complementarios/Python/10_mongodb/`, configuración de dependencias y pruebas de servicios.

Correcciones: API de callbacks Paho 2; espera de confirmación MQTT; suscripción confirmada antes de publicar; payload UTF-8 inválido; diagnóstico y cierre ante fallo; broker local configurable. MongoDB usa configuración validada junto al módulo, apertura diferida, contexto de cierre y datos sintéticos. Se corrige `Asensor` a `sensor` y el nombre engañoso `test_sensor.py`.

Resultado: **Verificado correctamente**, cuatro pruebas con servicios reales locales: conexión MQTT; publicación/suscripción; MQTT 5 con `noLocal`; ping, inserción, consulta y simulación MongoDB. Se ejecutaron en Python 3.13.17 con el entorno final de `uv.lock`. La base temporal de nombre aleatorio se eliminó en cada prueba.

Servicios: imágenes `eclipse-mosquitto:2.0` y `mongo:8.0`, con puertos publicados solo en localhost. Digest Mosquitto: `sha256:09b62ff32c2e7b64d4b431b9a89236073289b68db273de2b089edeb9b0d92b5c`; digest MongoDB: `sha256:8e7d23aa641b0ec6c86418866d5d18d74d5abf89061bc5db7bc4b80929021ef6`.

## Verificación final

| Comprobación | Clasificación | Resultado |
| --- | --- | --- |
| Pruebas de lógica | Verificado correctamente | 19 pruebas con dobles explícitos; no son mediciones físicas. |
| Integración local | Verificado correctamente | Cuatro pruebas con MQTT/MongoDB reales y datos sintéticos. |
| Sintaxis | Verificado correctamente | 29 fuentes compiladas en memoria: 26 de ejemplos y tres de pruebas/verificación. |
| Dependencias | Verificado parcialmente | `uv sync --locked --all-extras` y `uv pip check` correctos en Linux x86-64, Python 3.13.17. |
| Versiones | Verificado correctamente | Ninguna versión de paquete conservado cambió respecto al lock original. Se retiran Flask, sus dependencias exclusivas y el intermediario `dotenv`; se declara `python-dotenv` y `smbus` directamente. |
| Importaciones | Verificado parcialmente | Servicios, SMBus, LCD, DHT y ADS importan; RPi.GPIO exige Raspberry Pi. Blinka no acredita funcionamiento de GPIO por importar. |
| Enlaces Markdown locales | Verificado correctamente | 53 enlaces relativos y sus anclas comprobados con `verificar_repositorio.py`. |
| Exclusiones y alcance | Verificado correctamente | Solo 51 archivos nuevos dentro de la ruta autorizada; cachés, entorno y `.env` excluidos. Sin contenido ARM64 ni del proyecto. |
| Credenciales | Verificado parcialmente | Sin coincidencias en patrones revisados; no se auditó el historial completo. |
| Pi 3/4, cableado y periféricos | Pendiente por dependencia de hardware o servicios externos | Falta instalación ARM64, versión de Raspberry Pi OS, comprobación eléctrica y calibración. |
| Atlas, DNS SRV, TLS y autenticación externa | Pendiente por dependencia de hardware o servicios externos | Las integraciones realizadas son locales y sin credenciales. |
| Licencia y aprobación institucional | Verificado parcialmente | Procedencia y permiso del código propio identificados; falta confirmar licencia del aporte y aprobaciones. |

No quedan fallos reproducidos de las pruebas disponibles pendientes de corrección. Se conserva la advertencia de obsolescencia de PyMongo 3.12.0 en Python 3.13; no impidió las pruebas, pero no acredita futuras versiones de Python.

El alcance termina en Python. No se hicieron commits, push ni Pull Requests. La copia independiente usa la rama `feature/ejemplos-python-2026-2s`, sin mover `main`.

## Revisión posterior

Antes de preparar un PR: resolver licencia y aprobación del equipo responsable; repetir pruebas físicas y registrar sistema, modelo y calibración; revisar el [inventario](INVENTARIO_PYTHON.md) y ejecutar nuevamente las verificaciones. No marcar pruebas pendientes como aprobadas.
