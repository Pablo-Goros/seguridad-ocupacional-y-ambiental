---
name: audit-wiki
description: Audit the course wiki for deterministic repository errors and semantic knowledge-quality problems. Use for wiki health reviews; report by default and modify only when fixes are explicitly requested.
---

# Audit Wiki

Audit the repository from its root. Follow `AGENTS.md`, and read
`wiki/topic-template.md` and `wiki/index.md` before reviewing topics.

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
- claims that appear to be unsupported model inference;
- wiki content derived from practical assignments, including uncited PA-based
  examples or applications; PAs are task context, not wiki knowledge sources.

Follow citations into the catalog, extracts, and originals as needed. When
sources differ, distinguish contradictions from differences in scope or
terminology using the configured source authority.

## Modification policy

The default is audit and report: do not change files. If the user explicitly
asks to audit and fix, correct clear problems within the requested scope, avoid
speculative semantic rewrites, rerun the validator, inspect the diff, and give
a detailed change summary. Do not commit or push unless explicitly requested.
