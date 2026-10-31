# Recursos complementarios

Ejemplos adicionales de temporización, mensajería y almacenamiento de datos.

| Grupo | Qué enseña | Cómo ejecutar desde `Ejemplos/` |
| --- | --- | --- |
| [Temporización](Python/03_timer_task/README.md) | Hilos, Timer, rearme y cierre antes de liberar GPIO. Requiere Pi y LED. | `uv run --locked --extra hardware Recursos_Complementarios/Python/03_timer_task/heartbeat_thread.py` |
| [MQTT](Python/09_mqtt/README.md) | Conexión, publicación, suscripción y MQTT 5. Requiere broker. | `uv run --locked --extra mqtt Recursos_Complementarios/Python/09_mqtt/client.py` |
| [MongoDB](Python/10_mongodb/README.md) | Conexión, inserción, consulta y sensor sintético. Requiere MongoDB y variables de entorno. | `uv run --locked --extra mongodb Recursos_Complementarios/Python/10_mongodb/connect.py` |

Usa Python 3.13 y un único entorno en la raíz. Consulta cada README para los demás programas, datos esperados y configuración; conserva `.env` junto a los scripts de MongoDB y fuera de Git. La preparación común está en la [guía Python](../documentacion/preparar_entorno.md).

La simulación utiliza datos sintéticos. La validación física de temporización y GPIO sigue pendiente.

[Volver al índice](../README.md).
