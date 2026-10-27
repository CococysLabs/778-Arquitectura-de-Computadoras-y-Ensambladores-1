"""Pruebas de lógica con dobles explícitos; no verifican circuitos físicos."""

import contextlib
import io
from pathlib import Path
import runpy
import sys
import threading
import types
import unittest
from unittest.mock import Mock, patch

PYTHON = Path(__file__).resolve().parents[1] / "Python"


class Clock:
    def __init__(self, duration=1.0):
        self.now = 0.0
        self.duration = duration
        self.module = types.ModuleType("time")
        self.module.monotonic = lambda: self.now
        self.module.sleep = self.sleep

    def sleep(self, seconds):
        self.now += seconds
        if self.now >= self.duration:
            raise KeyboardInterrupt


def gpio_module():
    gpio = types.ModuleType("RPi.GPIO")
    for name, value in {"BCM": 11, "OUT": 0, "IN": 1, "LOW": 0,
                        "HIGH": 1, "PUD_UP": 22, "FALLING": 31}.items():
        setattr(gpio, name, value)
    for name in ("setmode", "setup", "output", "cleanup",
                 "add_event_detect", "remove_event_detect"):
        setattr(gpio, name, Mock())
    return gpio


def run_example(relative, modules):
    with patch.dict(sys.modules, modules), contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(str(PYTHON / relative), run_name="__main__")


class GPIOTests(unittest.TestCase):
    def button(self, script, schedule, duration):
        clock = Clock(duration)
        gpio = gpio_module()
        gpio.input = lambda pin: next(
            (level for until, level in schedule if clock.now < until), gpio.HIGH
        )
        rpi = types.ModuleType("RPi")
        rpi.GPIO = gpio
        run_example("01_input_button/" + script,
                    {"time": clock.module, "RPi": rpi, "RPi.GPIO": gpio})
        gpio.cleanup.assert_called_once()
        return [call.args[1] for call in gpio.output.call_args_list]

    def test_held_button_changes_once(self):
        self.assertEqual(self.button("button_polling.py",
                                     [(0.8, 0)], 1.2), [True])

    def test_bounce_is_ignored_and_second_press_counts(self):
        self.assertEqual(self.button(
            "button_polling.py",
            [(0.02, 0), (0.04, 1), (0.5, 0), (0.9, 1), (1.3, 0)], 1.7),
            [True, False])

    def test_short_then_long_press(self):
        self.assertEqual(self.button(
            "button_short_long.py",
            [(0.3, 0), (0.5, 1), (2.2, 0)], 2.5), [True, False])

    def test_callback_unregisters_even_when_setup_fails(self):
        gpio = gpio_module()
        gpio.add_event_detect.side_effect = RuntimeError("detector no disponible")
        rpi = types.ModuleType("RPi")
        rpi.GPIO = gpio
        with self.assertRaisesRegex(RuntimeError, "detector"):
            run_example("01_input_button/button_callback.py",
                        {"RPi": rpi, "RPi.GPIO": gpio})
        gpio.cleanup.assert_called_once()
        gpio.remove_event_detect.assert_not_called()

    def test_rearmed_timer_is_cancelled_before_gpio_cleanup(self):
        gpio = gpio_module()
        timers = []
        class Timer:
            ident = None
            def __init__(self, interval, function):
                self.function = function
                self.cancel = Mock()
                timers.append(self)
            def start(self):
                pass
        fake_threading = types.ModuleType("threading")
        fake_threading.Timer = Timer
        fake_threading.Lock = threading.Lock
        fake_threading.Event = threading.Event
        fake_time = types.ModuleType("time")
        def interrupt(seconds):
            timers[0].function()
            raise KeyboardInterrupt
        fake_time.sleep = interrupt
        rpi = types.ModuleType("RPi")
        rpi.GPIO = gpio
        run_example("03_timer_task/timer_rearm.py",
                    {"RPi": rpi, "RPi.GPIO": gpio, "time": fake_time,
                     "threading": fake_threading})
        self.assertEqual(len(timers), 2)
        timers[-1].cancel.assert_called_once()
        gpio.cleanup.assert_called_once()
        before = gpio.output.call_count
        timers[-1].function()
        self.assertEqual(gpio.output.call_count, before)



class SensorTests(unittest.TestCase):
    def test_dht_failure_waits_for_next_period_and_releases_sensor(self):
        clock = Clock(4.5)
        attempts = []
        class Sensor:
            @property
            def temperature(self):
                attempts.append(clock.now)
                raise RuntimeError("error de lectura")
            def exit(self):
                self.closed = True
        sensor = Sensor()
        board = types.ModuleType("board")
        board.D20 = 20
        dht = types.ModuleType("adafruit_dht")
        dht.DHT11 = lambda pin: sensor
        run_example("04_dht11/dht11_periodic.py",
                    {"time": clock.module, "board": board, "adafruit_dht": dht})
        self.assertEqual(len(attempts), 3)
        self.assertTrue(all(b - a >= 2 for a, b in zip(attempts, attempts[1:])))
        self.assertTrue(sensor.closed)

    def test_pcf8591_discards_old_conversion_and_closes_bus(self):
        bus = Mock()
        bus.read_byte.side_effect = [128, 42]
        smbus = types.ModuleType("smbus")
        smbus.SMBus = lambda number: bus
        output = io.StringIO()
        with patch.dict(sys.modules, {"smbus": smbus, "time": Clock(1).module}):
            with contextlib.redirect_stdout(output):
                runpy.run_path(str(PYTHON / "08_adc/pcf8591.py"), run_name="__main__")
        self.assertIn("42", output.getvalue())
        self.assertNotIn("128", output.getvalue())
        self.assertEqual(bus.read_byte.call_count, 2)
        bus.close.assert_called_once()

    def test_pcf8591_closes_bus_after_io_failure(self):
        bus = Mock()
        bus.write_byte.side_effect = OSError("bus no disponible")
        smbus = types.ModuleType("smbus")
        smbus.SMBus = lambda number: bus
        with self.assertRaises(OSError):
            run_example("08_adc/pcf8591.py", {"smbus": smbus})
        bus.close.assert_called_once()

    def test_ultrasonic_echo_timeouts_and_known_pulse(self):
        for mode in ("low", "high", "pulse"):
            with self.subTest(mode=mode):
                gpio = gpio_module()
                ticks = [0.0]
                clock = types.ModuleType("time")
                def monotonic():
                    ticks[0] += 0.0001
                    return ticks[0]
                clock.monotonic = monotonic
                clock.sleep = lambda seconds: None
                levels = iter([0, 1, 1, 1, 0])
                gpio.input = lambda pin: (
                    0 if mode == "low" else 1 if mode == "high"
                    else next(levels, 0))
                rpi = types.ModuleType("RPi")
                rpi.GPIO = gpio
                with patch.dict(sys.modules, {"time": clock, "RPi": rpi,
                                             "RPi.GPIO": gpio}):
                    namespace = runpy.run_path(str(PYTHON / "07_hc_sr04/hcsr04.py"))
                    sensor = namespace["HCSR04"](23, 24)
                    result = sensor.read()
                    sensor.cleanup()
                if mode == "pulse":
                    self.assertAlmostEqual(result, 5.145)
                else:
                    self.assertIsNone(result)
                gpio.cleanup.assert_called_once_with((23, 24))


class ServiceTests(unittest.TestCase):
    def test_mqtt_callbacks_replace_invalid_utf8(self):
        for script in ("subscribe.py", "sub_pub.py"):
            namespace = runpy.run_path(str(PYTHON / "09_mqtt" / script))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                namespace["on_message"](None, None, types.SimpleNamespace(payload=b"\xff"))
            self.assertIn("\ufffd", output.getvalue())

    def test_mqtt_rejects_wildcard_before_connecting(self):
        import os
        for script in ("publish.py", "subscribe.py", "sub_pub.py"):
            namespace = runpy.run_path(str(PYTHON / "09_mqtt" / script))
            with patch.dict(os.environ, {"MQTT_TOPIC": "demo/#"}):
                with self.assertRaisesRegex(SystemExit, "sin comodines"):
                    namespace["main"]()

    def test_mongodb_validates_uri_and_names_without_connecting(self):
        import os
        with patch.dict(os.environ, {}, clear=True):
            namespace = runpy.run_path(str(PYTHON / "10_mongodb/config.py"))
            with patch("dotenv.load_dotenv", return_value=False):
                namespace = runpy.run_path(str(PYTHON / "10_mongodb/config.py"))
                with self.assertRaisesRegex(ValueError, "MONGODB_URI"):
                    namespace["create_client"]()
                client = Mock()
                with self.assertRaisesRegex(ValueError, "MONGODB_DB"):
                    namespace["get_collection"](client)
                client.__getitem__ = Mock()
                client.__getitem__.assert_not_called()

    def test_mongodb_closes_client_on_service_failure(self):
        from pymongo.errors import ConnectionFailure
        config = types.ModuleType("config")
        client = Mock()
        client.__enter__ = Mock(return_value=client)
        client.__exit__ = Mock(return_value=False)
        client.admin.command.side_effect = ConnectionFailure("no disponible")
        config.create_client = lambda: client
        with patch.dict(sys.modules, {"config": config}):
            with self.assertRaisesRegex(SystemExit, "No se pudo conectar"):
                run_example("10_mongodb/connect.py", {})
        client.__exit__.assert_called_once()

    def test_mongodb_insert_keeps_synthetic_schema_and_closes(self):
        config = types.ModuleType("config")
        client = Mock()
        client.__enter__ = Mock(return_value=client)
        client.__exit__ = Mock(return_value=False)
        collection = Mock()
        collection.insert_many.return_value.inserted_ids = [1, 2, 3, 4]
        config.create_client = lambda: client
        config.get_collection = lambda selected: collection
        with patch.dict(sys.modules, {"config": config}):
            run_example("10_mongodb/insert.py", {})
        docs = collection.insert_many.call_args.args[0]
        self.assertEqual(len(docs), 4)
        self.assertTrue(all("sensor" in doc and "Asensor" not in doc for doc in docs))
        client.__exit__.assert_called_once()


class ResourceTests(unittest.TestCase):
    def test_lcd_bus_closes_even_when_clear_fails(self):
        for script in ("lcd_basic.py", "lcd_multiline.py", "lcd_screens.py"):
            with self.subTest(script=script):
                lcd = Mock()
                lcd.clear.side_effect = OSError("bus interrumpido")
                driver = types.ModuleType("rpi_lcd")
                driver.LCD = Mock(return_value=lcd)
                with self.assertRaisesRegex(OSError, "bus interrumpido"):
                    run_example("05_lcd_i2c/" + script,
                                {"rpi_lcd": driver, "time": Clock(0.1).module})
                lcd.bus.close.assert_called_once()
                self.assertEqual(driver.LCD.call_args.args, (0x27, 1, 16, 2, True))

    def test_ads_releases_i2c_when_device_initialization_fails(self):
        bus = Mock()
        board = types.ModuleType("board")
        board.I2C = lambda: bus
        ads = types.ModuleType("adafruit_ads1x15")
        ads.ADS1115 = Mock(side_effect=OSError("dispositivo ausente"))
        ads.AnalogIn = Mock()
        ads.ads1x15 = types.SimpleNamespace(Pin=types.SimpleNamespace(A3=3))
        with self.assertRaisesRegex(OSError, "dispositivo ausente"):
            run_example("08_adc/ads1115.py", {"board": board, "adafruit_ads1x15": ads})
        bus.deinit.assert_called_once()

    def test_callback_does_not_touch_gpio_after_cleanup(self):
        clock = Clock(0.1)
        gpio = gpio_module()
        rpi = types.ModuleType("RPi")
        rpi.GPIO = gpio
        namespace = run_example("01_input_button/button_callback.py",
                                {"RPi": rpi, "RPi.GPIO": gpio, "time": clock.module})
        gpio.remove_event_detect.assert_called_once_with(17)
        namespace["on_button"](17)
        gpio.output.assert_not_called()

    def test_heartbeat_stops_worker_before_cleanup(self):
        gpio = gpio_module()
        toggled = threading.Event()
        gpio.output.side_effect = lambda *args: toggled.set()
        clock = types.ModuleType("time")
        def interrupt(seconds):
            self.assertTrue(toggled.wait(1), "El hilo no ejecutó la tarea.")
            raise KeyboardInterrupt
        clock.sleep = interrupt
        rpi = types.ModuleType("RPi")
        rpi.GPIO = gpio
        namespace = run_example("03_timer_task/heartbeat_thread.py",
                                {"RPi": rpi, "RPi.GPIO": gpio, "time": clock})
        self.assertFalse(namespace["thread"].is_alive())
        gpio.cleanup.assert_called_once()

    def test_mqtt_connection_failure_is_nonzero_and_closes(self):
        from paho.mqtt import client as mqtt
        for script in ("client.py", "subscribe.py", "sub_pub.py"):
            with self.subTest(script=script):
                client = Mock()
                client.connect.side_effect = OSError("conexión rechazada")
                namespace = runpy.run_path(str(PYTHON / "09_mqtt" / script))
                with patch.object(mqtt, "Client", return_value=client):
                    with self.assertRaisesRegex(SystemExit, "MQTT|suscripción"):
                        namespace["main"]()
                client.disconnect.assert_called_once()

if __name__ == "__main__":
    unittest.main()
