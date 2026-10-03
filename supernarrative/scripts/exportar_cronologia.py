#!/usr/bin/env python3
"""
Genera la hoja de cronologia de un fanfic desde su base: capitulos, eventos
por era, estado al final del ultimo capitulo, quien sabe que, hilos, pistas,
relaciones, lugares y notas. Las reglas del usuario (feedback) van aparte en
feedback.md. Las fichas completas de los personajes estan en la base.

Uso:
  python3 scripts/exportar_cronologia.py --db db/neutral-frisk.db
  (por defecto escribe source/<nombre de la base>/cronologia.md)
"""

import argparse
import json
import os
import sqlite3
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

EVENTO = {"death": "muerte", "destruction": "destruccion", "discovery": "descubrimiento", "encounter": "encuentro",
          "revelation": "revelacion", "transformation": "transformacion", "movement": "movimiento"}
ESTADO = {"alive": "vivo", "dead": "muerto", "unknown": "desconocido", "presumed_dead": "dado por muerto",
          "missing": "desaparecido"}
NIVEL = {"knows": "sabe", "partial": "sabe en parte", "suspects": "sospecha", "wrong_belief": "cree otra cosa",
         "unaware": "no sabe", "forgot": "se olvido"}
COMO = {"witnessed": "lo vio", "deduced": "lo dedujo", "overheard": "lo escucho", "read": "lo leyo",
        "reader_inference": "lo infiere"}
HILO_TIPO = {"main_plot": "trama principal", "subplot": "subtrama", "mystery": "misterio", "romance": "romance",
             "character_arc": "arco de personaje", "thematic": "tematico", "red_herring": "pista falsa"}
HILO_ESTADO = {"planned": "planeado", "planted": "plantado", "developing": "en desarrollo", "climax": "climax",
               "resolved": "resuelto", "abandoned": "abandonado"}
BEAT = {"plant": "planta", "reinforce": "refuerza", "complicate": "complica", "twist": "giro", "escalate": "escala",
        "near_reveal": "casi se revela", "reveal": "se revela", "resolve": "se resuelve", "subvert": "se da vuelta"}
PISTA = {"active": "activa", "reinforced": "reforzada", "resolved": "resuelta", "red_herring": "pista falsa",
         "abandoned": "abandonada"}
RELACION = {"family": "familia", "enemy": "enemigos", "ally": "aliados", "mentor": "mentor", "lover": "pareja",
            "rival": "rivales", "colleague": "colegas", "unknown": "sin relacion todavia"}
REL_ESTADO = {"active": "activa", "evolving": "cambiando", "broken": "rota", "secret": "secreta", "dormant": "dormida"}
REGLA = {"forbidden": "prohibido", "style": "estilo", "structure": "estructura", "voice": "voz", "pov": "pov",
         "rhythm": "ritmo"}
NOTA = {"general": "general", "todo": "pendiente", "idea": "idea", "research": "investigacion", "revision": "revision"}
ESCENA = {"action": "accion", "dialogue": "dialogo", "reflection": "reflexion", "revelation": "revelacion",
          "transition": "transicion", "flashback": "flashback", "confrontation": "enfrentamiento",
          "investigation": "investigacion"}
RITMO = {"slow": "lento", "medium": "medio", "fast": "rapido", "frantic": "frenetico"}
TONO = {"hopeful": "esperanzado", "dread": "pavor", "melancholy": "melancolico", "triumphant": "triunfal",
        "neutral": "neutro", "paranoid": "paranoico", "intimate": "intimo", "chaotic": "caotico"}
ROL = {"protagonist": 1, "antagonist": 2, "secondary": 3, "tertiary": 4, "mentioned": 5}
VOZ = {"first_person": "primera persona", "third_person": "tercera persona",
       "third_omniscient": "tercera persona omnisciente"}


def t(mapa, valor):
    return mapa.get(valor, valor or "")


def frase(*partes):
    """Une partes en frases con un solo punto al final de cada una."""
    return " ".join(p if p.endswith(".") else p + "." for p in (x.strip() for x in partes if x) if p)


def celda(texto):
    return (texto or "").replace("|", "/").replace("\n", " ")


class Hoja:
    def __init__(self, conn):
        self.c = conn
        self.p = conn.execute("SELECT * FROM projects ORDER BY updated_at DESC LIMIT 1").fetchone()
        self.pid = self.p["id"]
        self.caps = conn.execute(
            "SELECT * FROM chapters WHERE project_id = ? ORDER BY chapter_order", (self.pid,)
        ).fetchall()
        self.num = {c["id"]: c["chapter_number"] for c in self.caps}
        self.pers = {r["id"]: r["name"] for r in conn.execute(
            "SELECT id, name FROM characters WHERE project_id = ?", (self.pid,))}
        self.lug = {r["id"]: r["name"] for r in conn.execute(
            "SELECT id, name FROM locations WHERE project_id = ?", (self.pid,))}
        self.out = []

    def w(self, linea=""):
        self.out.append(linea)

    def capn(self, cid):
        return f"cap {self.num[cid]}" if cid in self.num else (cid or "")

    def nombres(self, ids_json):
        try:
            ids = json.loads(ids_json or "[]")
        except ValueError:
            return ""
        return ", ".join(self.pers.get(i, i) for i in ids)

    # ------------------------------------------------------------------ partes

    def cabecera(self, db, slug):
        ultimo = self.caps[-1]["chapter_number"] if self.caps else 0
        self.w(f"# {self.p['name']}: hoja de cronologia")
        self.w()
        self.w(f"Sale de `{db}` con `python3 scripts/exportar_cronologia.py --db {db}`. No se edita a mano: "
               f"lo nuevo va en `source/{slug}/datos.json`, se carga con `python3 scripts/cargar_fanfic.py --db {db}` "
               f"y se vuelve a generar esta hoja. Las reglas del usuario van aparte en `feedback.md`.")
        self.w()
        self.w(f"- **Genero:** {self.p['genre']}")
        self.w(f"- **Narrador:** {t(VOZ, self.p['narrative_voice'])}")
        self.w(f"- **Palabras escritas:** {self.p['current_word_count']}")
        self.w(f"- **Capitulos escritos:** {len(self.caps)}. **Sigue:** capitulo {ultimo + 1}")
        self.w()
        self.w(self.p["description"] or "")
        self.w()

    def capitulos(self):
        self.w("## Capitulos")
        self.w()
        for c in self.caps:
            self.w(f"### Capitulo {c['chapter_number']}: {c['title']} ({c['status']}, {c['word_count']} palabras)")
            self.w()
            self.w(f"- **Archivo:** `{c['file_path']}`")
            self.w(f"- **Tipo:** {t(ESCENA, c['scene_type'])}. **Tension:** {c['tension_level']}/10. "
                   f"**Ritmo:** {t(RITMO, c['pacing'])}. **Tono:** {t(TONO, c['emotional_tone'])}")
            self.w(f"- **Cuando:** {c['story_date']}. **Termina:** {c['story_time_end']}")
            self.w(f"- **Abre con:** {c['opening_hook']}")
            self.w(f"- **Cierra con:** {c['closing_hook']}")
            self.w(f"- **Resumen:** {c['summary']}")
            escenas = self.c.execute(
                "SELECT * FROM scenes WHERE chapter_id = ? ORDER BY scene_order", (c["id"],)
            ).fetchall()
            if escenas:
                self.w("- **Escenas:**")
                for s in escenas:
                    self.w(f"  {s['scene_number']}. {self.lug.get(s['location_id'], '?')} "
                           f"({self.nombres(s['characters_present'])}): {s['summary']}")
            self.w()

    def cronologia(self):
        self.w("## Cronologia")
        self.w()
        self.w("Orden de la historia, no de los capitulos. Cada evento dice en que parte se cuenta.")
        self.w()
        eventos = self.c.execute("""
            SELECT we.*, ch.chapter_number FROM world_events we
            JOIN chapters ch ON ch.id = we.chapter_id
            WHERE we.project_id = ?
            ORDER BY we.story_timestamp, ch.chapter_number, we.rowid
        """, (self.pid,)).fetchall()
        era = None
        n = 0
        for e in eventos:
            if e["story_timestamp"] != era:
                if era is not None:
                    self.w()
                era = e["story_timestamp"]
                self.w(f"### {era}")
                self.w()
            n += 1
            desc = e["description"]
            cuando = f"cap {e['chapter_number']}"
            if desc.endswith("]") and " [se cuenta en " in desc:
                desc, cuando = desc[:-1].rsplit(" [se cuenta en ", 1)
            titulo = ""
            if desc.startswith("[") and "] " in desc:
                titulo, desc = desc[1:].split("] ", 1)
            linea = f"{n}. **{titulo}** ({t(EVENTO, e['event_type'])}). " if titulo else f"{n}. "
            quienes = self.nombres(e["affected_entities"])
            linea += frase(desc, f"*Personajes:* {quienes}" if quienes else "", f"*Se cuenta en:* {cuando}")
            self.w(linea)
        self.w()

    def estado(self):
        ultimo = self.caps[-1]["chapter_number"] if self.caps else 0
        self.w(f"## Estado al final del capitulo {ultimo}")
        self.w()
        self.w("Solo donde esta y como esta cada uno. Las fichas completas estan en la base.")
        self.w()
        self.w("| Personaje | Estado | Donde | Como esta |")
        self.w("|---|---|---|---|")
        filas = self.c.execute("""
            SELECT c.*, (SELECT COUNT(*) FROM scenes s JOIN chapters ch ON ch.id = s.chapter_id
                         WHERE ch.project_id = c.project_id
                           AND s.characters_present LIKE '%' || c.id || '%') AS escenas
            FROM characters c
            WHERE c.project_id = ? AND c.introduced_in_chapter IS NOT NULL AND c.role != 'mentioned'
            ORDER BY c.rowid
        """, (self.pid,)).fetchall()
        for c in sorted(filas, key=lambda c: (ROL.get(c["role"], 9), -c["escenas"])):
            self.w(f"| {celda(c['name'])} | {t(ESTADO, c['status'])} | {celda(self.lug.get(c['current_location_id'], ''))} "
                   f"| {celda(c['emotional_state'])} |")
        mencionados = [r["name"] for r in self.c.execute(
            "SELECT name FROM characters WHERE project_id = ? AND role = 'mentioned' ORDER BY rowid", (self.pid,))]
        if mencionados:
            self.w()
            self.w(f"Solo nombrados: {', '.join(mencionados)}.")
        self.w()

    def conocimiento(self):
        self.w("## Quien sabe que")
        self.w()
        ids = list(self.num)
        marcas = ", ".join("?" for _ in ids) or "''"
        hechos = self.c.execute(f"""
            SELECT * FROM story_facts
            WHERE project_id = ? AND (established_in_chapter IN ({marcas})
                  OR id IN (SELECT fact_id FROM knowledge_states WHERE project_id = ?))
            ORDER BY significance DESC, rowid
        """, (self.pid, *ids, self.pid)).fetchall()
        descripcion = {h["id"]: h["description"] for h in hechos}
        for h in hechos:
            cabeza = f"- **{h['description']}**"
            if not h["is_true"]:
                verdad = descripcion.get(h["contradiction_of"])
                if verdad is None and h["contradiction_of"]:
                    fila = self.c.execute(
                        "SELECT description FROM story_facts WHERE id = ?", (h["contradiction_of"],)).fetchone()
                    verdad = fila["description"] if fila else None
                cabeza += f" (FALSO. Lo cierto: {verdad})" if verdad else " (FALSO)"
            self.w(cabeza)
            filas = self.c.execute(
                "SELECT * FROM knowledge_states WHERE fact_id = ? ORDER BY rowid", (h["id"],)
            ).fetchall()
            por_nivel = {}
            for k in filas:
                quien = "lector" if k["knower_id"] == "__reader__" else self.pers.get(k["knower_id"], k["knower_id"])
                extra = []
                como = k["how_learned"] or ""
                if como.startswith("told_by:"):
                    extra.append(f"se lo dijo {self.pers.get(como.split(':', 1)[1], como.split(':', 1)[1])}")
                elif como:
                    extra.append(t(COMO, como))
                if k["wrong_belief_detail"]:
                    extra.append(k["wrong_belief_detail"])
                if k["notes"]:
                    extra.append(k["notes"])
                por_nivel.setdefault(k["knowledge_level"], []).append(
                    f"{quien} ({'; '.join(extra)})" if extra else quien)
            for nivel in ("knows", "partial", "suspects", "wrong_belief", "unaware", "forgot"):
                if nivel in por_nivel:
                    self.w(f"  - {t(NIVEL, nivel)}: {', '.join(por_nivel[nivel])}")
        self.w()

    def hilos(self):
        hilos = self.c.execute(
            "SELECT * FROM plot_threads WHERE project_id = ? ORDER BY priority DESC, rowid", (self.pid,)
        ).fetchall()
        for titulo, abiertos in (("Hilos abiertos", True), ("Hilos cerrados", False)):
            grupo = [h for h in hilos if (h["status"] not in ("resolved", "abandoned")) == abiertos]
            if not grupo:
                continue
            self.w(f"## {titulo}")
            self.w()
            for h in grupo:
                cierre = f", se cerro en {self.capn(h['resolved_in_chapter'])}" if h["resolved_in_chapter"] else ""
                self.w(f"### {h['name']} ({t(HILO_TIPO, h['thread_type'])}, {t(HILO_ESTADO, h['status'])}, "
                       f"prioridad {h['priority']}{cierre})")
                self.w()
                self.w(h["description"] or "")
                self.w()
                for b in self.c.execute(
                    "SELECT * FROM thread_beats WHERE thread_id = ? ORDER BY created_at, rowid", (h["id"],)
                ):
                    self.w(f"- {self.capn(b['chapter_id'])}, {t(BEAT, b['beat_type'])}: {b['description']}")
                if h["notes"]:
                    self.w(f"- *Nota:* {h['notes']}")
                self.w()

    def pistas(self):
        pistas = self.c.execute("""
            SELECT cl.*, pt.name AS hilo FROM clues cl
            LEFT JOIN plot_threads pt ON pt.id = cl.thread_id
            WHERE cl.project_id = ? ORDER BY cl.rowid
        """, (self.pid,)).fetchall()
        if not pistas:
            return
        self.w("## Pistas")
        self.w()
        for titulo, activas in (("Sin resolver", True), ("Resueltas", False)):
            grupo = [p for p in pistas if (p["status"] in ("active", "reinforced")) == activas]
            if not grupo:
                continue
            self.w(f"### {titulo}")
            self.w()
            for p in grupo:
                cabeza = (f"{p['description']} ({p['clue_type']}, sutileza {p['subtlety']}, "
                          f"{t(PISTA, p['status'])}, plantada en {self.capn(p['planted_in_chapter'])})")
                self.w("- " + frase(
                    cabeza,
                    f"*Hilo:* {p['hilo']}" if p["hilo"] else "",
                    f"*Como funciona:* {p['mechanism']}" if p["mechanism"] else "",
                    f"*Cobra sentido:* {p['intended_resolution']}" if p["intended_resolution"] else "",
                    f"*Resuelta en:* {self.capn(p['resolved_in_chapter'])}" if p["resolved_in_chapter"] else "",
                ))
            self.w()

    def relaciones(self):
        ids = list(self.num)
        if not ids:
            return
        marcas = ", ".join("?" for _ in ids)
        filas = self.c.execute(f"""
            SELECT * FROM character_relationships
            WHERE project_id = ? AND established_in_chapter IN ({marcas}) ORDER BY rowid
        """, (self.pid, *ids)).fetchall()
        if not filas:
            return
        self.w("## Relaciones del fanfic")
        self.w()
        for r in filas:
            a, b = self.pers.get(r["character_a_id"], "?"), self.pers.get(r["character_b_id"], "?")
            self.w(f"- **{a} y {b}** ({t(RELACION, r['relationship_type'])}, {t(REL_ESTADO, r['status'])}): " + frase(
                r["description"] or "", f"*En privado:* {r['private_reality']}" if r["private_reality"] else ""))
        self.w()

    def lugares(self):
        filas = self.c.execute(
            "SELECT * FROM locations WHERE project_id = ? ORDER BY rowid", (self.pid,)
        ).fetchall()
        if not filas:
            return
        self.w("## Lugares")
        self.w()
        hijos = {}
        for l in filas:
            hijos.setdefault(l["parent_location_id"], []).append(l)

        def rama(padre, nivel):
            for l in hijos.get(padre, []):
                self.w(f"{'  ' * nivel}- **{l['name']}**: {l['description'] or ''}")
                rama(l["id"], nivel + 1)

        rama(None, 0)
        self.w()

    def reglas(self):
        filas = self.c.execute(
            "SELECT * FROM narrative_rules WHERE project_id = ? AND active = 1 ORDER BY rowid", (self.pid,)
        ).fetchall()
        self.w(f"# {self.p['name']}: feedback del usuario")
        self.w()
        self.w("Reglas que el usuario dio al corregir los capitulos. Mandan sobre cualquier skill de estilo cuando choquen.")
        self.w()
        for i, r in enumerate(filas, 1):
            self.w(f"{i}. [{t(REGLA, r['category'])}, prioridad {r['priority']}] {r['rule']}")
        self.w()

    def notas(self):
        filas = self.c.execute(
            "SELECT * FROM author_notes WHERE project_id = ? AND note_type != 'pending_analysis' "
            "AND resolved = 0 ORDER BY rowid", (self.pid,)
        ).fetchall()
        if not filas:
            return
        self.w("## Notas")
        self.w()
        for n in filas:
            self.w(f"- [{t(NOTA, n['note_type'])}] {n['content']}")
        self.w()

    def generar(self, db, slug):
        self.cabecera(db, slug)
        self.capitulos()
        self.cronologia()
        self.estado()
        self.conocimiento()
        self.hilos()
        self.pistas()
        self.relaciones()
        self.lugares()
        self.notas()
        return "\n".join(self.out).rstrip() + "\n"

    def generar_feedback(self):
        self.out = []
        self.reglas()
        return "\n".join(self.out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Generar la hoja de cronologia de un fanfic")
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", help="por defecto source/<nombre de la base>/cronologia.md")
    args = ap.parse_args()

    if not os.path.exists(args.db):
        print(json.dumps({"status": "error", "message": f"DB no encontrada: {args.db}"}))
        sys.exit(1)
    slug = os.path.splitext(os.path.basename(args.db))[0]
    salida = args.out or os.path.join(RAIZ, "source", slug, "cronologia.md")

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    db_rel = os.path.relpath(os.path.abspath(args.db), RAIZ)
    hoja = Hoja(conn)
    texto = hoja.generar(db_rel, slug)
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    with open(salida, "w", encoding="utf-8") as f:
        f.write(texto)
    feedback = os.path.join(os.path.dirname(os.path.abspath(salida)), "feedback.md")
    with open(feedback, "w", encoding="utf-8") as f:
        f.write(hoja.generar_feedback())
    print(json.dumps({"status": "ok", "hoja": os.path.relpath(os.path.abspath(salida), RAIZ),
                      "feedback": os.path.relpath(feedback, RAIZ),
                      "lineas": texto.count("\n"), "palabras": len(texto.split())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
