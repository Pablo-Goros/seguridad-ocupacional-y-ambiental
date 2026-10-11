"""Check practical-assignment catalog separation and wiki source restrictions."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from scripts import validate_repo


class PracticalAssignmentValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.catalog = self.root / "sources/catalog.yaml"
        self.topics = self.root / "wiki/topics"
        self.topics.mkdir(parents=True)
        for relative in (
            "sources/practical-assignment/assignment.pdf",
            "sources/official/lecture.pdf",
            "sources/extracted/PA-001.md",
            "sources/extracted/OFF-001.md",
        ):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        for name, value in (("ROOT", self.root), ("CATALOG", self.catalog), ("TOPICS", self.topics)):
            self.enterContext(patch.object(validate_repo, name, value))
        self.entry = {
            "id": "PA-001",
            "title": "Assignment 1",
            "type": "practical_assignment",
            "path": "practical-assignment/assignment.pdf",
            "extracted": "extracted/PA-001.md",
        }

    def validate_entry(self, **changes):
        self.catalog.write_text(
            yaml.safe_dump({"sources": [self.entry | changes]}), encoding="utf-8"
        )
        result = validate_repo.Validation()
        ids = validate_repo.validate_catalog(result)
        return result, ids

    def test_pa_catalog_entry_is_valid(self):
        result, ids = self.validate_entry()
        self.assertEqual(result.errors, [])
        self.assertEqual(ids, {"PA-001"})

    def test_pa_type_requires_matching_id_directory_and_extract(self):
        for changes, message in (
            ({"id": "OFF-001"}, "ID prefix"),
            ({"path": "official/lecture.pdf"}, "'path' must start"),
            ({"extracted": "extracted/OFF-001.md"}, "PA extract must"),
            ({"type": "official"}, "ID prefix"),
        ):
            with self.subTest(changes=changes):
                result, _ = self.validate_entry(**changes)
                self.assertTrue(any(message in error for error in result.errors), result.errors)

    def test_teaching_source_remains_valid(self):
        result, _ = self.validate_entry(
            id="OFF-001", type="official", path="official/lecture.pdf",
            extracted="extracted/OFF-001.md",
        )
        self.assertEqual(result.errors, [])

    def test_wiki_rejects_pa_in_metadata_or_body(self):
        _, ids = self.validate_entry()
        for metadata_sources, body in ((["PA-001"], ""), ([], "Task [PA-001, p. 1]")):
            with self.subTest(metadata_sources=metadata_sources, body=body):
                metadata = {
                    "title": "Concept", "aliases": [], "sources": metadata_sources,
                    "related": [], "prerequisites": [],
                }
                (self.topics / "concept.md").write_text(
                    "---\n" + yaml.safe_dump(metadata) + "---\n" + body,
                    encoding="utf-8",
                )
                result = validate_repo.Validation()
                validate_repo.validate_topics(result, ids)
                self.assertTrue(any("cannot be a wiki knowledge source" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
