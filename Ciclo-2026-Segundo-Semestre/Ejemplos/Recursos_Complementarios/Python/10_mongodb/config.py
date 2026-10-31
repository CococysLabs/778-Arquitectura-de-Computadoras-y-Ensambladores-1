"""Configuración común de los ejemplos MongoDB; no ejecuta consultas al importar."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def create_client():
    load_dotenv(Path(__file__).with_name(".env"))
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        raise ValueError("Falta MONGODB_URI. Configura .env o la variable de entorno.")
    return MongoClient(uri, server_api=ServerApi("1"),
                       serverSelectionTimeoutMS=5000, connect=False)


def get_collection(client):
    database = os.getenv("MONGODB_DB", "").strip()
    collection = os.getenv("MONGODB_COLLECTION", "").strip()
    if not database or not collection:
        raise ValueError("Configura MONGODB_DB y MONGODB_COLLECTION antes de consultar.")
    return client[database][collection]
