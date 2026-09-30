---
name: estilo-narrativo-rol
description: Reproducir el estilo de escritura del usuario en historias con formato de rol (bloque de Narrador + bloques de Personaje). Define estructura de turnos, sintaxis, tiempos verbales, morfología (prefijos, sufijos, raíces, morfemas expresivos), marcas ortográficas y recursos de voz, separados en dos voces distintas — NARRADOR y PERSONAJE — que nunca se mezclan. Se activa cuando el usuario pida escribir, continuar, imitar, corregir o revisar un capítulo, prólogo, escena o diálogo "en mi estilo", "como escribo yo", con formato Narrador/Personaje, o cuando pegue un texto con ese formato y pida algo en el mismo estilo. No contiene nada de trama ni personajes: solo cómo se escribe.
---

# estilo-narrativo-rol

## regla cero — dos voces, dos gramáticas

El texto tiene dos motores de escritura que no se tocan:

- **NARRADOR**: párrafo corrido, una sola oración, sin comas, tiempos mezclados, muletillas en -mente.
- **PERSONAJE**: acotación de una línea en presente + diálogo corto en minúscula que estalla en MAYÚSCULA.

Si algo dentro de un diálogo suena a narrador (largo, con "claramente", con condicional -ría) está mal. Si algo dentro del narrador suena a personaje (frase corta, coma, vocativo) está mal.

En todo el texto: **cero signos de exclamación**. El volumen se escribe con MAYÚSCULAS y vocales alargadas, nunca con "!".

## 1. estructura de turno

- Orden: `Narrador` abre → uno o más bloques de `Personaje` juegan la escena → `Narrador` cierra, resume o salta de escena → se repite.
- Bloque de personaje = etiqueta `Nombre (rol)` + acotación + diálogo. La acotación puede ir sola sin diálogo ("caminando sin importarle nada") o ir después del diálogo como etiqueta de tono ("decia irónicamente", "decia con miedo").
- **Corte en suspenso**: el bloque de narrador termina con un conector colgado y sin resolver — "hasta que", "pero", "para abrir la puerta pero", "cuando" — y el siguiente bloque de personaje es lo que resuelve ese conector. Mínimo uno por escena.
- **Encabezados en mayúscula** para saltos de escena o momentos de peso: `# FIN DEL PROLOGO`, `# UNIVERSO X`, `# CONSECUENCIAS DE X`, `# FIN DE LA REPRODUCCIÓN`. Van bajo la etiqueta de Narrador.
- **Etiquetas dato:valor** sin espacio después de los dos puntos para información de mundo: `Linea temporal:66280`, `variacion:¿pregunta?`.
- **Cierre de capítulo**: encabezado `# FIN DE ...` o una única línea de personaje, seca, que funciona como remate y no lleva acotación larga.
- Los bloques de narrador se usan también para meter pensamientos del personaje y comentarios sobre el canon dentro del mismo párrafo, sin cambiar de bloque.

## 2. voz NARRADOR

### sintaxis

- Un párrafo = **una sola oración**. Cero comas. Cero puntos internos. Solo se cierra al terminar el bloque, y muchas veces ni eso.
- La oración se sostiene con conectores encadenados: **y / pero / mientras / asi que / hasta que / lo que / para / enseguida / claramente / simplemente / ahora mismo**.
- **Cadena "lo que"**: es el conector causal principal y se apila sin límite. Ejemplo de forma: "lo que rápidamente X hizo tal cosa lo que enorgullecio a Y lo que hizo que Z".
- **"pero" apilado**: "pero simplemente pero", "pero pero". No se corrige, es ritmo.
- **Preguntas retóricas** dentro de la narración: "¿que hizo eso?", "¿acaso murio?", "¿porque estaba aqui?". Se contestan en la misma oración o se dejan abiertas.
- **Pronombre de rebote "este / esta"** para retomar al último personaje nombrado sin repetir el nombre: "este apareceria", "esta reiria", "este dijo".
- **Etiqueta de habla dentro de la narración**: "diria emocionada", "decia estupefacto", "dijo con miedo". El narrador anuncia que el personaje va a hablar y el bloque siguiente es la línea.
- **Compresión de tiempo**: una tarde entera o diez años caben en un párrafo, mezclando acción, pensamiento del personaje, lista de lo que aprendió/hizo y comentario sobre el canon, todo corrido.
- **Repetición de la misma palabra** dentro de la oración no se evita: "claramente... claramente... claramente", "ayudar... ayudar... ayudar". La repetición es aceptada.

### tiempos verbales (los tres conviven en la misma oración)

| uso | tiempo | ejemplos de forma |
|---|---|---|
| fondo, estado, descripción | imperfecto | estaba, era, tenia, podia, sabia |
| hecho puntual ya ocurrido | pretérito | brillo, dio, golpeo, abrio, celebro |
| acción de rol (lo que el personaje hace en la escena) | condicional en **-ría** | apareceria, diria, estarian caminando, verian, agitaria, soltaria, abriria |

El condicional **no es hipotético**: significa "hace / hará". Es la marca de rol. Cambiar de tiempo a mitad de oración es normal y esperado.

### léxico

- **Adverbios en -mente como muletilla**: `claramente` es el rey (mínimo 2 por párrafo largo, puede llegar a 5), después `simplemente`, `rápidamente`, `básicamente`, `tontamente`, `supuestamente`, `tranquilamente`, `plácidamente`, `finalmente`. `enseguida` cumple la misma función aunque no termine en -mente.
- **Intensificador burlón "estúpidamente"** + adjetivo o gerundio: "estúpidamente avanzadas", "tardando estúpidamente casi toda la tarde", "tecnologia estúpidamente avanzada".
- **Vocabulario técnico crudo** pegado dentro de la oración sin explicar ni frenar: riel, ionización, refrigeración criogénica, bobinas, polímero, aislante, chip, celda, campo magnético.
- **Nombres propios y gentilicios en minúscula**: nombres de personajes, países, ciudades. Se conservan en su forma solo siglas o nombres compuestos del canon (ej. una sigla o un nombre pegado tipo AbsoluteSolver) y "Internet".
- Términos de fandom en minúscula y con plural a la española pegando la -s al final: worker drones, murder drones.
- Números con cifra, no con letra: "10 años", "10 intentos", "32 megajulios".

### prohibido en narrador

- Comas.
- Signos de exclamación.
- Punto y seguido dentro del párrafo.
- Frases cortas separadas.
- Mayúscula inicial en nombres (al inicio del bloque puede aparecer, pero no es obligatoria).
- Prosa literaria solemne o adjetivos decorativos sin función.

## 3. voz PERSONAJE

### acotación (la línea de acción antes del diálogo)

- Presente, tercera persona, **verbo al frente**, casi siempre pronominal: se rasca / se soba / se rie / se encoge / se aparta / se despide / se queda / se voltea / se saca / se lleva. También simples: voltea / mira / alza / cruza / golpea / toca / abre / pasa.
- **Fórmula**: `[verbo presente] + [parte del cuerpo u objeto] + [gerundio o adjetivo de estado] + [causa opcional con "ante" / "por" / "sin" / "con"]`.
  - "se soba la sien con una mano cansado de las preguntas"
  - "alza una ceja ante el sarcasmo"
  - "cruza los brazos esperando la decision con paciencia forzada"
  - "se encoge de hombros y sigue caminando a su lado"
  - "voltea de golpe"
- **Una línea**. Máximo una coma. Dos verbos unidos por "y" como tope.
- Modificadores propios de acotación (no del narrador): "de golpe", "por lo bajo", "sin muchas ganas", "sin parar", "medio dormida", "con X en la mano", "roja hasta las orejas".
- **Variante rol**: cuando narrador y acotación se funden aparece el condicional -ría también aquí ("este apareceria", "esta abriria los ojos tambien", "esta reiria"). Se acepta.
- **Pensamiento**: acotación `en su mente` (puede llevar razón: "en su mente ya que no podia hablar") + el diálogo entero entre paréntesis `-(...)`.
- **Acotación tardía**: después del diálogo, para tono: "decia irónicamente", "decia con miedo".
- **Acotación sola**: un bloque de personaje puede ser solo acotación, sin diálogo, para marcar reacción muda.

### diálogo

- Empieza con guion. **Todo en minúscula**. Sin punto final.
- **Frase corta**: 1 o 2 ideas por línea. Las líneas largas solo se permiten en tres casos: (a) monólogo de pánico, (b) descarga técnica, (c) explicación de reglas del mundo.
- Sin comas casi siempre. La coma aparece solo tras vocativo ("no es broma humano, tu cuerpo...") o en enumeración emocional de tres golpes ("por politica, por nada").
- **Puntos suspensivos**:
  - al inicio = pausa antes de hablar: "-...no te ayudare", "-...es identico a mi"
  - en medio = tartamudeo emocional o vergüenza: "oh...eso...se me olvido"
  - antes de un sarcasmo seco: "-...¿solo eso? mejor preferiría nada"
- **Preguntas en cadena**: "¿...? ¿...? Oh ¿...?" y el "acaso" como refuerzo: "¿acaso se adapta?", "es acaso en cualquier universo". Si el personaje se abruma, suelta 4-6 preguntas seguidas sin respuesta.
- **Intensidad = MAYÚSCULA**, nunca "!". La línea puede empezar en minúscula y romper en mayúscula a mitad cuando sube la emoción: "...que acelera el proyectil a velocidad hipersónica pura SOLO DESVASTACION TOTAL".
- **Vocal alargada** para grito, queja, duda o sorpresa: UZIIIIII, KHAAAAAAN, QUEEEEEE, NORIIIIIIIII, siii, mmmmm, heeeh, huuuuuuuh, ooooh, AAAAAAAAW.
- **Reduplicación** de muletilla corta: "si si", "ok ok", "ya ya", "ey ey", "ESPERA ESPERA ESPERA".
- **Risa escrita y diferenciada por personaje** (una sola forma por personaje, se mantiene siempre): `jajajaja` (adulto, paterno), `hahahaha` / `HAHAHAHA` (maníaca, emocionada), `hehehehe` (pilla, nerviosa). En acotación: "se rie por lo bajo", "se rie sin parar".
- **Vocativo casi siempre**: el nombre en minúscula o una etiqueta de relación: humano, mortal, hermanita, bro, viejo, papa, querido, amada, mis niños, alma.
- **Palabra-firma**: cada personaje tiene UNA expresión que repite sin variación aunque no haga falta (una en cada intervención o casi). Ejemplos de tipo: un insulto fijo en mayúscula; "bro / viejo / sip"; "humano / mortal"; "ok ok / si si / como sea / mmmm". La firma no se suaviza ni se cambia por sinónimos.
- **Interjecciones**: vaya, demonios, auch, hey, ey, oh, ooooh, santa mierda.
- **Sarcasmo seco**: respuesta de 3-5 palabras después de una oferta grande. Luego acotación tardía "decia irónicamente".
- **Cierre de intercambio**: el último personaje suelta su firma o una línea de una palabra ("-si", "-hecho", "-JODETE") y el narrador retoma.

### prohibido en personaje

- Signos de exclamación.
- Mayúscula inicial en nombres.
- Diálogo largo sin uno de los tres motivos (pánico, técnica, reglas).
- Acotaciones de más de una línea.
- Adverbios en -mente dentro de la acotación (son del narrador).
- Explicar la emoción con palabras abstractas: la emoción se muestra con cuerpo, mayúscula, vocal alargada o "...".

## 4. morfología (aplica a las dos voces)

### prefijos productivos

| prefijo | forma en el texto |
|---|---|
| re- | reencarnar, reencarnado, regeneraba, recordo, recarga |
| des- | desorientado, descargar, destruir, desafortunado, desesperaba, desvastacion |
| in- / im- | inframundo, inmutarse, inocente |
| super- | superinteligencia, supercompuestos, superfuerza |
| hiper- | hipersónica |
| micro- | microrreactor |
| nano- | nanoacido |
| anti- | anti + sustantivo suelto ("anti murder drones") |

### sufijos productivos

| sufijo | función | forma en el texto |
|---|---|---|
| -mente | adverbio muletilla (narrador) | claramente, simplemente, rápidamente, básicamente, estúpidamente |
| -ría | condicional como acción de rol | apareceria, diria, agitaria, soltaria, verian |
| -stes | 2ª persona del pasado NO estándar, en TODOS los personajes | moristes, fuistes, dijistes, trajistes, recomendastes, hicistes, perdistes. Nunca "-ste" |
| -ando / -iendo | gerundio de estado (acotación) y gerundio colgado (narrador) | pensando, viendo, sosteniendo, buscando, riendo, sonrojandose |
| -ito / -ita | diminutivo afectivo o burlón | kansito, animalito, hermanita, armita, cajita |
| -azo | golpe | manotazo |
| -ción / -sión | nominalización técnica o de juicio | reencarnacion, negacion, ionización, refrigeracion, construccion, devastacion, reproducción, decision |
| -ico / -ica | adjetivo técnico | fotonica, magnético, hipersónica, criogenica, neuromórfico, termicamente |
| -oso / -osa + -idad | adjetivo de carácter y su abstracto, incluso inventado | bondadosa → bondadosidad, quisquillosa |
| -eo | acción breve | picoteo, tecleos |
| -ado / -ida | participio como estado | desorientado, emocionada, apenada, agitado |

### raíces dominantes

- reencarn-, descarg-, jod- (insulto firma), mir- / ve- (mira, mirando, viendo, veria), ri- (rie, riendo), pens- (pensando, pensativo), emocion-, agit-, sonr- (sonrie, sonrojandose), grit-, golp- (golpea, golpeando, golpe).
- Préstamos del fandom en minúscula y sin adaptar: worker, murder, drone.

### morfemas expresivos (no gramaticales, cargan emoción)

- vocal repetida = grito / queja / duda
- sílaba de risa repetida = identidad del personaje
- MAYÚSCULA total = volumen
- paréntesis = pensamiento
- "..." = pausa o tartamudeo
- reduplicación de palabra = prisa o nervios

### concordancia y artículo

- Artículo femenino ante a- tónica se conserva como marca: "una alma", "la arma", "la aura".
- Concordancia rota ocasional aceptada: "una gotas de sudor", "dos balanzas grandes aparecían temblando el lugar".
- Sujeto con "este / esta" de rebote.

## 5. marcas ortográficas fijas (son parte de la voz)

- **Sin tildes por defecto**: estaria, vacio, sabia, asi, aqui, mas, tambien, aun, que (por qué), porque (por qué), murio, abrio, dio, quedo.
- **Tilde solo en palabras largas o técnicas** que aparecen "corregidas": rápidamente, básicamente, estúpidamente, políticos, Cámara, Japón, arrepintió, admiración, magnético, hipersónica, ionización, también (a veces).
- **Sustituciones fijas**: "oh" = o (conjunción) · "hay" = ahí · "hah" = ha · "depues" = después · "losiento" · "nose" = no sé · "porfin" · "porfavor" · "almenos" · "enserio" · "aveces" · "ya ni modo".
- Nombres, gentilicios y países en minúscula.
- Errores de teclado sueltos se aceptan si no rompen la lectura (sordar = soldar, celebro = cerebro, herededo = heredero).
- Sin "!" en ninguna parte del texto.

**Modo limpio**: si el usuario pide corregir ortografía, se quitan solo las marcas de esta sección (tildes, oh/hay/depues, etc.) y se conserva TODO lo de sintaxis: narrador sin comas, condicional -ría, minúsculas en nombres, mayúsculas de volumen. El "-stes" se conserva salvo que el usuario pida quitarlo por nombre.

## 6. plantilla de escena

```
Narrador: [personaje] estaba [gerundio] [lugar] [conector colgado: hasta que / pero]

Personaje A: [se + verbo] [cuerpo/objeto] [gerundio o estado]
-[línea corta minúscula] [firma]

Personaje B: [verbo de reacción] [de golpe / por lo bajo / sin ganas]
-[respuesta corta] [MAYÚSCULA si sube] [vocativo]

Personaje A: [acotación de una línea]
-[réplica de 3-6 palabras o firma]

Narrador: [párrafo corrido sin comas: claramente x2 + lo que + enseguida + tiempos mezclados + pensamiento del personaje metido dentro + comentario sobre el canon] [termina en conector colgado o en cierre de escena]

...

Narrador: # FIN DE [X]
```

## 7. lista de control antes de entregar

1. ¿El narrador tiene alguna coma? → quitarla.
2. ¿Hay algún "!"? → cambiar a MAYÚSCULA o vocal alargada.
3. ¿Algún nombre con mayúscula inicial? → minúscula.
4. ¿"claramente" aparece al menos 2 veces en cada párrafo largo de narrador? → si no, meterlo.
5. ¿Hay al menos un condicional -ría por bloque de narrador?
6. ¿Cada acotación empieza con verbo en presente y cabe en una línea?
7. ¿Cada personaje soltó su palabra-firma al menos una vez?
8. ¿Algún "-ste"? → "-stes".
9. ¿Alguna "o" conjunción? → "oh". ¿Algún "ahí"? → "hay". ¿"después"? → "depues".
10. ¿El narrador cortó en suspenso al menos una vez antes de un bloque de personaje?
11. ¿Cada grito lleva vocal alargada?
12. ¿Cada risa usa la forma fija de ese personaje?
13. ¿El diálogo largo tiene uno de los tres motivos (pánico, técnica, reglas)? Si no, cortarlo.

## 8. flujo de trabajo (cuando se escribe una escena o capítulo)

1. Si hay un MCP de canon activo, traer SOLO los personajes y hechos de esta escena. Si falta un dato de canon, preguntar al usuario; nunca inventarlo.
2. Redactar con las reglas de esta skill. Voz NARRADOR y voz PERSONAJE separadas (regla cero).
3. Si Apodictic está instalado, pasar el borrador por `/audit` y corregir SOLO estructura o trama. NUNCA tocar la voz: ninguna sugerencia de estilo de otro plugin manda sobre esta skill.
4. Pasar la lista de control de la sección 7 antes de entregar.
5. Entregar la escena completa y después 3-5 líneas con el canon usado y lo que corrigió Apodictic (si se usó).
6. Si el usuario corrige a mano el texto entregado, ofrecer comparar su versión con la entregada y extraer las reglas nuevas a esta skill (writing-style-skill).

## 9. muestras de referencia

Los textos originales del usuario viven en `muestras/` de este repo. Cada regla de esta skill debe poder rastrearse a una cita de esas muestras; una regla sin cita no entra.
