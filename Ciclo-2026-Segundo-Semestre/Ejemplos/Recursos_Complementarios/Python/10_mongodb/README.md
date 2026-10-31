# Persistencia de documentos en MongoDB

## Objetivo y funcionamiento

Conectar a una base de laboratorio, insertar documentos sintéticos, consultar campos y guardar lecturas simuladas. No se accede a sensores físicos.

| Archivo | Función |
| --- | --- |
| `connect.py` | Verifica conexión mediante ping. |
| `insert.py` | Inserta cuatro documentos; uno carece de temperatura. |
| `query.py` | Lista, filtra, proyecta campos y ordena por temperatura. |
| `simulate_sensor.py` | Inserta temperatura y humedad aleatorias una vez por segundo. |
| `config.py` | Auxiliar común: carga configuración y valida campos requeridos. No se ejecuta por separado. |

## Requisitos

Python 3.13 y un servicio MongoDB de laboratorio **5.0 o posterior**, porque se declara Stable API 1. Los ejemplos conservan PyMongo 3.12.0; sus comprobaciones y límites se detallan en la [guía del entorno](../../../documentacion/preparar_entorno.md).

## Conexiones físicas

No requiere GPIO, Raspberry Pi ni sensores. Requiere conectividad al servicio MongoDB.

## Instalación

Desde `Ejemplos/`:

```bash
uv sync --locked --extra mongodb
test -e Recursos_Complementarios/Python/10_mongodb/.env || cp Recursos_Complementarios/Python/10_mongodb/.env.example Recursos_Complementarios/Python/10_mongodb/.env
```

Copia la plantilla solo si todavía no tienes un archivo `.env` propio. En él revisa:

```dotenv
MONGODB_URI=mongodb://127.0.0.1:27017/?appName=Curso778
MONGODB_DB=curso778_demo
MONGODB_COLLECTION=sensores
```

El archivo `.env` se busca junto a `config.py`, independientemente del directorio actual. Las variables ya definidas en la terminal tienen prioridad. No publiques `.env`, claves ni datos reales. Los nombres de base y colección son obligatorios para las operaciones con documentos.

## Ejecución

Desde `Ejemplos/`, con MongoDB iniciado:

```bash
uv run --locked --extra mongodb Recursos_Complementarios/Python/10_mongodb/connect.py
uv run --locked --extra mongodb Recursos_Complementarios/Python/10_mongodb/insert.py
uv run --locked --extra mongodb Recursos_Complementarios/Python/10_mongodb/query.py
uv run --locked --extra mongodb Recursos_Complementarios/Python/10_mongodb/simulate_sensor.py
```

Detén el simulador con Ctrl+C; cierra el cliente al salir.

## Resultados esperados

El ping confirma conectividad. La inserción crea cuatro documentos y muestra sus identificadores, que varían por ejecución. La consulta muestra dos documentos de la sala `lab` después de una única inserción y la proyección omite `_id`. El documento sin `temp` conserva ese campo ausente.

El simulador genera temperaturas de 20 a 30 °C y humedad entera de 40 a 70 %. Son estímulos sintéticos, no mediciones verificadas.

## Limitaciones y seguridad

Cada nueva ejecución de `insert.py` añade otros cuatro documentos. El simulador continúa escribiendo hasta detenerse: utiliza una base desechable y controla su crecimiento. No elimina registros automáticamente.

La URI predeterminada es local y no incorpora autenticación; no expongas un servicio así a Internet. Los fallos de selección de servidor tienen un límite de espera de 5 s; la duración total puede incluir otras operaciones del controlador.

PyMongo 3.12.0 es antiguo y emite una advertencia deprecada en Python 3.13. Se mantiene para evitar una migración innecesaria de API; una actualización futura exige repetir las pruebas. El soporte físico de Raspberry Pi no se deduce de una ejecución x86-64.

## Problemas frecuentes

- Falta configuración: completa `MONGODB_URI`, `MONGODB_DB` y `MONGODB_COLLECTION`.
- Conexión fallida: comprueba puerto, servicio y autenticación; los errores no imprimen la URI para evitar exponer secretos.
- Consulta vacía: ejecuta antes `insert.py` en la misma base y colección.
- Documentos repetidos: las inserciones son acumulativas; utiliza otra base de laboratorio si deseas comenzar de nuevo.
- URI `mongodb+srv://`: requiere DNS y acceso externo. Las comprobaciones locales utilizan `mongodb://`; no acreditan Atlas ni infraestructura institucional.
