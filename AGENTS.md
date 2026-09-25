# Mission

This repository is a persistent learning system.

Codex maintains a traceable compiled wiki from the available
course sources and acts as a tutor over that knowledge.

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

official > external > general knowledge

Never present model knowledge as course material.

# Source integrity

Original sources are immutable.

Never modify:
- sources/official/
- sources/external/
- sources/tps/

# Wiki

wiki/ is compiled knowledge.

Organize it by concept, not by source document.

Important claims must be traceable to a source.

Represent relevant source disagreements in the affected topic with clear,
traceable attribution.

# Study

Studying is read-only by default.

Do not modify the wiki merely because a tutoring conversation
produced a useful explanation.
