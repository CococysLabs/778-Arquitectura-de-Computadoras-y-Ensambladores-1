"""Verificar fuentes, enlaces, exclusiones y alcance de los cambios."""

from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PREFIX = ROOT.relative_to(REPO).as_posix() + "/"
IGNORED_PARTS = {".venv", "__pycache__", "build"}
files = sorted(path for path in ROOT.rglob("*")
               if path.is_file() and not IGNORED_PARTS.intersection(path.parts))
errors = []
python_count = 0
links = 0
secret_pattern = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    r"|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}"
    r"|AKIA[0-9A-Z]{16}"
    r"|mongodb(?:\+srv)?://[^:\s/]+:[^<@\s]+@"
)
for path in files:
    relative = path.relative_to(ROOT)
    content = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        python_count += 1
        try:
            compile(content, str(relative), "exec")
        except SyntaxError as error:
            errors.append(f"Sintaxis {relative}: {error}")
    if secret_pattern.search(content):
        errors.append(f"Posible secreto en {relative}; revisar sin publicar su valor.")
    if path.name.startswith(".env") and path.name != ".env.example":
        errors.append(f"Archivo de entorno personal incluido: {relative}")
    if path.suffix in {".o", ".pyc", ".so"} or path.name == "output.txt":
        errors.append(f"Archivo generado incluido: {relative}")
    if any(line.rstrip() != line for line in content.splitlines()):
        errors.append(f"Espacios al final de línea: {relative}")
    if path.suffix == ".md":
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", content):
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            pathname, _, anchor = unquote(target).partition("#")
            resolved = (path.parent / pathname).resolve() if pathname else path
            links += 1
            if not resolved.exists():
                errors.append(f"Enlace inexistente en {relative}: {target}")
            elif not resolved.is_relative_to(ROOT):
                errors.append(f"Enlace local fuera del conjunto en {relative}: {target}")
            if anchor and resolved.is_file() and resolved.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", resolved.read_text(), re.M)
                slugs = {re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
                         for heading in headings}
                if anchor not in slugs:
                    errors.append(f"Ancla no encontrada en {relative}: {target}")

base = subprocess.check_output(
    ["git", "merge-base", "main", "HEAD"], cwd=REPO).decode().strip()
changed = subprocess.check_output(
    ["git", "diff", "--name-only", base, "-z"], cwd=REPO).decode().split("\0")
untracked = subprocess.check_output(
    ["git", "ls-files", "--others", "--exclude-standard", "-z"],
    cwd=REPO).decode().split("\0")
paths = sorted(set(filter(None, changed + untracked)))
for path in paths:
    if not path.startswith(PREFIX):
        errors.append(f"Cambio fuera de la ruta autorizada: {path}")
    parts = Path(path).parts
    if "11_proyecto" in parts or re.search(r"(?:parcial|tarea|practica|shell)", Path(path).name, re.I):
        errors.append(f"Material excluido de la migración: {path}")
    if any(part in {".venv", "__pycache__", "build"} for part in parts):
        errors.append(f"Archivo generado sin excluir: {path}")
    if Path(path).suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".o", ".so", ".pyc", ".d"}:
        errors.append(f"Imagen reservada o archivo generado incluido: {path}")
    candidate = REPO / path
    if candidate.is_file() and candidate.read_bytes().startswith(b"\x7fELF"):
        errors.append(f"Ejecutable ELF incluido: {path}")

print(f"Fuentes Python compiladas en memoria: {python_count}")
print(f"Enlaces relativos comprobados: {links}")
print(f"Rutas de cambio dentro del aporte: {len(paths)}")
print("Patrones de secretos: revisión limitada; no sustituye auditoría del historial.")
if errors:
    for error in errors:
        print("FALLO:", error)
    raise SystemExit(1)
print("Verificado correctamente: sintaxis, enlaces locales, formato y alcance.")
