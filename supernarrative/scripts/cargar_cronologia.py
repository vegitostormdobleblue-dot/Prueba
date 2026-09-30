#!/usr/bin/env python3
"""
Carga la cronología canon de murder drones (source/cronologia-canon.md)
en story_facts como hechos 'historical'. Los marcados con ★ llevan
significance 9; el resto 5. established_in_chapter guarda la era.

Uso:
  python3 scripts/cargar_cronologia.py --db db/murder-drones.db
"""

import argparse
import sqlite3
import os

ERAS = {
    "Antes del 3000", "Del 3000 al 3040", "Del 3040 al 3045", "Del 3045 al 3050",
    "Del 3050 al 3070", "3070", "3071", "Final Absoluto",
}


def parse(path):
    era = None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line in ERAS:
            era = line
            continue
        if not era or not line or line[0] not in "•★":
            continue
        yield era, line[0] == "★", line[1:].strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--file", default=os.path.join(os.path.dirname(__file__), "..", "source", "cronologia-canon.md"))
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys=ON")
    pid = conn.execute("SELECT id FROM projects ORDER BY updated_at DESC LIMIT 1").fetchone()[0]

    nuevos = 0
    for era, clave, desc in parse(args.file):
        ya = conn.execute("SELECT 1 FROM story_facts WHERE project_id=? AND description=?", (pid, desc)).fetchone()
        if ya:
            continue
        conn.execute(
            "INSERT INTO story_facts (project_id, category, description, is_true, established_in_chapter, revealed_to_reader_in, significance) "
            "VALUES (?, 'historical', ?, 1, ?, 'canon', ?)",
            (pid, desc, f"canon: {era}", 9 if clave else 5),
        )
        nuevos += 1
    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM story_facts WHERE project_id=? AND category='historical'", (pid,)).fetchone()[0]
    print(f"cargados {nuevos} hechos nuevos, {total} hechos canon en total")


if __name__ == "__main__":
    main()
