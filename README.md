# Course Wiki Template

A local, Git-native workspace for turning course sources into a traceable,
concept-oriented study wiki.

The V1 workflow is:

1. `ingest-material` preserves and catalogs sources, extracts searchable text, and synthesizes supported wiki topics.
2. `study` uses the compiled wiki as a read-only tutoring layer.
3. `audit-wiki` combines deterministic validation with semantic review.

Install the script dependencies with:

```bash
python -m pip install -r requirements.txt
```

Searchable Markdown extraction is built in for PDF, DOCX, and PPTX sources.
PDF extracts preserve page boundaries; PowerPoint extracts preserve slide
boundaries. Office extraction includes textual document content, tables, and
PowerPoint speaker notes, and warns when visual or unsupported content requires
inspection of the immutable original.

Video sources produce synthesized educational Markdown rather than transcripts:

```bash
python scripts/extract_video.py sources/official/lecture-05.mp4 --output sources/extracted/OFF-005.md
```

Video processing is local-only and does not use a paid API. Install
[Ollama](https://ollama.com/download), then download the default local
vision-language model once:

```bash
ollama pull qwen2.5vl:3b
```

The extractor also requires `ffmpeg` and `ffprobe` on `PATH`; `faster-whisper`
is installed through `requirements.txt` and downloads its selected speech model
on first use. Ollama must be running while processing. The script temporarily
extracts audio and sampled frames, keeps transcript data in memory, and merges
useful spoken and visual information into structured study material in the
language configured by `course.yaml`. Source-specific intermediates are deleted;
only reusable model weights and the requested Markdown output remain. Frame
sampling can be tuned with `--frame-interval` and `--max-frames`.
