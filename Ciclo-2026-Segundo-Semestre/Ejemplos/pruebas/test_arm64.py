"""Compilar y ejecutar ejemplos AArch64 reales mediante QEMU."""

import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    '00_hello_world': 'Semana_03_Entorno_ARM64/ARM64/00_hello_world.s',
    '01_if': 'Semana_06_Control_Flujo_y_Funciones/ARM64/01_if.s',
    '02_while': 'Semana_06_Control_Flujo_y_Funciones/ARM64/02_while.s',
    '05_atoi': 'Semana_06_Control_Flujo_y_Funciones/ARM64/05_atoi.s',
    '06_itoa': 'Semana_06_Control_Flujo_y_Funciones/ARM64/06_itoa.s',
    '10_select_menu': 'Semana_06_Control_Flujo_y_Funciones/ARM64/10_select_menu.s',
    '07_sum_and_subtract': 'Semana_07_Funciones_y_Pila/ARM64/07_sum_and_subtract.s',
    '03_read_file': 'Semana_08_Linux_y_Archivos/ARM64/03_read_file.s',
    '04_process_buffer': 'Semana_08_Linux_y_Archivos/ARM64/04_process_buffer.s',
    '08_read_numbers': 'Semana_08_Linux_y_Archivos/ARM64/08_read_numbers.s',
    '09_read_input': 'Semana_08_Linux_y_Archivos/ARM64/09_read_input.s',
}
INCLUDE_DIRS = (
    ROOT / 'Semana_06_Control_Flujo_y_Funciones/ARM64',
    ROOT / 'Semana_08_Linux_y_Archivos/ARM64',
    ROOT / 'compartidos/ARM64',
)
PROGRAMS = ("00_hello_world", "01_if", "02_while", "03_read_file",
            "04_process_buffer", "07_sum_and_subtract", "09_read_input",
            "10_select_menu")
TOOLS = ("make", "aarch64-linux-gnu-as", "aarch64-linux-gnu-ld", "qemu-aarch64")


@unittest.skipUnless(all(shutil.which(tool) for tool in TOOLS),
                     "Requiere make, binutils AArch64 y QEMU.")
class ARMTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="curso778-arm64-")
        cls.work = Path(cls.temporary.name)
        cls.build = cls.work / "build"
        for program in PROGRAMS:
            subprocess.run(
                ["make", "-f", "Makefile.qemu", f"SRC={SOURCES[program]}",
                 f"BUILD={cls.build}"], cwd=ROOT, check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def execute(self, program, data=b"", fixture=None, fixture_directory=False):
        with tempfile.TemporaryDirectory(prefix="curso778-datos-") as directory:
            cwd = Path(directory)
            (cwd / "datos").mkdir()
            filename = cwd / "datos/lecturas.csv"
            if fixture_directory:
                filename.mkdir()
            elif fixture is not None:
                filename.write_bytes(fixture)
            return subprocess.run(
                ["qemu-aarch64", str(self.build / Path(SOURCES[program]).with_suffix(""))],
                cwd=cwd, input=data, capture_output=True, timeout=5)

    def harness(self, source, fixture=None):
        with tempfile.TemporaryDirectory(prefix="curso778-rutina-") as directory:
            cwd = Path(directory)
            (cwd / "datos").mkdir()
            if fixture is not None:
                (cwd / "datos/lecturas.csv").write_bytes(fixture)
            asm = cwd / "check.s"
            obj = cwd / "check.o"
            exe = cwd / "check"
            asm.write_text(source)
            subprocess.run(["aarch64-linux-gnu-as", "-g", *[flag for directory in INCLUDE_DIRS
                              for flag in ("-I", str(directory))],
                            "-o", str(obj), str(asm)],
                           check=True, capture_output=True)
            subprocess.run(["aarch64-linux-gnu-ld", "-o", str(exe), str(obj)],
                           check=True, capture_output=True)
            return subprocess.run(["qemu-aarch64", str(exe)], cwd=cwd,
                                  capture_output=True, timeout=5)

    def abi_harness(self, includes, setup, call, checks, data=""):
        seed = "\n".join(f"mov x{register}, #{register}" for register in range(19, 30))
        verify = "\n".join(
            f"cmp x{register}, #{register}\nb.ne bad" for register in range(19, 30))
        return f"""
{includes}
.data
{data}
.balign 8
saved_sp: .quad 0
.text
.global _start
_start:
{seed}
ldr x16, =saved_sp
mov x17, sp
str x17, [x16]
{setup}
bl {call}
{checks}
{verify}
ldr x16, =saved_sp
ldr x16, [x16]
mov x17, sp
cmp x16, x17
b.ne bad
mov x0, #0
b finish
bad:
mov x0, #97
finish:
mov x8, #93
svc #0
"""

    def test_basic_programs(self):
        for program, output in (("00_hello_world", b"Hello, World!\n"),
                                ("01_if", b"x es menor o igual que 10\n"),
                                ("02_while", b"")):
            with self.subTest(program=program):
                result = self.execute(program)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, output)

    def test_if_greater_branch_with_test_constant(self):
        source = (ROOT / SOURCES["01_if"]).read_text()
        self.assertIn("mov x0, #5", source)
        result = self.harness(source.replace("mov x0, #5", "mov x0, #11"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"x es mayor que 10\n")

    def test_file_copy_empty_binary_and_multiple_blocks(self):
        for data in (b"", b"10\n20\n$\n", bytes(range(256)) * 40):
            with self.subTest(size=len(data)):
                result = self.execute("03_read_file", fixture=data)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, data)

    def test_process_buffer_sentinel_boundary_and_eof(self):
        for data in (b"", b"10\n20\n", b"10\n$\n20", b"x" * 4096 + b"$fin"):
            with self.subTest(size=len(data)):
                result = self.execute("04_process_buffer", fixture=data)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, data.split(b"$", 1)[0])

    def test_file_open_and_read_failures(self):
        for program in ("03_read_file", "04_process_buffer", "07_sum_and_subtract"):
            for directory in (False, True):
                with self.subTest(program=program, directory=directory):
                    result = self.execute(program, fixture_directory=directory)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(b"Error", result.stderr)

    def test_numbers_empty_zero_crlf_and_optional_sentinel(self):
        cases = ((b"", 0), (b"$", 0), (b"0\n", 0), (b"10\n20\n30\n40\n50\n$\n", 150),
                 (b"\r\n10\r\n20\r\n", 30), (b"10\n20", 30),
                 (b"0\n" * 2048, 0), (b"9223372036854775807\n", 9223372036854775807))
        for data, total in cases:
            with self.subTest(size=len(data), total=total):
                result = self.execute("07_sum_and_subtract", fixture=data)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, f"Suma: {total}\nResta: {-total}\n".encode())

    def test_numbers_reject_invalid_overflow_and_oversize(self):
        cases = (b"-1\n", b"12x\n", b"1 2\n", b"$\n10\n",
                 b"9223372036854775808\n", b"9223372036854775807\n1\n",
                 b"9" * 100, b"0\n" * 2049)
        for data in cases:
            with self.subTest(size=len(data), prefix=data[:25]):
                result = self.execute("07_sum_and_subtract", fixture=data)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertIn(b"Error", result.stderr)

    def test_keyboard_exact_length_and_eof(self):
        for data in (b"", b"hola\n", b"a" * 64, b"b" * 130, b"a\0b\n"):
            with self.subTest(size=len(data)):
                result = self.execute("09_read_input", data=data)
                chunks = [data[i:i + 64] for i in range(0, len(data), 64)]
                expected = b"".join(b"Ingrese un dato: Dato ingresado: " + chunk
                                    for chunk in chunks) + b"Ingrese un dato: "
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, expected)

    def test_menu_valid_invalid_long_and_eof(self):
        cases = ((b"", 0, False), (b"3", 0, True), (b"9\n3\n", 1, True),
                 (b"\n3\n", 1, True), (b"12\n3\n", 1, True),
                 (b"x" * 100 + b"\n3\n", 1, True), (b"3\r\n", 0, True))
        for data, invalid, goodbye in cases:
            with self.subTest(data=data[:20]):
                result = self.execute("10_select_menu", data=data)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.count("Opción inválida\n".encode()), invalid)
                self.assertEqual("Adiós\n".encode() in result.stdout, goodbye)
                if invalid:
                    self.assertNotIn(b"Ingrese una opci\xc3\xb3n: Hola\n", result.stdout)
        result = self.execute("10_select_menu", data=b"1\n2\n3\n")
        self.assertIn(b": Hola\n", result.stdout)
        self.assertIn(b": Mundo\n", result.stdout)

    def test_atoi_bounds_and_preserved_registers(self):
        for text, value, consumed, valid in (
                ("0", 0, 1, True), ("123\n", 123, 3, True),
                ("12x", 12, 2, True), ("9223372036854775807", 9223372036854775807, 19, True),
                ("", 0, 0, False), ("-1", 0, 0, False),
                ("9223372036854775808", 0, 18, False)):
            with self.subTest(text=text):
                raw = ", ".join(str(byte) for byte in text.encode())
                data = "input:\n" + (f".byte {raw}\n" if raw else "") + "input_end:\n.byte 255"
                checks = f"ldr x16, ={value}\ncmp x0, x16\nb.ne bad\n"
                checks += f"ldr x16, =input+{consumed}\ncmp x1, x16\nb.ne bad\n"
                checks += f"cmp x2, #{0 if valid else -1}\nb.ne bad"
                source = self.abi_harness('.include "05_atoi.s"',
                    "ldr x0, =input\nldr x1, =input_end", "atoi", checks, data)
                result = self.harness(source)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_itoa_limits_capacity_guards_and_preserved_registers(self):
        for value, capacity in ((0, 1), (42, 2), (-42, 3),
                                (9223372036854775807, 19),
                                (-9223372036854775808, 20), (42, 1), (0, 0), (-1, 1)):
            with self.subTest(value=value, capacity=capacity):
                text = str(value)
                valid = capacity >= len(text)
                data = f"left: .byte 76\nbuffer: .space {capacity}\nright: .byte 82"
                checks = f"cmp x0, #{0 if valid else -1}\nb.ne bad\n"
                checks += "ldr x16, =left\nldrb w17, [x16]\ncmp w17, #76\nb.ne bad\n"
                checks += "ldr x16, =right\nldrb w17, [x16]\ncmp w17, #82\nb.ne bad\n"
                if valid:
                    checks += f"cmp x2, #{len(text)}\nb.ne bad\n"
                    checks += f"ldr x16, =buffer+{capacity-len(text)}\ncmp x1, x16\nb.ne bad\n"
                    for index, char in enumerate(text):
                        checks += f"ldrb w17, [x1, #{index}]\ncmp w17, #{ord(char)}\nb.ne bad\n"
                source = self.abi_harness('.include "06_itoa.s"',
                    f"ldr x0, ={value}\nldr x2, =buffer\nadd x1, x2, #{capacity}",
                    "itoa", checks, data)
                result = self.harness(source)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_number_reader_capacity_and_preserved_registers(self):
        for data, capacity, expected in ((b"1\n2\n", 2, 2), (b"1\n2\n", 1, -5),
                                         (b"", 2, 0), (b"1x", 2, -4)):
            with self.subTest(data=data, capacity=capacity):
                source = self.abi_harness(
                    '.include "io.s"\n.include "08_read_numbers.s"',
                    f"ldr x0, =vector\nmov x1, #{capacity}", "read_numbers",
                    f"cmp x0, #{expected}\nb.ne bad", "vector: .space 16")
                self.assertEqual(self.harness(source, data).returncode, 0)

    def test_write_failure_is_reported(self):
        with open("/dev/full", "wb") as full:
            result = subprocess.run(
                ["qemu-aarch64", str(self.build / Path(SOURCES["00_hello_world"]).with_suffix(""))],
                stdout=full, stderr=subprocess.PIPE, timeout=5)
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"Error", result.stderr)

    def test_makefiles_reject_auxiliaries_and_track_includes(self):
        result = subprocess.run(
            ["make", "-f", "Makefile.qemu", f"SRC={SOURCES['05_atoi']}"],
            cwd=ROOT, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"auxiliares", result.stderr)
        dependencies = (self.build / Path(SOURCES["07_sum_and_subtract"]).with_suffix(".d")).read_text()
        for filename in ("io.s", "05_atoi.s", "06_itoa.s", "08_read_numbers.s"):
            self.assertIn(filename, dependencies)
        native = subprocess.run(
            ["make", "-f", "Makefile.arm64", "-n", f"BUILD={self.work / 'native'}"],
            cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(native.returncode, 0, native.stderr)
        self.assertIn("as -g", native.stdout)

    def test_rebuild_when_shared_or_weekly_routine_changes(self):
        with tempfile.TemporaryDirectory(prefix="curso778-rebuild-") as directory:
            cwd = Path(directory)
            for source in (*SOURCES.values(), "compartidos/ARM64/io.s", "Makefile.qemu"):
                destination = cwd / source
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / source, destination)
            command = ["make", "-f", "Makefile.qemu",
                       f"SRC={SOURCES['07_sum_and_subtract']}"]
            subprocess.run(command, cwd=cwd, check=True, capture_output=True)
            obj = cwd / "build" / Path(SOURCES["07_sum_and_subtract"]).with_suffix(".o")
            for source in ("compartidos/ARM64/io.s", SOURCES["05_atoi"],
                           SOURCES["06_itoa"], SOURCES["08_read_numbers"]):
                with self.subTest(source=source):
                    self.assertEqual(subprocess.run(command + ["-q"], cwd=cwd).returncode, 0)
                    changed = obj.stat().st_mtime_ns + 1
                    os.utime(cwd / source, ns=(changed, changed))
                    self.assertEqual(subprocess.run(command + ["-q"], cwd=cwd).returncode, 1)
                    result = subprocess.run(command, cwd=cwd, check=True, capture_output=True)
                    self.assertIn(b"aarch64-linux-gnu-as", result.stdout)
                    self.assertEqual(subprocess.run(command + ["-q"], cwd=cwd).returncode, 0)

    @unittest.skipUnless(os.getenv("PRUEBAS_GDB") == "1" and shutil.which("gdb-multiarch"),
                         "Activar PRUEBAS_GDB=1 para sesión TCP real con GDB.")
    def test_real_gdb_loop_counter(self):
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        executable = self.build / Path(SOURCES["02_while"]).with_suffix("")
        emulator = subprocess.Popen(
            ["qemu-aarch64", "-g", str(port), str(executable)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            time.sleep(0.2)
            result = subprocess.run(
                ["gdb-multiarch", "--batch", "-nx", str(executable),
                 "-ex", "set pagination off", "-ex", "set architecture aarch64",
                 "-ex", f"target remote 127.0.0.1:{port}",
                 "-ex", "break finWhile", "-ex", "continue",
                 "-ex", 'printf "contador=%ld\\n", $x0', "-ex", "detach"],
                capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(b"contador=100", result.stdout)
            self.assertEqual(emulator.wait(timeout=5), 0)
        finally:
            if emulator.poll() is None:
                emulator.kill()
            emulator.communicate()


if __name__ == "__main__":
    unittest.main()
