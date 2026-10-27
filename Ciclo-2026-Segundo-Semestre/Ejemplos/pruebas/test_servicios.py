"""Integración opcional con servicios reales, locales y desechables."""

import contextlib
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import time
import unittest
import uuid

PYTHON = Path(__file__).resolve().parents[1] / "Python"


def wait_line(process, text, timeout=12):
    deadline = time.monotonic() + timeout
    lines = []
    while time.monotonic() < deadline:
        if select.select([process.stdout], [], [], 0.1)[0]:
            line = process.stdout.readline()
            if not line:
                break
            lines.append(line)
            if text in line:
                return "".join(lines)
    raise AssertionError(f"No apareció {text!r}: {''.join(lines)}")


@contextlib.contextmanager
def listening(script, env):
    process = subprocess.Popen(
        [sys.executable, "-u", str(PYTHON / script)], env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        yield process
    finally:
        if process.poll() is None:
            process.send_signal(signal.SIGINT)
        try:
            output, error = process.communicate(timeout=8)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()
            raise AssertionError("El programa no cerró después de Ctrl+C.")
        if process.returncode != 0:
            raise AssertionError(f"Código {process.returncode}: {output} {error}")


@unittest.skipUnless(os.getenv("PRUEBAS_SERVICIOS") == "1",
                     "Requiere servicios locales y PRUEBAS_SERVICIOS=1.")
class RealServicesTests(unittest.TestCase):
    def mqtt_env(self):
        env = dict(os.environ)
        env["MQTT_HOST"] = "127.0.0.1"
        env["MQTT_PORT"] = os.getenv("PRUEBA_MQTT_PORT", "18883")
        env["MQTT_TOPIC"] = "curso778/prueba/" + uuid.uuid4().hex
        return env

    def run_script(self, script, env):
        result = subprocess.run([sys.executable, str(PYTHON / script)], env=env,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_real_mqtt_connection(self):
        self.assertIn("Desconectado", self.run_script("09_mqtt/client.py", self.mqtt_env()))

    def test_real_publish_and_subscribe(self):
        env = self.mqtt_env()
        with listening("09_mqtt/subscribe.py", env) as subscriber:
            wait_line(subscriber, "Suscripción confirmada")
            self.run_script("09_mqtt/publish.py", env)
            self.assertIn("Hola MQTT", wait_line(subscriber, "Mensaje recibido"))

    def test_real_mqtt5_no_local_and_peer_message(self):
        from paho.mqtt.publish import single
        env = self.mqtt_env()
        with listening("09_mqtt/sub_pub.py", env) as process:
            wait_line(process, "Conectado y suscrito")
            single(env["MQTT_TOPIC"], "mensaje de otro cliente",
                   hostname="127.0.0.1", port=int(env["MQTT_PORT"]))
            output = wait_line(process, "mensaje de otro cliente")
            self.assertNotIn("Recibido: Mensaje ", output)

    def test_real_mongo_insert_query_and_simulation(self):
        from pymongo import MongoClient
        env = dict(os.environ)
        port = int(os.getenv("PRUEBA_MONGO_PORT", "27078"))
        env.update(MONGODB_URI=f"mongodb://127.0.0.1:{port}/?appName=Curso778Pruebas",
                   MONGODB_DB="curso778_prueba_" + uuid.uuid4().hex,
                   MONGODB_COLLECTION="sensores")
        with MongoClient(env["MONGODB_URI"], serverSelectionTimeoutMS=5000) as client:
            client.admin.command("ping")
            try:
                self.assertIn("verificada", self.run_script("10_mongodb/connect.py", env))
                self.run_script("10_mongodb/insert.py", env)
                collection = client[env["MONGODB_DB"]][env["MONGODB_COLLECTION"]]
                self.assertEqual(collection.count_documents({}), 4)
                output = self.run_script("10_mongodb/query.py", env)
                self.assertIn("raspi-01", output)
                self.assertIn("Temperatura en orden descendente", output)
                with listening("10_mongodb/simulate_sensor.py", env) as process:
                    wait_line(process, "Lectura sintética insertada")
                doc = collection.find_one({"sensor": "raspi"})
                self.assertIsNotNone(doc)
                self.assertTrue(20 <= doc["temp"] <= 30)
                self.assertTrue(40 <= doc["hum"] <= 70)
            finally:
                # La base de prueba tiene un nombre único y no contiene datos del usuario.
                client.drop_database(env["MONGODB_DB"])


if __name__ == "__main__":
    unittest.main()
