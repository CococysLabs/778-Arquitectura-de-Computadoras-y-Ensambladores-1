"""Insertar una lectura sintética por segundo; no lee sensores físicos."""

import random
import time

from pymongo.errors import PyMongoError

from config import create_client, get_collection


def main():
    try:
        with create_client() as client:
            collection = get_collection(client)
            while True:
                doc = {
                    "sensor": "raspi",
                    "temp": round(random.uniform(20, 30), 1),
                    "hum": random.randint(40, 70),
                    "room": "lab",
                }
                collection.insert_one(doc)
                print(f"Lectura sintética insertada: {doc}")
                time.sleep(1)
    except KeyboardInterrupt:
        print("Programa terminado.")
    except (ValueError, PyMongoError):
        raise SystemExit("No se pudo guardar la simulación. Revisa MongoDB y su configuración.")


if __name__ == "__main__":
    main()
