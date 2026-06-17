#!/usr/bin/env python3
"""Incrusta modelo_base_camp.csv dentro de plantilla_reporte.html.

Genera reporte_camp_base_standalone.html con los datos embebidos.
No requiere dependencias externas (solo la librería estándar de Python).
"""
import sys
import pathlib

TEMPLATE = "plantilla_reporte.html"
CSV = "modelo_base_camp.csv"
MARKER = "__CSV_PLACEHOLDER__"
# Carpeta que GitHub Pages publica. index.html => link limpio (raíz del sitio).
SITE_DIR = pathlib.Path("_site")


def main() -> None:
    tpl_path = pathlib.Path(TEMPLATE)
    csv_path = pathlib.Path(CSV)

    if not tpl_path.exists():
        sys.exit(f"ERROR: no se encontró la plantilla {TEMPLATE}")
    if not csv_path.exists():
        sys.exit(f"ERROR: no se encontró el CSV {CSV}")

    tpl = tpl_path.read_text(encoding="utf-8")
    csv = csv_path.read_text(encoding="utf-8-sig")  # tolera BOM

    if MARKER not in tpl:
        sys.exit(f"ERROR: no se encontró el marcador {MARKER} en {TEMPLATE}")
    if "</script" in csv.lower():
        sys.exit("ERROR: el CSV contiene '</script>'; no se puede incrustar de forma segura.")

    out = tpl.replace(MARKER, csv)

    SITE_DIR.mkdir(exist_ok=True)
    # index.html => el link compartido es la raíz del sitio (.../).
    # También dejamos una copia con nombre descriptivo para descargar.
    for name in ("index.html", "reporte_camp_base_standalone.html"):
        # UTF-8 sin BOM, sin traducir saltos de línea
        (SITE_DIR / name).write_text(out, encoding="utf-8", newline="")

    rows = max(0, len([ln for ln in csv.splitlines() if ln.strip()]) - 1)
    print(f"OK: {rows} filas incrustadas en {SITE_DIR}/index.html")


if __name__ == "__main__":
    main()
