#!/usr/bin/env python3
"""
Carga un fanfic desde su semilla (source/<fanfic>/datos.json) en la base del
fanfic, que es una copia de db/murder-drones.db. El canon no se toca nunca.

datos.json es la fuente de todo lo propio del fanfic. Se puede correr las
veces que haga falta:
- personajes, lugares, capitulos, hechos, conocimiento, hilos, pistas,
  relaciones y notas se agregan o se actualizan;
- escenas (por capitulo), eventos de la cronologia, beats de cada hilo y
  reglas del usuario se reemplazan completos si cambiaron.

Lo que no dice "capitulo" es del capitulo 1. Para lo de un capitulo nuevo se
pone "capitulo": N en el item (escenas, cronologia, hechos, conocimiento,
beats, pistas, relaciones, notas).

Uso:
  python3 scripts/cargar_fanfic.py --db db/neutral-frisk.db --dry-run   (ver cambios)
  python3 scripts/cargar_fanfic.py --db db/neutral-frisk.db             (guardar)
Si la base no existe la crea copiando el canon.
"""

import argparse
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CANON = "murder-drones.db"


def salir(msg):
    print(json.dumps({"status": "error", "message": msg}, ensure_ascii=False))
    sys.exit(1)


def js(valor):
    return json.dumps(valor, ensure_ascii=False) if valor is not None else None


class Cargador:
    def __init__(self, conn, datos, slug):
        self.conn = conn
        self.d = datos
        self.slug = slug
        fila = conn.execute("SELECT id FROM projects ORDER BY updated_at DESC LIMIT 1").fetchone()
        if not fila:
            salir("la base no tiene proyecto")
        self.pid = fila["id"]
        self.cambios = {}
        self.insertados = set()
        self.cambio = False
        self.caps = {}
        self.pers = {}
        self.lugares = {}
        self.hilos = {}

    # ---------------------------------------------------------------- utilidades

    def anotar(self, tabla, que, etiqueta):
        self.cambios.setdefault(tabla, {}).setdefault(que, []).append(etiqueta)

    def upsert(self, tabla, donde, campos, etiqueta):
        """Busca la fila por `donde`; si existe actualiza solo lo distinto."""
        cond = " AND ".join(f"{k} = ?" for k in donde)
        cols = ", ".join(["id"] + list(campos))
        fila = self.conn.execute(f"SELECT {cols} FROM {tabla} WHERE {cond}", tuple(donde.values())).fetchone()
        if fila:
            distintos = {k: v for k, v in campos.items() if fila[k] != v}
            self.cambio = bool(distintos)
            if distintos:
                sets = ", ".join(f"{k} = ?" for k in distintos)
                self.conn.execute(f"UPDATE {tabla} SET {sets} WHERE id = ?", (*distintos.values(), fila["id"]))
                if (tabla, fila["id"]) not in self.insertados:
                    self.anotar(tabla, "actualizados", etiqueta)
            return fila["id"]
        todo = {**donde, **campos}
        cur = self.conn.execute(
            f"INSERT INTO {tabla} ({', '.join(todo)}) VALUES ({', '.join('?' for _ in todo)})",
            tuple(todo.values()),
        )
        nuevo = self.conn.execute(f"SELECT id FROM {tabla} WHERE rowid = ?", (cur.lastrowid,)).fetchone()["id"]
        self.insertados.add((tabla, nuevo))
        self.cambio = True
        self.anotar(tabla, "nuevos", etiqueta)
        return nuevo

    def cap(self, item, clave="capitulo"):
        n = item.get(clave, 1) if isinstance(item, dict) else item
        if n is None:
            return None
        n = int(n)
        if n not in self.caps:
            fila = self.conn.execute(
                "SELECT id FROM chapters WHERE project_id = ? AND chapter_number = ?", (self.pid, n)
            ).fetchone()
            if not fila:
                salir(f"el capitulo {n} no esta en 'capitulos'")
            self.caps[n] = fila["id"]
        return self.caps[n]

    def personaje(self, nombre):
        if nombre not in self.pers:
            fila = self.conn.execute(
                "SELECT id FROM characters WHERE project_id = ? AND name = ?", (self.pid, nombre)
            ).fetchone()
            if not fila:
                salir(f"personaje desconocido: {nombre}")
            self.pers[nombre] = fila["id"]
        return self.pers[nombre]

    def lugar(self, nombre):
        if not nombre:
            return None
        if nombre not in self.lugares:
            salir(f"lugar desconocido: {nombre}")
        return self.lugares[nombre]

    def hilo(self, nombre):
        if nombre not in self.hilos:
            salir(f"hilo desconocido: {nombre}")
        return self.hilos[nombre]

    def hecho(self, local):
        return f"{self.slug}:{local}"

    def reemplazar(self, etiqueta, tabla, viejos, nuevos, borrar, insertar):
        """Reemplaza un grupo de filas solo si el contenido cambio."""
        if viejos == nuevos:
            return
        borrar()
        insertar()
        self.anotar(tabla, "reemplazados" if viejos else "nuevos", etiqueta)

    # ---------------------------------------------------------------- secciones

    def proyecto(self):
        p = self.d["proyecto"]
        campos = {k: p[k] for k in ("name", "description", "genre", "narrative_voice", "target_word_count") if k in p}
        self.upsert("projects", {"id": self.pid}, campos, p["name"])
        if self.cambio:
            self.conn.execute("UPDATE projects SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (self.pid,))

    def cargar_lugares(self):
        for l in self.d.get("lugares", []):
            self.lugares[l["name"]] = self.upsert(
                "locations", {"project_id": self.pid, "name": l["name"]},
                {"description": l.get("description")}, l["name"],
            )
        for l in self.d.get("lugares", []):
            self.upsert(
                "locations", {"id": self.lugares[l["name"]]},
                {"parent_location_id": self.lugar(l.get("parent"))}, l["name"],
            )

    def cargar_capitulos(self):
        eventos = {}
        for e in self.d.get("cronologia", []):
            eventos.setdefault(int(e.get("capitulo", 1)), []).append(e["titulo"])
        for c in self.d.get("capitulos", []):
            n = int(c["chapter_number"])
            ruta = c.get("file_path")
            palabras = 0
            if ruta and os.path.exists(os.path.join(RAIZ, ruta)):
                with open(os.path.join(RAIZ, ruta), encoding="utf-8") as f:
                    palabras = len(f.read().split())
            campos = {k: c.get(k) for k in (
                "title", "summary", "status", "scene_type", "tension_level", "pacing", "emotional_tone",
                "story_date", "story_time_start", "story_time_end", "opening_hook", "closing_hook", "file_path",
            )}
            campos.update(word_count=palabras, chapter_order=n, key_events=js(eventos.get(n)))
            self.caps[n] = self.upsert("chapters", {"project_id": self.pid, "chapter_number": n}, campos, f"cap {n}")

    def cargar_personajes(self):
        for p in self.d.get("personajes", []):
            campos = {k: p.get(k) for k in (
                "full_name", "role", "description_physical", "description_psychological", "backstory",
                "motivation", "secret", "flaw", "arc_summary", "voice_notes", "speech_patterns",
                "status", "emotional_state",
            )}
            campos["aliases"] = js(p.get("aliases"))
            campos["current_location_id"] = self.lugar(p.get("location"))
            campos["introduced_in_chapter"] = self.cap(p)
            self.pers[p["name"]] = self.upsert(
                "characters", {"project_id": self.pid, "name": p["name"]}, campos, p["name"]
            )
        # personajes canon: solo cambia como estan y donde
        for p in self.d.get("estado_canon", []):
            campos = {}
            if "emotional_state" in p:
                campos["emotional_state"] = p["emotional_state"]
            if "location" in p:
                campos["current_location_id"] = self.lugar(p["location"])
            if "status" in p:
                campos["status"] = p["status"]
            self.upsert("characters", {"id": self.personaje(p["name"])}, campos, p["name"])
        for c in self.d.get("capitulos", []):
            if c.get("pov"):
                self.upsert("chapters", {"id": self.cap(c["chapter_number"])},
                            {"pov_character_id": self.personaje(c["pov"])}, f"cap {c['chapter_number']}")

    def cargar_escenas(self):
        por_cap = {}
        for e in self.d.get("escenas", []):
            por_cap.setdefault(int(e.get("capitulo", 1)), []).append(e)
        for n, escenas in sorted(por_cap.items()):
            cid = self.cap(n)
            nuevas = [
                (int(e["n"]), self.lugar(e.get("lugar")), js([self.personaje(x) for x in e.get("personajes", [])]),
                 e.get("resumen"), e.get("proposito"))
                for e in escenas
            ]
            viejas = [tuple(r) for r in self.conn.execute(
                "SELECT scene_number, location_id, characters_present, summary, purpose FROM scenes "
                "WHERE chapter_id = ? ORDER BY scene_order", (cid,)
            ).fetchall()]

            def borrar():
                self.conn.execute("DELETE FROM scenes WHERE chapter_id = ?", (cid,))

            def insertar():
                for s in nuevas:
                    self.conn.execute(
                        "INSERT INTO scenes (chapter_id, scene_number, location_id, characters_present, summary, purpose, scene_order) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)", (cid, *s, s[0]),
                    )

            self.reemplazar(f"cap {n}", "scenes", viejas, nuevas, borrar, insertar)
            # personajes canon: primer capitulo donde aparecen
            for x in dict.fromkeys(x for e in escenas for x in e.get("personajes", [])):
                cur = self.conn.execute(
                    "UPDATE characters SET introduced_in_chapter = ? WHERE id = ? AND introduced_in_chapter IS NULL",
                    (cid, self.personaje(x)),
                )
                if cur.rowcount:
                    self.anotar("characters", "actualizados", f"{x} (aparece en cap {n})")

    def cargar_cronologia(self):
        cron = self.d.get("cronologia", [])
        caps = sorted({int(e.get("capitulo", 1)) for e in cron})
        nuevos = []
        for e in sorted(cron, key=lambda e: int(e.get("capitulo", 1))):
            desc = f"[{e['titulo']}] {e['texto']}"
            if e.get("revelado"):
                desc += f" [se cuenta en {e['revelado']}]"
            nuevos.append((self.cap(e), e["tipo"], desc, e["era"],
                           js([self.personaje(x) for x in e.get("personajes", [])])))
        ids = [self.cap(n) for n in caps]
        marcas = ", ".join("?" for _ in ids)
        viejos = [tuple(r) for r in self.conn.execute(
            f"SELECT we.chapter_id, we.event_type, we.description, we.story_timestamp, we.affected_entities "
            f"FROM world_events we JOIN chapters ch ON ch.id = we.chapter_id "
            f"WHERE we.project_id = ? AND we.chapter_id IN ({marcas}) ORDER BY ch.chapter_number, we.rowid",
            (self.pid, *ids),
        ).fetchall()] if ids else []

        def borrar():
            self.conn.execute(f"DELETE FROM world_events WHERE project_id = ? AND chapter_id IN ({marcas})", (self.pid, *ids))

        def insertar():
            for ev in nuevos:
                self.conn.execute(
                    "INSERT INTO world_events (project_id, chapter_id, event_type, description, story_timestamp, affected_entities) "
                    "VALUES (?, ?, ?, ?, ?, ?)", (self.pid, *ev),
                )

        self.reemplazar("cronologia", "world_events", viejos, nuevos, borrar, insertar)

    def cargar_hechos(self):
        lector = {}
        for k in self.d.get("conocimiento", []):
            if k["quien"] == "__reader__" and k["nivel"] in ("knows", "partial"):
                lector[k["hecho"]] = self.cap(k)
        for h in self.d.get("hechos", []):
            revelado = self.cap(h, "revelado_en") if "revelado_en" in h else lector.get(h["id"])
            self.upsert("story_facts", {"id": self.hecho(h["id"])}, {
                "project_id": self.pid,
                "category": h["category"],
                "description": h["description"],
                "is_true": 1 if h.get("is_true", True) else 0,
                "significance": h.get("significance", 5),
                "established_in_chapter": self.cap(h),
                "revealed_to_reader_in": revelado,
            }, h["id"])
        for h in self.d.get("hechos", []):
            self.upsert("story_facts", {"id": self.hecho(h["id"])},
                        {"contradiction_of": self.hecho(h["contradicts"]) if h.get("contradicts") else None}, h["id"])

    def cargar_conocimiento(self):
        for k in self.d.get("conocimiento", []):
            quien = k["quien"] if k["quien"] == "__reader__" else self.personaje(k["quien"])
            como = k.get("como")
            if como and como.startswith("told_by:"):
                como = "told_by:" + self.personaje(como.split(":", 1)[1])
            self.upsert("knowledge_states", {"knower_id": quien, "fact_id": self.hecho(k["hecho"])}, {
                "project_id": self.pid,
                "knowledge_level": k["nivel"],
                "wrong_belief_detail": k.get("detalle"),
                "how_learned": como,
                "learned_in_chapter": self.cap(k),
                "confidence": k.get("confianza", "certain"),
                "notes": k.get("notas"),
            }, f"{k['quien']} / {k['hecho']}")

    def cargar_hilos(self):
        hilos = self.d.get("hilos", [])
        total = sum(len(h.get("beats", [])) for h in hilos)
        base = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(seconds=total + 1)
        paso = 0
        for h in hilos:
            planeado = h.get("status") == "planned"
            self.hilos[h["name"]] = tid = self.upsert(
                "plot_threads", {"project_id": self.pid, "name": h["name"]}, {
                    "description": h.get("description"),
                    "thread_type": h["thread_type"],
                    "status": h["status"],
                    "priority": h.get("priority", 5),
                    "notes": h.get("notes") or None,
                    "planted_in_chapter": None if planeado else self.cap(h, "plantado") if "plantado" in h else self.cap(1),
                    "target_resolution_chapter": self.cap(h["objetivo"]) if h.get("objetivo") else None,
                    "resolved_in_chapter": self.cap(h["resolved"]) if h.get("resolved") else None,
                }, h["name"])
            beats = sorted(h.get("beats", []), key=lambda b: int(b.get("capitulo", 1)))
            nuevos = [(self.cap(b), b["beat_type"], b["description"], b.get("impact", 5)) for b in beats]
            viejos = [tuple(r) for r in self.conn.execute(
                "SELECT chapter_id, beat_type, description, impact_level FROM thread_beats "
                "WHERE thread_id = ? ORDER BY created_at, rowid", (tid,)
            ).fetchall()]

            def borrar(tid=tid):
                self.conn.execute("DELETE FROM thread_beats WHERE thread_id = ?", (tid,))

            def insertar(tid=tid, nuevos=nuevos):
                nonlocal paso
                for b in nuevos:
                    paso += 1
                    cuando = (base + timedelta(seconds=paso)).strftime("%Y-%m-%d %H:%M:%S")
                    self.conn.execute(
                        "INSERT INTO thread_beats (thread_id, chapter_id, beat_type, description, impact_level, created_at) "
                        "VALUES (?, ?, ?, ?, ?, ?)", (tid, *b, cuando),
                    )

            self.reemplazar(h["name"], "thread_beats", viejos, nuevos, borrar, insertar)

    def cargar_pistas(self):
        for p in self.d.get("pistas", []):
            refuerzos = p.get("reforzada_en")
            self.upsert("clues", {"project_id": self.pid, "description": p["description"]}, {
                "thread_id": self.hilo(p["hilo"]) if p.get("hilo") else None,
                "planted_in_chapter": self.cap(p),
                "clue_type": p["clue_type"],
                "subtlety": p["subtlety"],
                "mechanism": p.get("mechanism"),
                "intended_resolution": p.get("intended_resolution"),
                "resolved_in_chapter": self.cap(p["resolved_in_chapter"]) if p.get("resolved_in_chapter") else None,
                "reinforced_in_chapters": js([self.cap(n) for n in refuerzos]) if refuerzos else None,
                "status": p.get("status", "active"),
            }, p["description"][:60])

    def cargar_relaciones(self):
        for r in self.d.get("relaciones", []):
            a, b = self.personaje(r["a"]), self.personaje(r["b"])
            campos = {
                "project_id": self.pid,
                "description": r.get("description"),
                "private_reality": r.get("private_reality"),
                "status": r.get("status", "active"),
                "established_in_chapter": self.cap(r),
            }
            for k in ("public_perception", "evolution_notes"):
                if k in r:
                    campos[k] = r[k]
            self.upsert("character_relationships",
                        {"character_a_id": a, "character_b_id": b, "relationship_type": r["type"]},
                        campos, f"{r['a']} - {r['b']} ({r['type']})")

    def cargar_reglas(self):
        nuevas = [(r["category"], r["rule"], r.get("priority", 5)) for r in self.d.get("reglas", [])]
        viejas = [tuple(r) for r in self.conn.execute(
            "SELECT category, rule, priority FROM narrative_rules WHERE project_id = ? ORDER BY rowid", (self.pid,)
        ).fetchall()]

        def borrar():
            self.conn.execute("DELETE FROM narrative_rules WHERE project_id = ?", (self.pid,))

        def insertar():
            for r in nuevas:
                self.conn.execute(
                    "INSERT INTO narrative_rules (project_id, category, rule, priority) VALUES (?, ?, ?, ?)",
                    (self.pid, *r),
                )

        self.reemplazar("reglas del usuario", "narrative_rules", viejas, nuevas, borrar, insertar)

    def cargar_notas(self):
        for n in self.d.get("notas", []):
            self.upsert("author_notes", {"project_id": self.pid, "content": n["content"]}, {
                "note_type": n.get("note_type", "general"),
                "chapter_id": self.cap(n) if "capitulo" in n else None,
                "resolved": 1 if n.get("resolved") else 0,
            }, n["content"][:60])

    def contar_palabras(self):
        total = self.conn.execute(
            "SELECT COALESCE(SUM(word_count), 0) FROM chapters WHERE project_id = ?", (self.pid,)
        ).fetchone()[0]
        self.upsert("projects", {"id": self.pid}, {"current_word_count": total}, "palabras")
        return total

    def cargar(self):
        self.proyecto()
        self.cargar_lugares()
        self.cargar_capitulos()
        self.cargar_personajes()
        self.cargar_escenas()
        self.cargar_cronologia()
        self.cargar_hechos()
        self.cargar_conocimiento()
        self.cargar_hilos()
        self.cargar_pistas()
        self.cargar_relaciones()
        self.cargar_reglas()
        self.cargar_notas()
        return self.contar_palabras()


def main():
    ap = argparse.ArgumentParser(description="Cargar la semilla de un fanfic en su propia base")
    ap.add_argument("--db", required=True, help="base del fanfic, por ejemplo db/neutral-frisk.db")
    ap.add_argument("--file", help="semilla JSON (por defecto source/<nombre de la base>/datos.json)")
    ap.add_argument("--canon", default=os.path.join(RAIZ, "db", CANON), help="base canon para crear la copia")
    ap.add_argument("--dry-run", action="store_true", help="mostrar los cambios sin guardar nada")
    args = ap.parse_args()

    if os.path.basename(args.db) == CANON:
        salir("db/murder-drones.db es el canon limpio: el fanfic va en su propia copia (db/<nombre>.db)")
    slug = os.path.splitext(os.path.basename(args.db))[0]
    archivo = args.file or os.path.join(RAIZ, "source", slug, "datos.json")
    if not os.path.exists(archivo):
        salir(f"no existe la semilla: {archivo}")
    with open(archivo, encoding="utf-8") as f:
        datos = json.load(f)

    creada = not os.path.exists(args.db)
    if creada:
        if not os.path.exists(args.canon):
            salir(f"no existe el canon: {args.canon}")
        if args.dry_run:
            conn = sqlite3.connect(":memory:")
            sqlite3.connect(args.canon).backup(conn)
        else:
            shutil.copyfile(args.canon, args.db)
            conn = sqlite3.connect(args.db)
    else:
        conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")

    cargador = Cargador(conn, datos, slug)
    try:
        palabras = cargador.cargar()
    except sqlite3.Error as e:
        conn.rollback()
        salir(f"sqlite: {e}")
    if args.dry_run:
        conn.rollback()
    else:
        conn.commit()

    resumen = {}
    for tabla, que in cargador.cambios.items():
        resumen[tabla] = {k: (len(v) if k == "nuevos" and len(v) > 12 else v) for k, v in que.items()}
    print(json.dumps({
        "status": "ok",
        "db": args.db,
        "semilla": os.path.relpath(archivo, RAIZ),
        "dry_run": args.dry_run,
        "base_creada": creada,
        "palabras": palabras,
        "cambios": resumen or "sin cambios",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
