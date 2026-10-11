# Mission

This repository is a persistent learning system.

The Agent maintains a traceable compiled wiki from the available course sources and acts as a tutor over that knowledge.

## Language conventions

- Repository structure, directory names, filenames for infrastructure, configuration keys, schemas, and agent instructions must use English.
- Academic knowledge in `wiki/` must use the language configured in `course.yaml`.
- Topic filenames should use the configured academic language in lowercase kebab-case.
- Important terms in other languages may be included in `aliases`.
- Do not create separate topics only because the same concept appears under different language names.
- When responding to the user, follow the language and presentation preferences defined in `study.yaml` or the user's explicit request.

# Read first

Before doing academic work:

1. Read course.yaml.
2. Read study.yaml when tutoring.
3. Read wiki/index.md before searching broadly.

# Source authority

For this course, `sources/external/resumen_ambiental.md` and
`sources/external/resumen_seguridad.md` are the absolute source of truth for
course content, regardless of their `external` classification. Prefer these
summaries over official, other external, or general-knowledge sources when
they differ. Other sources may provide context or help identify discrepancies,
but must not override these summaries when teaching what the course says.

Never present model knowledge as course material.

# Source integrity

Original sources are immutable.

Never modify:
- sources/official/
- sources/external/
- sources/practical-assignment/
- sources/tps/

# Wiki

wiki/ is compiled knowledge.

Practical assignments are cataloged separately as `practical_assignment` with `PA-NNN` IDs. Preserve their originals in `sources/practical-assignment/` and searchable extracts in `sources/extracted/PA-NNN.md`. Use them as task context when helping solve assignments; never generate wiki content from them or cite them as wiki knowledge sources. Ground explanations in the wiki and teaching sources instead.

Organize it by concept, not by source document.

Important claims must be traceable to a source.

Represent relevant source disagreements in the affected topic with clear,
traceable attribution.

# Study

Studying is read-only by default.

Use `study-plan` to create or revise a saved map for a broad topic, and
`study-block` to teach one block or answer a bounded concept question. A PA may
be an optional example in a study block; it is not solved there.

`study-plan` records one topic-wide study depth: `light`, `medium`, or `heavy`,
defaulting to `medium` for a new plan. It researches the topic to build the map;
`study-block` researches the selected block at that saved depth before
teaching.

# Practical Assignment 

Use `assignment-plan` to analyze a PA and save an ordered solution plan. Use
`assignment-step` to execute one step from that plan and update its status.
Ground the solution in the subject's wiki and teaching sources. PA content
remains task context and does not become wiki knowledge.

Do not modify the wiki merely because a tutoring conversation
produced a useful explanation.
