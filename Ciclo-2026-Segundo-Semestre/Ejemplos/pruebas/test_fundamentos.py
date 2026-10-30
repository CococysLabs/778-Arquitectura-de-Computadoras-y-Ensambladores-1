"""Ejecutar los ejemplos de semana 2 y contrastar sus resultados visibles."""

from pathlib import Path
import subprocess
import sys
import unittest

PYTHON = Path(__file__).resolve().parents[1] / "Semana_02_Fundamentos_Arquitectura/Python"


class FundamentosTests(unittest.TestCase):
    def execute(self, name):
        result = subprocess.run([sys.executable, str(PYTHON / name)],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_bases(self):
        self.assertEqual(self.execute("01_bases_numericas.py"),
                         "Decimal: 42\nBinario: 00101010\nHexadecimal: 2A\n"
                         "Desde binario 00101010: 42\nDesde hexadecimal 2A: 42\n")

    def test_complemento_a_dos(self):
        self.assertEqual(self.execute("02_complemento_a_dos.py"),
                         "-128 -> 10000000 -> sin signo: 128, con signo: -128\n"
                         "  -5 -> 11111011 -> sin signo: 251, con signo: -5\n"
                         "   0 -> 00000000 -> sin signo:   0, con signo: 0\n"
                         " 127 -> 01111111 -> sin signo: 127, con signo: 127\n"
                         "Complemento a dos de 5 en 8 bits: 11111011\n")

    def test_bits(self):
        self.assertEqual(self.execute("03_operaciones_bits.py"),
                         "a:          10101010\nb:          00001111\n"
                         "AND:        00001010\nOR:         10101111\n"
                         "XOR:        10100101\nBorrar b:   10100000\n"
                         "NOT 8 bits: 01010101\nLSL 1:      101010100 (340)\n"
                         "LSL 8 bits: 01010100\nLSR 1:      01010101\n-8 >> 1:    -4\n")

    def test_endianness(self):
        self.assertEqual(self.execute("04_bytes_endianness.py"),
                         "little: 78 56 34 12\nRecuperado (little): 0x12345678\n"
                         "big: 12 34 56 78\nRecuperado (big): 0x12345678\n"
                         "Los bytes se muestran desde el offset 0 hasta el 3; "
                         "no son direcciones físicas.\n")


if __name__ == "__main__":
    unittest.main()
