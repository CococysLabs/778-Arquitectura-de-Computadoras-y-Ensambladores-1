"""Verificar conexión a MongoDB mediante ping."""

from pymongo.errors import PyMongoError

from config import create_client


def main():
    try:
        with create_client() as client:
            client.admin.command("ping")
            print("Conexión a MongoDB verificada mediante ping.")
    except (ValueError, PyMongoError):
        raise SystemExit("No se pudo conectar. Revisa MONGODB_URI y la disponibilidad del servicio.")


if __name__ == "__main__":
    main()
