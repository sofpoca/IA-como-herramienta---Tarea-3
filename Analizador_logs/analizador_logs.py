"""Analiza registros con el formato [NIVEL] [YYYY-MM-DD] mensaje.

Solo INFO, WARNING y ERROR al inicio cuentan como eventos. Una línea cuenta
como incompleta si no tiene un nivel reconocido, una fecha ISO válida o un
mensaje. Los eventos con nivel reconocido se cuentan aunque estén incompletos.
"""

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


SEVERITIES = ("INFO", "WARNING", "ERROR")
SEVERITY_PATTERN = re.compile(r"^\[(INFO|WARNING|ERROR)\](?:\s+(.*))?$")
ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_LIKE_PATTERN = re.compile(
    r"^\d{1,4}[-/]\d{1,2}[-/]\d{1,4}(?:[Tt].*)?$"
)


@dataclass
class LineResult:
    severity: Optional[str]
    date_status: str
    date_text: Optional[str]
    message: str
    incomplete: bool


def _is_valid_iso_date(value: str) -> bool:
    if not ISO_DATE_PATTERN.fullmatch(value):
        return False

    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def analyze_line(line: str) -> LineResult:
    """Analiza una línea; las fechas ausentes e inválidas son incompletas."""
    match = SEVERITY_PATTERN.match(line.strip())
    if not match:
        return LineResult(None, "no evaluable", None, "", True)

    severity = match.group(1)
    remainder = (match.group(2) or "").strip()
    parts = remainder.split(maxsplit=1)
    first_token = parts[0] if parts else ""
    trailing_message = parts[1] if len(parts) == 2 else ""

    if first_token and DATE_LIKE_PATTERN.fullmatch(first_token):
        is_valid = _is_valid_iso_date(first_token)
        date_status = "válida" if is_valid else "inválida"
        date_text = first_token
        message = trailing_message
    else:
        date_status = "ausente"
        date_text = None
        message = remainder

    incomplete = date_status != "válida" or not message.strip()
    return LineResult(
        severity, date_status, date_text, message.strip(), incomplete
    )


def analyze_lines(lines: Iterable[str]) -> Tuple[List[LineResult], Dict[str, int], int]:
    results = [analyze_line(line) for line in lines]
    counts = {severity: 0 for severity in SEVERITIES}
    incomplete_count = 0

    for result in results:
        if result.severity:
            counts[result.severity] += 1
        if result.incomplete:
            incomplete_count += 1

    return results, counts, incomplete_count


def select_file() -> Optional[Path]:
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError as exc:
        raise RuntimeError(
            "No se pudo cargar tkinter para abrir el selector de archivos."
        ) from exc

    try:
        root = tk.Tk()
        try:
            root.withdraw()
            selected = filedialog.askopenfilename(
                title="Selecciona el archivo de registros",
                filetypes=[
                    ("Archivos de texto", "*.txt"),
                    ("Todos los archivos", "*.*"),
                ],
            )
        finally:
            root.destroy()
    except tk.TclError as exc:
        raise RuntimeError(
            "No se pudo abrir el selector gráfico de archivos."
        ) from exc

    return Path(selected) if selected else None


def _print_results(
    results: List[LineResult], counts: Dict[str, int], incomplete_count: int
) -> None:
    print("\nDetalle por línea:")
    for number, result in enumerate(results, start=1):
        if result.severity is None:
            severity_text = "no reconocida"
        else:
            severity_text = result.severity

        date_text = result.date_status
        if result.date_text:
            date_text += " ({})".format(result.date_text)

        message_text = result.message or "(vacío)"
        line_status = "incompleta" if result.incomplete else "completa"
        print(
            '  Línea {}: nivel={}, fecha={}, mensaje="{}", estado={}'.format(
                number, severity_text, date_text, message_text, line_status
            )
        )

    total_events = sum(counts.values())
    print("\nResumen:")
    print("  Total de eventos: {}".format(total_events))
    for severity in SEVERITIES:
        print("  {}: {}".format(severity, counts[severity]))
    print("  Líneas incompletas o mal formateadas: {}".format(incomplete_count))


def main() -> None:
    try:
        path = select_file()
    except RuntimeError as exc:
        print("Error: {}".format(exc))
        return

    if path is None:
        print("No se seleccionó ningún archivo.")
        return

    try:
        with path.open("r", encoding="utf-8-sig") as file:
            results, counts, incomplete_count = analyze_lines(file)
    except UnicodeDecodeError:
        print("Error: el archivo no contiene texto UTF-8 válido.")
        return
    except OSError as exc:
        print("Error al leer '{}': {}".format(path, exc))
        return

    print("Archivo analizado: {}".format(path))
    _print_results(results, counts, incomplete_count)


if __name__ == "__main__":
    main()
