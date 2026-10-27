"""Insertar documentos sintéticos, incluido uno sin campo de temperatura."""

from pprint import pprint

from pymongo.errors import PyMongoError

from config import create_client, get_collection


def main():
    try:
        with create_client() as client:
            collection = get_collection(client)
            docs = [
                {"sensor": "raspi-01", "temp": 23.5, "room": "lab"},
                {"sensor": "raspi-02", "temp": 22.1, "room": "lab"},
                {"sensor": "esp32-01", "room": "oficina"},
                {"sensor": "esp32-02", "temp": 26.3, "room": "oficina"},
            ]
            result = collection.insert_many(docs)
            print(f"Documentos insertados: {len(result.inserted_ids)}")
            pprint(result.inserted_ids)
    except (ValueError, PyMongoError):
        raise SystemExit("No se pudo insertar. Revisa la configuración y el servicio MongoDB.")


if __name__ == "__main__":
    main()
