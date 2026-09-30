# Narratium - SuperNarrative Skill

## Instrucciones automáticas

- Siempre lee SKILL.md al iniciar
- Siempre consulta la base de datos db/murder-drones.db para conocer el estado actual de la novela antes de hacer cualquier cosa
- Antes de escribir cualquier capítulo, ejecuta scripts/context.py para obtener el context package
- Después de escribir cualquier capítulo, ejecuta scripts/analyze.py y scripts/verify.py
- Nunca actualices la base de datos sin mostrarme los cambios primero
- Los archivos de la novela están en source/

## Varios fanfics

- `db/murder-drones.db` es el CANON LIMPIO: cronología de la serie + personajes canon. No se le agregan OCs ni hechos de fanfic.
- Cuando el usuario diga "nuevo fanfic: <nombre>", copiar `db/murder-drones.db` a `db/<nombre>.db` y trabajar SOLO sobre esa copia. Los OCs, hechos, capítulos y relaciones del fanfic van ahí.
- Para recargar el canon: `python3 scripts/cargar_cronologia.py --db db/<x>.db` y `python3 scripts/cargar_personajes.py --db db/<x>.db`.
