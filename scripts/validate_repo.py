#!/usr/bin/env python3
"""Run deterministic structural checks for the course wiki repository."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
import sys
from urllib.parse import unquote

try:
    import yaml
except ImportError:
    print(
        "ERROR dependency: missing 'PyYAML'; run "
        "'python -m pip install -r requirements.txt'",
        file=sys.stderr,
    )
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "wiki" / "topics"
CATALOG = ROOT / "sources" / "catalog.yaml"
INDEX = ROOT / "wiki" / "index.md"

REQUIRED_PATHS = (
    "AGENTS.md",
    "course.yaml",
    "study.yaml",
    "README.md",
    "sources/inbox",
    "sources/official",
    "sources/external",
    "sources/extracted",
    "sources/catalog.yaml",
    "wiki/index.md",
    "wiki/README.md",
    "wiki/topic-template.md",
    "wiki/topics",
    ".agents/skills/ingest-material/SKILL.md",
    ".agents/skills/study/SKILL.md",
    ".agents/skills/audit-wiki/SKILL.md",
    "scripts/extract_office.py",
    "scripts/extract_pdf.py",
    "scripts/extract_video.py",
    "scripts/validate_repo.py",
)
TOPIC_FIELDS = ("title", "aliases", "sources", "related", "prerequisites")
LIST_FIELDS = ("aliases", "sources", "related", "prerequisites")
TOPIC_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
SOURCE_ID_RE = re.compile(r"^(OFF|EXT)-\d{3,}$")
SOURCE_REFERENCE_RE = re.compile(r"\b(?:OFF|EXT)-\d{3,}\b")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


@dataclass
class Validation:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, location: str, message: str) -> None:
        self.errors.append(f"ERROR {location}: {message}")

    def warning(self, location: str, message: str) -> None:
        self.warnings.append(f"WARNING {location}: {message}")


def display(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def load_yaml(path: Path, validation: Validation) -> object | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        validation.error(display(path), f"must be UTF-8 ({exc})")
    except yaml.YAMLError as exc:
        validation.error(display(path), f"malformed YAML ({exc})")
    except OSError as exc:
        validation.error(display(path), f"cannot be read ({exc})")
    return None


def parse_frontmatter(path: Path, validation: Validation) -> tuple[dict, str] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        validation.error(display(path), f"cannot be read as UTF-8 ({exc})")
        return None

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        validation.error(display(path), "missing opening frontmatter delimiter '---'")
        return None
    try:
        closing = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        validation.error(display(path), "missing closing frontmatter delimiter '---'")
        return None

    try:
        data = yaml.safe_load("\n".join(lines[1:closing]))
    except yaml.YAMLError as exc:
        validation.error(display(path), f"malformed frontmatter YAML ({exc})")
        return None
    if not isinstance(data, dict):
        validation.error(display(path), "frontmatter must be a YAML mapping")
        return None
    return data, "\n".join(lines[closing + 1 :])


def validate_paths(validation: Validation) -> None:
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).exists():
            validation.error(relative, "required path is missing")


def safe_source_path(relative: str, location: str, validation: Validation) -> Path | None:
    candidate = (ROOT / "sources" / relative).resolve()
    sources_root = (ROOT / "sources").resolve()
    if candidate != sources_root and sources_root not in candidate.parents:
        validation.error(location, f"path escapes sources/: {relative!r}")
        return None
    return candidate


def validate_catalog(validation: Validation) -> set[str]:
    if not CATALOG.is_file():
        return set()
    data = load_yaml(CATALOG, validation)
    if data is None:
        return set()
    if not isinstance(data, dict) or set(data) != {"sources"}:
        validation.error("sources/catalog.yaml", "root must contain only a 'sources' list")
        return set()
    entries = data["sources"]
    if not isinstance(entries, list):
        validation.error("sources/catalog.yaml", "'sources' must be a list")
        return set()

    ids: set[str] = set()
    for number, entry in enumerate(entries, start=1):
        location = f"sources/catalog.yaml entry {number}"
        if not isinstance(entry, dict):
            validation.error(location, "entry must be a mapping")
            continue
        required = {"id", "title", "type", "path"}
        missing = required - set(entry)
        unknown = set(entry) - required - {"extracted"}
        if missing:
            validation.error(location, f"missing fields: {', '.join(sorted(missing))}")
        if unknown:
            validation.error(location, f"unsupported fields: {', '.join(sorted(unknown))}")

        source_id = entry.get("id")
        if not isinstance(source_id, str) or not SOURCE_ID_RE.fullmatch(source_id):
            validation.error(location, "'id' must match OFF-NNN or EXT-NNN")
        elif source_id in ids:
            validation.error(location, f"duplicate source ID {source_id}")
        else:
            ids.add(source_id)

        title = entry.get("title")
        if not isinstance(title, str) or not title.strip():
            validation.error(location, "'title' must be a non-empty string")

        source_type = entry.get("type")
        if source_type not in {"official", "external"}:
            validation.error(location, "'type' must be 'official' or 'external'")
        elif isinstance(source_id, str):
            expected_prefix = "OFF-" if source_type == "official" else "EXT-"
            if not source_id.startswith(expected_prefix):
                validation.error(location, f"ID prefix does not match type {source_type!r}")

        original = entry.get("path")
        if not isinstance(original, str) or not original.strip():
            validation.error(location, "'path' must be a non-empty string")
        else:
            allowed_dirs = {
                "official": ("official/", "tps/"),
                "external": ("external/",),
            }.get(source_type)
            normalized = original.replace("\\", "/")
            if allowed_dirs and not normalized.startswith(allowed_dirs):
                expected = " or ".join(repr(directory) for directory in allowed_dirs)
                validation.error(location, f"'path' must start with {expected}")
            resolved = safe_source_path(original, location, validation)
            if resolved is not None and not resolved.is_file():
                validation.error(location, f"original file does not exist: sources/{normalized}")

        extracted = entry.get("extracted")
        if extracted is not None:
            if not isinstance(extracted, str) or not extracted.strip():
                validation.error(location, "'extracted' must be a non-empty string when declared")
            else:
                normalized = extracted.replace("\\", "/")
                if not normalized.startswith("extracted/"):
                    validation.error(location, "'extracted' must be under extracted/")
                resolved = safe_source_path(extracted, location, validation)
                if resolved is not None and not resolved.is_file():
                    validation.error(location, f"extract does not exist: sources/{normalized}")
    return ids


def validate_topics(validation: Validation, catalog_ids: set[str]) -> dict[str, Path]:
    if not TOPICS.is_dir():
        return {}
    topic_paths = sorted(TOPICS.glob("*.md"), key=lambda path: path.name.casefold())
    folded: dict[str, str] = {}
    topics: dict[str, Path] = {}
    parsed: dict[str, tuple[dict, str]] = {}

    for path in topic_paths:
        if not TOPIC_NAME_RE.fullmatch(path.name):
            validation.error(display(path), "filename must use lowercase kebab-case.md")
        folded_name = path.name.casefold()
        if folded_name in folded:
            validation.error(display(path), f"duplicates topic filename {folded[folded_name]!r}")
        folded[folded_name] = path.name
        slug = path.stem
        topics[slug] = path

        result = parse_frontmatter(path, validation)
        if result is None:
            continue
        metadata, body = result
        parsed[slug] = result
        for field_name in TOPIC_FIELDS:
            if field_name not in metadata:
                validation.error(display(path), f"missing frontmatter field {field_name!r}")
        title = metadata.get("title")
        if not isinstance(title, str) or not title.strip():
            validation.error(display(path), "'title' must be a non-empty string")
        for field_name in LIST_FIELDS:
            value = metadata.get(field_name)
            if not isinstance(value, list):
                validation.error(display(path), f"'{field_name}' must be a list")
            elif not all(isinstance(item, str) and item.strip() for item in value):
                validation.error(display(path), f"'{field_name}' items must be non-empty strings")

        referenced_ids = set(SOURCE_REFERENCE_RE.findall(body))
        frontmatter_sources = metadata.get("sources", [])
        if isinstance(frontmatter_sources, list):
            for item in frontmatter_sources:
                if isinstance(item, str):
                    referenced_ids.update(SOURCE_REFERENCE_RE.findall(item))
        for source_id in sorted(referenced_ids - catalog_ids):
            validation.error(display(path), f"references source ID absent from catalog: {source_id}")

    for slug, (metadata, _) in parsed.items():
        for field_name in ("related", "prerequisites"):
            values = metadata.get(field_name, [])
            if not isinstance(values, list):
                continue
            for target in values:
                if not isinstance(target, str):
                    continue
                if target == slug:
                    validation.error(display(topics[slug]), f"'{field_name}' references the topic itself")
                elif target not in topics:
                    validation.error(display(topics[slug]), f"'{field_name}' references missing topic {target!r}")
    return topics


def link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " " in target:
        target = target.split(" ", 1)[0]
    return unquote(target.split("#", 1)[0].split("?", 1)[0])


def validate_markdown_links(validation: Validation, topics: dict[str, Path]) -> None:
    wiki = ROOT / "wiki"
    if not wiki.is_dir():
        return
    indexed: set[str] = set()
    for path in sorted(wiki.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            validation.error(display(path), f"cannot be read as UTF-8 ({exc})")
            continue
        for raw in MARKDOWN_LINK_RE.findall(text):
            target = link_target(raw)
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                validation.error(display(path), f"broken relative Markdown link: {raw!r}")
                continue
            if path == INDEX:
                try:
                    relative = resolved.relative_to(TOPICS.resolve())
                except ValueError:
                    continue
                if len(relative.parts) == 1 and relative.suffix == ".md":
                    indexed.add(relative.stem)

    for slug, path in sorted(topics.items()):
        if slug not in indexed:
            validation.error(display(path), "topic is not linked from wiki/index.md")


def main() -> int:
    validation = Validation()
    validate_paths(validation)
    catalog_ids = validate_catalog(validation)
    topics = validate_topics(validation, catalog_ids)
    validate_markdown_links(validation, topics)

    for message in validation.errors + validation.warnings:
        print(message)
    if validation.errors:
        print(f"Validation failed with {len(validation.errors)} error(s).")
        return 1
    print(f"Repository validation passed ({len(topics)} topic(s), {len(catalog_ids)} source(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
