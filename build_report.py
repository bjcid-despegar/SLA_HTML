#!/usr/bin/env python3
"""Incrusta modelo_base_camp.csv dentro de plantilla_reporte.html.

Genera reporte_camp_base_standalone.html con los datos embebidos.
No requiere dependencias externas (solo la librería estándar de Python).
"""
import sys
import pathlib

CSV = "modelo_base_camp.csv"
MARKER = "__CSV_PLACEHOLDER__"
# Carpeta que GitHub Pages publica. index.html => link limpio (raíz del sitio).
SITE_DIR = pathlib.Path("_site")

# (plantilla, [nombres de salida]).
#  - base: vista completa con segmentación por carga (miembro del equipo).
#  - managers: misma estructura sin la segmentación por carga (resultado general).
BUILDS = [
    ("plantilla_reporte.html",
     ["index.html", "reporte_camp_base_standalone.html"]),
    ("plantilla_reporte_managers.html",
     ["reporte_camp_managers_standalone.html"]),
]


def main() -> None:
    csv_path = pathlib.Path(CSV)
    if not csv_path.exists():
        sys.exit(f"ERROR: no se encontró el CSV {CSV}")

    csv = csv_path.read_text(encoding="utf-8-sig")  # tolera BOM
    if "</script" in csv.lower():
        sys.exit("ERROR: el CSV contiene '</script>'; no se puede incrustar de forma segura.")

    SITE_DIR.mkdir(exist_ok=True)
    rows = max(0, len([ln for ln in csv.splitlines() if ln.strip()]) - 1)

    for template, names in BUILDS:
        tpl_path = pathlib.Path(template)
        if not tpl_path.exists():
            sys.exit(f"ERROR: no se encontró la plantilla {template}")
        tpl = tpl_path.read_text(encoding="utf-8")
        if MARKER not in tpl:
            sys.exit(f"ERROR: no se encontró el marcador {MARKER} en {template}")
        out = tpl.replace(MARKER, csv)
        for name in names:
            # UTF-8 sin BOM, sin traducir saltos de línea
            (SITE_DIR / name).write_text(out, encoding="utf-8", newline="")
        print(f"OK: {rows} filas incrustadas en {SITE_DIR}/{names[0]}")


if __name__ == "__main__":
    main()
