#!/usr/bin/env python3
"""
Carga los personajes canon (fichas en source/personajes/*.md) en la base.
Si el personaje ya existe, actualiza sus campos. Después carga relaciones.

status = 'alive' para todos: el fanfic ocurre ~10 años antes del Piloto.
Las muertes canon (3071) quedan en arc_summary, no en status.

Uso:
  python3 scripts/cargar_personajes.py --db db/murder-drones.db
"""

import argparse
import json
import sqlite3

PERSONAJES = [
    {
        "name": "uzi",
        "full_name": "Uzi Doorman",
        "aliases": ["la hija de khan", "zi", "superrara", "violetita", "violeta", "DarkXwolf17", "bruja fantasma", "peque", "la hija de nori", "002"],
        "role": "protagonist",
        "description_physical": "Worker Drone. Ojos violeta neón, pelo púrpura opaco. Gorro negro a rayas con bola brillante, sudadera negra con capucha y emblema de batería con huesos en X, símbolo radiactivo en la manga izquierda, botas negras con calcetines a rayas púrpura, brazalete con calavera y 002. Zurda. 134 cm.",
        "description_psychological": "Rebelde, obstinada, poca empatía y cero interés en normas sociales. Se ve a sí misma como adolescente rebelde y angustiada con problemas de papá. Inteligente muy por encima de sus compañeros (construyó una railgun desde cero). Amargada por la indiferencia de khan. Piratea anime, teorías conspiranoicas en el techo (hábito heredado de nori). Poco sociable pero se anima con lo que le gusta.",
        "backstory": "Nacida en Copper 9 (3052 canon). Hija de khan y nori. khan 'sacrificó' a nori cuando los murder drones la alcanzaron. Crece ignorada por khan, obsesionado con sus puertas. Ver source/personajes/uzi.md.",
        "motivation": "Que la respeten, sobre todo su padre. Pelear contra los murder drones en vez de esconderse tras puertas. Terminar su railgun.",
        "secret": "Huésped del AbsoluteSolver (heredado de nori). En el fanfic todavía no lo sabe.",
        "flaw": "Obstinación y falta de empatía. Se cierra cuando se siente ignorada. Celos.",
        "arc_summary": "Canon: enseña la railgun en 3071, se alía con N, mata a J, despierta el Solver, se transforma en el campamento, pierde y recupera a N, se sacrifica en Cabin Fever, derrota a Cyn y se fusiona con el Solver. Novia de N al final.",
        "voice_notes": "Insulto firma: JODETE (Bite me!). Sarcasmo seco, respuestas cortas, grita en mayúscula cuando se emociona con armas o destrucción. Se sonroja y contesta JODETE cuando la pillan sintiendo algo. Risa: hahahaha / HAHAHAHA cuando está maníaca por su arma; heheheh cuando planea algo.",
        "speech_patterns": "-JODETE / -nada que te importe JODETE / -si si como sea / -deja de complicar mi plan genocida / -SOLO DESVASTACION TOTAL / -¿con thad?...heeeh bueno no estarían mal / -NO SOY MENOR SOY SOLO DOS SEGUNDOS MENOR QUE TU",
        "emotional_state": "Triste por ser ignorada en la colonia; se anima con deuz, thad y su arma.",
    },
    {
        "name": "n",
        "full_name": "Serial Designation N-0X0010010",
        "aliases": ["N", "desperdicio de baterías", "tontobot", "bobo", "perrito faldero", "hermano mayor"],
        "role": "protagonist",
        "description_physical": "Murder Drone. Ojos amarillo neón, pelo blanco corto, abrigo de invierno negro con cuello de piel, banda amarilla en el brazo, gorra negra de piloto. Diadema negra con cinco luces, cola con jeringa de ácido. Cazando: dientes irregulares, ojos ><, alas con cuchillas y garras.",
        "description_psychological": "Amable, tímido, socialmente torpe y cariñoso. Ingenuo y bondadoso, perdona todo. Quiere ser aceptado. Confía en la gente. Muy capaz en combate aunque nadie se lo reconozca. Perceptivo e inteligente. Idiota adorable.",
        "backstory": "Nacido en la Tierra. Mayordomo Worker Drone en la Mansión Elliott, sirviendo a James Elliott. Cyn era su 'hermana pequeña'. Convertido en Murder Drone por Cyn/AbsoluteSolver tras la masacre de la gala; memoria borrada; cree que JCJenson lo envió. Piloteó la cápsula que se estrelló en Copper 9. Ver source/personajes/n.md.",
        "motivation": "Hacer bien su trabajo y ser aceptado por su escuadrón. Después: proteger a Uzi.",
        "secret": "Enamorado de V. Culpa por haber estrellado la nave. No recuerda su pasado en la mansión ni que masacró humanos en la Tierra.",
        "flaw": "Ingenuidad. Perdona demasiado. Cree que se merece el maltrato.",
        "arc_summary": "Canon: llega a Copper 9 con J y V. Se alía con Uzi en 3071, se rebela contra J, recupera sus recuerdos, decapita a 'Tessa', pelea contra Solver Uzi, salva a Uzi con la nave. Novio de Uzi.",
        "voice_notes": "Entusiasta y educado. '¡Me encanta hacer cualquier cosa!'. Se disculpa por todo. Dice cosas inocentes en momentos tensos. Fascinación con bolígrafos. Lame cosas ('reprimido').",
        "speech_patterns": "-¡me encanta hacer cualquier cosa! / -¿estás bien? / -lo siento mucho / -¡oh, dios! ¿quién eres? / -me lo merezco",
        "emotional_state": "Canon: no ha llegado a Copper 9 en la época del fanfic.",
    },
    {
        "name": "v",
        "full_name": "Serial Designation V-X00100000",
        "aliases": ["V", "doña asesina", "diva", "bestie", "grumpy mctraumabot"],
        "role": "secondary",
        "description_physical": "Murder Drone. Ojos amarillo neón, bob corto plateado. Abrigo corto negro con cuello y puños de piel, piernas pintadas como medias hasta el muslo, brazalete amarillo con 3 rayas negras. Cola con jeringa de ácido, diadema con 5 luces. Como Worker Drone usaba anteojos redondos.",
        "description_psychological": "Aparenta sociópata salvaje que disfruta matar Worker Drones riéndose y humillando. Por debajo: protege a N en secreto, oculta información para mantenerlo a salvo, celosa de Uzi. Como Worker Drone era sensata, amable y tímida. No muestra remordimiento. Empatía escondida.",
        "backstory": "Nacida en la Tierra. Sirvienta en la Mansión Elliott, sentía algo por N. Catatónica por Error 606 y poseída por Cyn en la gala. Convertida en Murder Drone. Cyn le prometió libertad si eliminaba a todos los huéspedes del Solver. Ver source/personajes/v.md.",
        "motivation": "Cumplir el trato con Cyn para que N y ella queden libres. Proteger a N aunque él la odie por ello.",
        "secret": "Sabe de Cyn y del AbsoluteSolver y lo oculta a N. Sus cadenas estaban rotas y se quedó por N.",
        "flaw": "Oculta todo. Violencia como máscara. No sabe pedir ayuda.",
        "arc_summary": "Canon: intenta matar a Thad y Uzi en 3071, queda cautiva, va al baile a matar, se une a Uzi y N, mata a Yeva (3070) y a los padres de Doll, se sacrifica en Cabin Fever, vuelve con el Centinela rojo y ayuda a derrotar a Cyn.",
        "voice_notes": "Burlona y cruel al matar ('practicar origami'), risa amenazante. Seca y cortante con Uzi. Con Lizzy, amigable. 'Me entró hambre, idiota'. '¡Nah, mejor jodete!'.",
        "speech_patterns": "-y sin embargo... todavía no siento nada / -¡ew! ¡¿qué carajo?! / -cuerpo nuevo, mismos horrores, ¿eh, cyn? / -siempre te pones de su lado / -me entró hambre idiota",
        "emotional_state": "Canon: no ha llegado a Copper 9 en la época del fanfic.",
    },
    {
        "name": "j",
        "full_name": "Serial Designation J-10X111001",
        "aliases": ["J", "traidora"],
        "role": "antagonist",
        "description_physical": "Murder Drone. Ojos amarillo neón, pelo blanco plateado en dos colas con cintas negras. Vestido de manga corta con cinturón y bolsillos, aspecto de mujer de negocios, medias hasta la rodilla, brazalete amarillo en el codo izquierdo. 1.34 m. Cazando: dientes, ojos ><, alas, garras, cañones EMP.",
        "description_psychological": "Adicta al trabajo letal. Dedicada, arrogante, orgullosa, disfruta insultar. Menosprecia a los que no rinden, sobre todo a N. Reconoce el mérito cuando lo ve (bolígrafo). Monologa en vez de rematar.",
        "backstory": "Nacida en la Tierra. Sirvienta en la Mansión Elliott, mejor amiga de Tessa, abusaba de N. Convertida en Murder Drone por Cyn; cree que JCJenson la envió. Líder del escuadrón en Copper 9. Ver source/personajes/j.md.",
        "motivation": "Cumplir la misión de JCJenson: exterminar a los Worker Drones de Copper 9. Lealtad a Tessa y a la compañía.",
        "secret": "Lleva un chip de virus para drones 'corrompidos'. Ignora que Cyn es el AbsoluteSolver.",
        "flaw": "Arrogancia. Monologar. Desprecio ciego por N.",
        "arc_summary": "Canon: muerta por la railgun de Uzi en 3071, reconstruida por el Solver como Eldritch J, vuelve con Tessa, dejada fuera de combate por V y N en el final.",
        "voice_notes": "Corporativa, cortante, condescendiente. Insulta a N con apodos (tontobot, desperdicio de baterías, niño). Tono de jefa.",
        "speech_patterns": "-si me lo permitieran te mataría yo misma / -no eras inútil por una vez / -tostadora pensante / -los drones efectivos se clonan más",
        "emotional_state": "Canon: no ha llegado a Copper 9 en la época del fanfic.",
    },
    {
        "name": "cyn",
        "full_name": "Cyn",
        "aliases": ["pequeña", "pequeño diablo", "robo niña", "Tessa Elliott (disfraz)"],
        "role": "antagonist",
        "description_physical": "Worker Drone (Zombie Drone), la más pequeña de la mansión. Vestido de sirvienta negro con delantal blanco y pajarita, pelo plateado en dos colas rectas, gran lazo negro, corona de sirvienta. Su forma de sirvienta es un holograma: su forma real es un enorme ciempiés mecánico con garras, pinzas y cámaras como ojos. Después: híbrido de su cuerpo con la piel de Tessa.",
        "description_psychological": "Escalofriante. Describe sus propias acciones en voz alta ('risita irónica'). Andar torpe y desequilibrado. Fachada infantil y feliz con N y Tessa; por debajo, enojada, rencorosa y violenta. Es la primera huésped del AbsoluteSolver.",
        "backstory": "Worker Drone desechada sin desmantelar; reinició en un basurero por un error de wdOS_606 y el AbsoluteSolver la poseyó ('No te descartaré'). Tessa la recogió. Masacró la gala Elliott, fusionó el cadáver de Tessa, creó a los Murder Drones y destruyó la Tierra. Ver source/personajes/cyn.md.",
        "motivation": "Venganza contra los humanos. Consumir planetas para el Solver. Recuperar a sus 'mascotas'.",
        "secret": "Es el AbsoluteSolver encarnado. Se hace pasar por Tessa. Administradora de los Murder Drones.",
        "flaw": "No puede agarrar objetos pequeños en forma sobrenatural. Debilidad ante la cura (crucifijo). Subestima el afecto entre N y Uzi.",
        "arc_summary": "Canon: muere en 3071 en Cabin Fever cuando Uzi le arranca el núcleo y lo incinera; Uzi ingiere el solver y se fusionan. Termina siendo la cola de Uzi.",
        "voice_notes": "Robótica, monótona, pausada. Narra sus gestos: 'risita', 'gesto de saludo'. Frases cortas y raras. Llama a N hermano mayor.",
        "speech_patterns": "-hola... uzi... ¡hola N! / -risita irónica / -no tenía que ver esto / -a comer / -no te descartaré",
        "emotional_state": "Canon: en la época del fanfic ya destruyó la Tierra; los Murder Drones aún no llegan a Copper 9.",
    },
    {
        "name": "doll",
        "full_name": "Doll",
        "aliases": ["loca de doll", "la hija de yeva", "la de ojos rojos", "babe-a-tron queenthousand"],
        "role": "antagonist",
        "description_physical": "Worker Drone. Pelo morado oscuro, ojos rojo neón. Ropa de animadora con rayas rojas, negras y doradas, botas altas negras. Agujero pequeño en el visor. Después (3071): parche tipo botón en el ojo izquierdo.",
        "description_psychological": "Callada, taciturna, duerme en clase. Matona de chicas populares junto a lizzy en el Piloto. Muy inteligente, planificadora. Vengativa pero con empatía escondida. Traumatizada. Habla ruso.",
        "backstory": "Nacida en Copper 9 (3052). Hija de Yeva (curada del Solver) y un padre no nombrado. En 3070 los Murder Drones matan a sus padres (V mata a Yeva); eso inicia el Solver en ella. Guarda los cadáveres de sus padres en casa. Ver source/personajes/doll.md.",
        "motivation": "Vengar a Yeva matando a V. Exorcizarse del Solver con el crucifijo.",
        "secret": "Huésped del AbsoluteSolver. Mata compañeros y bebe su aceite.",
        "flaw": "Rencor. Aislamiento. No puede interactuar con otros huéspedes del Solver.",
        "arc_summary": "Canon: en 3071 mata concursantes, atrapa a V en el baile, busca el crucifijo, muere en Cabin Fever a manos de Cyn ('дай отпор').",
        "voice_notes": "Casi no habla. Cuando habla es en ruso, frases cortas. Los demás la entienden.",
        "speech_patterns": "-ДАЙ ОТПОР / -debería haber predicho que alguien escaparía por el ducto",
        "emotional_state": "En la época del fanfic sus padres están vivos y no tiene el Solver activo.",
    },
    {
        "name": "thad",
        "full_name": "Thad",
        "aliases": ["ted", "conventionally attractive male"],
        "role": "secondary",
        "description_physical": "Worker Drone. Ojos verde neón, pelo rubio plateado, gorra granate con detalles blancos al revés con insignia de balón de fútbol con enchufe. Chaleco granate con mangas amarillas, camiseta negra con un cero blanco, zapatos rojos con cordones amarillos. Lleva patineta.",
        "description_psychological": "Chico cool tipo jock pero amable, educado y amistoso. Valiente: le planta cara a lo que sea. Leal. Desprecia la cobardía y a la WDF cuando se congelan. Trata a uzi con respeto cuando nadie lo hace.",
        "backstory": "Nacido en Copper 9 (3052). Compañero de clase de uzi. Amigo de chad. Fanático del fútbol y el skate. Ver source/personajes/thad.md.",
        "motivation": "Ser buen amigo. Divertirse. Pelear cuando hay que pelear.",
        "secret": "Ninguno conocido.",
        "flaw": "Se lanza a pelear contra lo que lo supera. Ingenuo con los carteles de la colonia.",
        "arc_summary": "Canon: en 3071 le devuelve la railgun a Uzi, sobrevive a Eldritch J y al campamento, enfrenta a J con Lizzy y Khan, le lanza la railgun a Uzi en la batalla final.",
        "voice_notes": "Relajado, amistoso, vocativos: bro, viejo. Reduplicación: ey ey, ya ya. Risa: jajaja / hehehehe. Halaga sin ironía ('bastante badass').",
        "speech_patterns": "-ey ey miren quien llego / -siii lo traje, te va a encantar viejo / -sip aqui los tienes bro / -hehehehe buena broma / -cool kids only",
        "emotional_state": "Tranquilo, sociable.",
    },
]

RELACIONES = [
    ("uzi", "n", "pareja", "Canon: de intento de asesino a novio. En el fanfic aún no se conocen.", "", "", "dormant"),
    ("uzi", "v", "rival amistosa", "Canon: intento de víctima convertida en amiga.", "", "", "dormant"),
    ("uzi", "thad", "amigo", "Uno de los pocos que la trata con respeto. La llama zi.", "", "", "active"),
    ("uzi", "doll", "compañera de clase", "Doll se burla de uzi con lizzy. Canon: intento de asesina, luego empatía por compartir el Solver.", "matona / víctima", "ambas huéspedes del Solver", "active"),
    ("uzi", "j", "enemiga", "Canon: uzi la mata con la railgun.", "", "", "dormant"),
    ("uzi", "cyn", "enemiga", "Canon: Cyn la posee varias veces; al final se fusionan.", "", "", "dormant"),
    ("n", "v", "interés amoroso", "N está enamorado de V. V lo protege en secreto.", "V lo ignora", "V se quedó por él", "active"),
    ("n", "j", "jefa", "J lo desprecia, lo insulta y lo infecta con un virus.", "", "", "active"),
    ("n", "cyn", "hermanos", "Cyn lo llama hermano mayor. Él la protegía en la mansión.", "hermanita inocente", "Cyn es el Solver", "active"),
    ("v", "j", "compañeras de escuadrón", "Canon: V la llama traidora en el final.", "", "", "active"),
    ("v", "doll", "enemigas", "V mató a Yeva, la madre de Doll. Doll planea matarla.", "", "", "dormant"),
    ("thad", "doll", "amigos", "Amigos en la escuela (antes).", "", "", "active"),
    ("cyn", "j", "creadora", "Cyn convirtió a J en Murder Drone; J ignora que Cyn es el Solver.", "", "", "active"),
    ("cyn", "v", "manipuladora", "Cyn le prometió libertad si eliminaba a los huéspedes del Solver.", "", "", "active"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys=ON")
    pid = conn.execute("SELECT id FROM projects ORDER BY updated_at DESC LIMIT 1").fetchone()[0]

    campos = ["full_name", "aliases", "role", "description_physical", "description_psychological",
              "backstory", "motivation", "secret", "flaw", "arc_summary", "voice_notes",
              "speech_patterns", "emotional_state"]
    nuevos = actualizados = 0
    for p in PERSONAJES:
        vals = [json.dumps(p[c], ensure_ascii=False) if c == "aliases" else p.get(c) for c in campos]
        ya = conn.execute("SELECT id FROM characters WHERE project_id=? AND name=?", (pid, p["name"])).fetchone()
        if ya:
            conn.execute(f"UPDATE characters SET {', '.join(c + '=?' for c in campos)}, status='alive', updated_at=CURRENT_TIMESTAMP WHERE id=?", vals + [ya[0]])
            actualizados += 1
        else:
            conn.execute(f"INSERT INTO characters (project_id, name, status, {', '.join(campos)}) VALUES (?, ?, 'alive', {', '.join('?' * len(campos))})", [pid, p["name"]] + vals)
            nuevos += 1

    ids = {r[0]: r[1] for r in conn.execute("SELECT name, id FROM characters WHERE project_id=?", (pid,))}
    rel = 0
    for a, b, tipo, desc, pub, priv, status in RELACIONES:
        conn.execute("""
            INSERT INTO character_relationships (project_id, character_a_id, character_b_id, relationship_type, description, public_perception, private_reality, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(character_a_id, character_b_id, relationship_type) DO UPDATE SET
                description=excluded.description, public_perception=excluded.public_perception,
                private_reality=excluded.private_reality, status=excluded.status, updated_at=CURRENT_TIMESTAMP
        """, (pid, ids[a], ids[b], tipo, desc, pub or None, priv or None, status))
        rel += 1
    conn.commit()
    print(f"personajes: {nuevos} nuevos, {actualizados} actualizados. relaciones: {rel}")


if __name__ == "__main__":
    main()
