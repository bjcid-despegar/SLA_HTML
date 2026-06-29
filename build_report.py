#!/usr/bin/env python3
"""Incrusta modelo_base_camp.csv y modelo_base_camp_ctr.csv en las plantillas.

Genera los HTML standalone con ambos datasets embebidos:
  - modelo_base_camp.csv      -> SLA, nº de campañas, nº de placements
  - modelo_base_camp_ctr.csv  -> CTR (un registro por placement-mes)
No requiere dependencias externas (solo la librería estándar de Python).
"""
import sys
import pathlib

CSV = "modelo_base_camp.csv"
CSV_CTR = "modelo_base_camp_ctr.csv"
MARKER = "__CSV_PLACEHOLDER__"
MARKER_CTR = "__CSV_CTR_PLACEHOLDER__"
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


def _read_csv(name: str) -> str:
    path = pathlib.Path(name)
    if not path.exists():
        sys.exit(f"ERROR: no se encontró el CSV {name}")
    data = path.read_text(encoding="utf-8-sig")  # tolera BOM
    if "</script" in data.lower():
        sys.exit(f"ERROR: {name} contiene '</script>'; no se puede incrustar de forma segura.")
    return data


def main() -> None:
    csv = _read_csv(CSV)
    csv_ctr = _read_csv(CSV_CTR)

    SITE_DIR.mkdir(exist_ok=True)
    rows = max(0, len([ln for ln in csv.splitlines() if ln.strip()]) - 1)
    rows_ctr = max(0, len([ln for ln in csv_ctr.splitlines() if ln.strip()]) - 1)

    for template, names in BUILDS:
        tpl_path = pathlib.Path(template)
        if not tpl_path.exists():
            sys.exit(f"ERROR: no se encontró la plantilla {template}")
        tpl = tpl_path.read_text(encoding="utf-8")
        if MARKER not in tpl:
            sys.exit(f"ERROR: no se encontró el marcador {MARKER} en {template}")
        out = tpl.replace(MARKER, csv)
        # El marcador de CTR es opcional (plantillas viejas pueden no tenerlo).
        if MARKER_CTR in out:
            out = out.replace(MARKER_CTR, csv_ctr)
        for name in names:
            # UTF-8 sin BOM, sin traducir saltos de línea
            (SITE_DIR / name).write_text(out, encoding="utf-8", newline="")
        print(f"OK: {rows} filas SLA + {rows_ctr} filas CTR incrustadas en {SITE_DIR}/{names[0]}")


if __name__ == "__main__":
    main()
