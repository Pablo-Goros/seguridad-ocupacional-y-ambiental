---
name: ingest-material
description: Catalog and extract pending course material and practical assignments; compile wiki knowledge only from teaching sources.
---

# Ingest Material

Transform classifiable files in `sources/inbox/` into preserved evidence and
source-backed wiki knowledge. Course practical-assignment instructions belong
in `sources/practical-assignment/`; also inspect unrecorded files already placed
there. Work from the repository root. Follow `AGENTS.md` and
`wiki/topic-template.md` before processing academic content.

Use `tmp/` for temporary processing artifacts such as rendered pages or
intermediate conversions. Keep final searchable extracts in
`sources/extracted/`; do not ingest files from `tmp/` automatically.

## Process the inbox

Inspect every pending file and classify it as:

- `official`: teaching material supplied by the course, chair, or instructor.
- `external`: complementary books, papers, documentation, or other outside
  resources.
- `practical_assignment`: a course consigna, rubric, starter material, or
  other instruction for a course practical assignment.

Use file contents and available provenance, not filename guesses. Leave an
ambiguous file in the inbox and report what evidence is missing. Classify course
assignments as `practical_assignment` even when supplied by the instructor.
They are task context for solving assignments, not wiki knowledge sources.

For each classifiable source:

1. Read `sources/catalog.yaml` and assign the next unused ID for its type:
   `OFF-NNN`, `EXT-NNN`, or `PA-NNN` for `official`, `external`, or
   `practical_assignment`, respectively. IDs are stable, independent of filenames, and must
   never be reassigned, recycled, or removed merely because a source changes
   location.
2. Move the original without changing its bytes to `sources/official/`,
   `sources/external/`, or `sources/practical-assignment/` for a course practical assignment.
   Do not move or rename an unrecorded file already in
   `sources/practical-assignment/`; catalog it in place.
3. Add the minimal catalog record: `id`, `title`, `type`, `path`, and
   `extracted` when an extract exists. Paths are relative to `sources/`.
4. Create an ID-named searchable extract for supported formats:

   ```bash
   # PDF, with page boundaries
   python scripts/extract_pdf.py sources/<location>/<file>.pdf --output sources/extracted/<SOURCE-ID>.md

   # Word or PowerPoint, with document structure or slide boundaries
   python scripts/extract_office.py sources/<location>/<file>.docx --output sources/extracted/<SOURCE-ID>.md
   python scripts/extract_office.py sources/<location>/<file>.pptx --output sources/extracted/<SOURCE-ID>.md

   ```

   Extraction is a regenerable retrieval aid, not authority. If important
   information depends on images, diagrams, formulas, tables, or spatial
   layout, inspect the original page when possible and do not infer missing
   meaning from extracted text. DOCX extraction preserves body paragraphs,
   headings, and tables in document order, but not Word pagination. PPTX
   extraction preserves slide boundaries, text, tables, and speaker notes.
   Extraction warnings identify files or slides that require inspection of the
   original. For other formats, preserve the original and create an ID-named
   searchable derivative only when the format can be converted without
   academic interpretation.

## Synthesize the wiki

Understand the source before editing topics. Use `wiki/index.md` as the map,
then search topic titles, aliases, synonyms, and equivalent terms. Update an
existing topic when the concept naturally belongs there. Create a new topic
only for a concept that could reasonably support an independent academic
question; never mirror document units such as classes, chapters, or slides.

For a practical assignment, stop after preserving, cataloging, and extracting
the document. Keep its questions, requirements, constraints, and supplied data
searchable in `sources/extracted/PA-NNN.md`; do not add solutions or inferred
theory to the extract. Never create or update wiki topics or the index based
on a PA, including practical applications, examples, or exam relevance. A run
containing only PAs leaves `wiki/` unchanged. In a mixed run, synthesize wiki
content only from `official` and `external` teaching sources.

Follow `wiki/topic-template.md`, adapting optional sections to the concept.
Apply the repository's language and filename conventions from `AGENTS.md`.
Prefer links over repeated explanations. Maintain meaningful `related` and
`prerequisites` relationships.

Follow the source-authority and citation rules in `AGENTS.md` and `course.yaml`.
Add exam relevance only when repository evidence supports it, and distinguish
explicit evidence from inference.

Update `wiki/index.md` after topic creation, renaming, or reorganization. Keep
it a concise navigation map rather than a course summary.

## Complete the run

Run `python scripts/validate_repo.py`, inspect the full Git diff, and report:

- sources incorporated;
- topics created and updated;
- unresolved classification or content ambiguities;
- validation problems.

Do not commit or push unless explicitly requested.
