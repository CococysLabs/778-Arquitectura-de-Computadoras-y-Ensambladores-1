"""Consultar los documentos sintéticos insertados mediante insert.py."""

from pprint import pprint

from pymongo.errors import PyMongoError

from config import create_client, get_collection


def main():
    try:
        with create_client() as client:
            collection = get_collection(client)
            print("1) Todos los documentos")
            for doc in collection.find():
                pprint(doc)
            print("\n2) Documentos de la sala lab")
            for doc in collection.find({"room": "lab"}):
                pprint(doc)
            print("\n3) Proyección de sensor y temperatura")
            for doc in collection.find({}, {"_id": 0, "sensor": 1, "temp": 1}):
                pprint(doc)
            print("\n4) Temperatura en orden descendente")
            for doc in collection.find().sort("temp", -1):
                pprint(doc)
    except (ValueError, PyMongoError):
        raise SystemExit("No se pudo consultar. Revisa la configuración y el servicio MongoDB.")


if __name__ == "__main__":
    main()
