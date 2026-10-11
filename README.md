# Course Wiki Template

A local workspace for organizing course material into a traceable,
concept-oriented wiki and study environment.

To use the template for a course, configure `course.yaml` and `study.yaml`, then
add course material under `sources/inbox`. The repository skills support the main
workflows:

- `ingest-material` catalogs sources, creates searchable extracts, and builds
  the course wiki from teaching material.
- `study-plan` and `study-block` create learning maps and teach one block at a
  time.
- `assignment-plan` and `assignment-step` plan and carry out practical
  assignment work.
- `audit-wiki` reviews the wiki's structure and content.

Practical assignments are kept separately from teaching sources and the
compiled wiki. They can provide optional examples while studying or be worked
through directly.

Install the script dependencies with:

```bash
python -m pip install -r requirements.txt
```

Searchable Markdown extraction is built in for PDF, DOCX, and PPTX sources.
PDF extracts preserve page boundaries; PowerPoint extracts preserve slide
boundaries. Office extraction includes textual document content, tables, and
PowerPoint speaker notes, and warns when visual or unsupported content requires
inspection of the immutable original.
