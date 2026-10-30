# Preparar el entorno Python

## Plataforma y estado de verificación

El objetivo académico es Raspberry Pi 3/4 con Raspberry Pi OS de 64 bits y Python 3.13. **No se ha verificado ejecución física en Raspberry Pi**. No se anuncia una versión concreta del sistema como compatible hasta comprobarla con los periféricos.

La instalación se comprobó con CPython **3.13.17**, Linux x86-64 y uv. El archivo `uv.lock` fija las dependencias transitivas; `.python-version` selecciona Python 3.13. Una instalación correcta en x86-64 no demuestra funcionamiento ARM64.

| Dependencia directa | Versión | Uso |
| --- | --- | --- |
| RPi.GPIO | 0.7.1 | LED, pulsadores, PWM, temporizadores y HC-SR04 |
| adafruit-circuitpython-dht | 4.0.12 | DHT11 |
| adafruit-circuitpython-ads1x15 | 3.0.5 | ADS1115 |
| rpi-lcd | 0.0.3 | LCD I²C |
| smbus | 1.1.post2 | PCF8591 y LCD |
| paho-mqtt | 2.1.0 | MQTT |
| pymongo[srv] | 3.12.0 | MongoDB |
| python-dotenv | 1.2.2 | Variables de MongoDB |

Estas versiones directas se conservaron respecto al contenido original, salvo la declaración directa de dependencias antes transitivas. El paquete `dotenv` era un intermediario de `python-dotenv`; se usa directamente este último. La compatibilidad de cada componente depende también del sistema y hardware.

## Requisitos del sistema

En Debian/Raspberry Pi OS, instala herramientas y cabeceras cuando una dependencia necesite compilar:

```bash
sudo apt update
sudo apt install python3-dev build-essential libi2c-dev i2c-tools
```

Las cabeceras deben corresponder al intérprete empleado. Si la distribución no incluye Python 3.13, sigue el procedimiento de instalación de Python/uv para tu sistema; no sustituyas el Python del sistema ni utilices `sudo pip`.

Para Blinka/DHT puede ser necesario libgpiod. El nombre del paquete depende de la versión del sistema: compruébalo con `apt-cache search libgpiod` y sigue la [guía del fabricante](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi). No se ha validado aquí un paquete concreto para Raspberry Pi OS.

Activa I²C con `sudo raspi-config` para LCD y ADC y comprueba que existe `/dev/i2c-1`. Verifica permisos de usuario para GPIO/I²C; cierra la sesión y vuelve a entrar si cambias grupos. No ejecutes otros programas sobre los mismos pines.

## Instalación con uv

Instala uv mediante su [documentación oficial](https://docs.astral.sh/uv/getting-started/installation/). Desde la carpeta `Ejemplos/`:

```bash
uv python install 3.13
uv sync --locked --extra mqtt --extra mongodb
```

Para ejemplos físicos, en la Raspberry Pi:

```bash
uv sync --locked --extra hardware
```

Puedes combinar extras en un mismo comando. Al cambiar los extras, uv ajusta el entorno; para disponer de todos utiliza `uv sync --locked --all-extras`. Los comandos de ejecución de cada README indican el extra requerido.

Para comprobar dependencias:

```bash
uv pip check
```

No uses `uv add` para ejecutar una práctica: cambia el manifiesto y el lock.

## Alternativa con pip

Crea un entorno con un intérprete Python 3.13 ya instalado:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "paho-mqtt==2.1.0" "pymongo[srv]==3.12.0" "python-dotenv==1.2.2"
```

En la Raspberry Pi, para hardware:

```bash
python -m pip install "RPi.GPIO==0.7.1" "adafruit-circuitpython-dht==4.0.12" "adafruit-circuitpython-ads1x15==3.0.5" "rpi-lcd==0.0.3" "smbus==1.1.post2"
```

Esta alternativa fija dependencias directas; para reproducir también las transitivas utiliza uv y el lock. Ejecuta los programas con `python carpeta/archivo.py` en el entorno activo; utiliza `deactivate` al terminar.

## Diagnóstico y límites

- `RPi.GPIO` rechaza la importación fuera de una Raspberry Pi; es una limitación esperada, no un resultado de prueba física.
- Que `board`, DHT o ADS1115 se importen no demuestra acceso al bus ni disponibilidad de pines.
- PyMongo 3.12.0 emite una advertencia de obsolescencia por una función de fechas en Python 3.13; no impidió la importación. No se oculta la advertencia ni se declara compatibilidad con futuras versiones de Python.
- La extensión `srv` instala dnspython 1.16.0. Las pruebas locales usan `mongodb://`; no prueban DNS SRV, Atlas ni autenticación externa.
- Los paquetes de Raspberry Pi contienen componentes nativos: repetir instalación y pruebas en ARM64 es obligatorio antes de afirmar compatibilidad completa.
- Mantén `.venv/`, `__pycache__/` y `.env` fuera de Git.

Consulta el [registro de resultados](../REGISTRO_PYTHON.md), las [pruebas](../pruebas/README.md) y las [reglas de conexión GPIO](gpio_y_sensores.md).
