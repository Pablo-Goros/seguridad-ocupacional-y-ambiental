---
name: ingest-material
description: Ingest pending course sources and course practical assignments into the catalog, searchable extracts, and a traceable concept-oriented wiki.
---

# Ingest Material

Transform classifiable files in `sources/inbox/` into preserved evidence and
source-backed wiki knowledge. Course practical-assignment instructions belong
in `sources/tps/`; also inspect unrecorded files already placed there. Work
from the repository root. Read `AGENTS.md`, `course.yaml`, `wiki/index.md`,
and `wiki/topic-template.md` before processing academic content.

## Process the inbox

Inspect every pending file and classify it as:

- `official`: supplied by the course, chair, or instructor.
- `external`: complementary books, papers, documentation, or other outside
  resources.
- `practical assignment`: an official consigna, rubric, starter material, or
  other instruction for a course practical assignment.

Use file contents and available provenance, not filename guesses. Leave an
ambiguous file in the inbox and report what evidence is missing. A practical
assignment remains an `official` source in the catalog; `practical assignment`
only determines its storage location and how it is used in the wiki and study.

For each classifiable source:

1. Read `sources/catalog.yaml` and assign the next unused ID for its type:
   `OFF-NNN` or `EXT-NNN`. IDs are stable, independent of filenames, and must
   never be reassigned, recycled, or removed merely because a source changes
   location.
2. Move the original without changing its bytes to `sources/official/`,
   `sources/external/`, or `sources/tps/` for a course practical assignment.
   Do not move or rename an unrecorded file already in `sources/tps/`; catalog
   it in place. Treat originals in `sources/tps/` as immutable once recorded.
3. Add the minimal catalog record: `id`, `title`, `type`, `path`, and
   `extracted` when an extract exists. Paths are relative to `sources/`.
4. Create an ID-named searchable extract for supported formats:

   ```bash
   # PDF, with page boundaries
   python scripts/extract_pdf.py sources/<location>/<file>.pdf --output sources/extracted/<SOURCE-ID>.md

   # Word or PowerPoint, with document structure or slide boundaries
   python scripts/extract_office.py sources/<location>/<file>.docx --output sources/extracted/<SOURCE-ID>.md
   python scripts/extract_office.py sources/<location>/<file>.pptx --output sources/extracted/<SOURCE-ID>.md

   # Video, synthesized from temporary audio/transcript/frame evidence
   python scripts/extract_video.py sources/<location>/<file>.mp4 --output sources/extracted/<SOURCE-ID>.md
   ```

   Extraction is a regenerable retrieval aid, not authority. If important
   information depends on images, diagrams, formulas, tables, or spatial
   layout, inspect the original page when possible and do not infer missing
   meaning from extracted text. DOCX extraction preserves body paragraphs,
   headings, and tables in document order, but not Word pagination. PPTX
   extraction preserves slide boundaries, text, tables, and speaker notes.
   Extraction warnings identify files or slides that require inspection of the
   original. Video extraction is different: its durable output is a concise,
   structured educational document synthesized from the spoken and visual
   content, not a transcript. Audio, timestamped transcript data, and sampled
   frames are disposable implementation details and must not be cataloged or
   preserved as user-facing sources. The video extract should combine related
   ideas, remove filler and repetition, preserve meaningful examples,
   equations, diagrams, code, tables, and caveats, and use timestamps only for
   major or especially useful moments. Processing is local-only: use
   `faster-whisper` for speech recognition and the loopback Ollama service with
   `qwen2.5vl:3b` for visual analysis and synthesis. It requires `ffmpeg`,
   `ffprobe`, Ollama, and the Python dependencies, but no API key or paid remote
   service. The script deletes source-specific intermediates after a successful
   or failed run; reusable local model weights may remain cached. Before the
   first run, verify Ollama is running and execute `ollama pull qwen2.5vl:3b`.
   For other formats, preserve the original and create an ID-named searchable
   derivative only when the format can be converted without academic
   interpretation.

## Synthesize the wiki

Understand the source before editing topics. Use `wiki/index.md` as the map,
then search topic titles, aliases, synonyms, and equivalent terms. Update an
existing topic when the concept naturally belongs there. Create a new topic
only for a concept that could reasonably support an independent academic
question; never mirror document units such as classes, chapters, or slides.

For a practical assignment, do not create a topic for the TP itself. Identify
the concepts, methods, data, evaluation criteria, and implementation decisions
that its consigna actually requires. Add a concise, traceable practical
application to the relevant existing topics when it improves their use for
study; cite the assignment precisely and distinguish a required task from a
general theoretical claim. An assignment spanning several concepts may update
several topics.

Follow `wiki/topic-template.md`, adapting optional sections to the concept.
Use the academic language configured in `course.yaml`, lowercase kebab-case
filenames, and aliases for important equivalent names in other languages.
Prefer links over repeated explanations. Maintain meaningful `related` and
`prerequisites` relationships.

Synthesize across sources according to `course.yaml` authority. Trace important
claims with repository citations such as `[OFF-001, p. 12]`,
`[EXT-003, pp. 45-47]`, or `[OFF-005, 00:34:20]` for a video; do not cite
general model knowledge as course evidence.
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
