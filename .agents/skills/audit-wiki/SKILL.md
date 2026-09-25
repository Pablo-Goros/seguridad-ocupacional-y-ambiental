---
name: audit-wiki
description: Audit the course wiki for deterministic repository errors and semantic knowledge-quality problems. Use for wiki health reviews; report by default and modify only when fixes are explicitly requested.
---

# Audit Wiki

Audit the repository from its root. Read `AGENTS.md`, `course.yaml`,
`wiki/topic-template.md`, and `wiki/index.md` to preserve local contracts.

## Mechanical pass

Run:

```bash
python scripts/validate_repo.py
```

Report its actionable errors before semantic conclusions. The validator covers
repository paths, topic frontmatter and filenames, catalog integrity, source
references, topic relationships, index coverage, and obvious broken relative
Markdown links.

## Semantic pass

Review what deterministic checks cannot decide:

- concepts duplicated under different names or aliases;
- topics that are too broad or too granular to be independently useful;
- contradictory explanations or excessive duplicated content;
- missing prerequisites, suspicious relationships, and heavily referenced but
  insufficiently explained concepts;
- academic content in a language other than `course.yaml` specifies;
- exam-relevance claims without repository evidence;
- claims that appear to be unsupported model inference.

Follow citations into the catalog, extracts, and originals as needed. Apply the
authority order from `course.yaml`, and distinguish an actual contradiction
from sources that merely use different scope or terminology.

## Modification policy

The default is audit and report: do not change files. If the user explicitly
asks to audit and fix, correct clear problems within the requested scope, avoid
speculative semantic rewrites, rerun the validator, inspect the diff, and give
a detailed change summary. Do not commit or push unless explicitly requested.
