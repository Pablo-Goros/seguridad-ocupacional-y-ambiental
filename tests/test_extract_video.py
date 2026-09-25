from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_video import (  # noqa: E402
    OllamaClient,
    SYNTHESIS_INSTRUCTIONS,
    TimedText,
    analyze_frames,
    clean_markdown,
    format_timestamp,
    format_transcript,
    process_video,
    synthesize_markdown,
    transcribe_audio,
)


class FakeTranscriber:
    def __init__(self, segments: list[dict[str, object]]) -> None:
        self.segments = segments
        self.calls: list[tuple[str, dict[str, object]]] = []

    def transcribe(self, path: str, **kwargs: object) -> tuple[object, object]:
        self.calls.append((path, kwargs))
        return iter(self.segments), object()


class FakeOllama:
    def __init__(self, outputs: list[str]) -> None:
        self.outputs = outputs
        self.calls: list[dict[str, object]] = []

    def chat(self, **kwargs: object) -> str:
        self.calls.append(kwargs)
        return self.outputs.pop(0)


class ExtractVideoTests(unittest.TestCase):
    def test_ollama_client_rejects_non_local_service(self) -> None:
        with self.assertRaisesRegex(ValueError, "local loopback"):
            OllamaClient("https://example.com")

    def test_formats_sparse_source_timestamps(self) -> None:
        segments = [TimedText(0, 2, "Inicio"), TimedText(3723.6, 3730, "Tema")]

        self.assertEqual(format_timestamp(3723.6), "01:02:04")
        self.assertEqual(
            format_transcript(segments), "[00:00:00] Inicio\n[01:02:04] Tema"
        )

    def test_transcribes_locally_with_timestamps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            audio = Path(directory) / "audio.mp3"
            audio.write_bytes(b"audio")
            transcriber = FakeTranscriber(
                [
                    {"start": 2, "end": 4, "text": "Concepto A"},
                    {"start": 5, "end": 8, "text": "Concepto B"},
                ]
            )

            result = transcribe_audio(transcriber, audio, "es")

            self.assertEqual([item.start for item in result], [2, 5])
            self.assertEqual(
                [item.text for item in result], ["Concepto A", "Concepto B"]
            )
            _, kwargs = transcriber.calls[0]
            self.assertEqual(kwargs["language"], "es")
            self.assertTrue(kwargs["vad_filter"])

    def test_visual_analysis_ignores_empty_batches(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            frame = Path(directory) / "frame.jpg"
            frame.write_bytes(b"jpeg")
            ollama = FakeOllama(
                ["NO_USEFUL_VISUAL_CONTENT", "### Equation\nUseful"]
            )

            notes = analyze_frames(
                ollama, [(0, frame), (30, frame)], "local-model", batch_size=1
            )

            self.assertEqual(notes, ["### Equation\nUseful"])
            self.assertIn("Image 1: 00:00:00", ollama.calls[0]["prompt"])
            self.assertEqual(len(ollama.calls[0]["images"]), 1)

    def test_synthesis_contract_prioritizes_study_notes(self) -> None:
        ollama = FakeOllama(
            ["```markdown\n# Presión selectiva\n\nContenido.\n```"]
        )

        result = synthesize_markdown(
            ollama,
            [TimedText(10, 20, "Explicación")],
            ["Diagrama en 00:00:15"],
            "model",
            "es",
        )

        self.assertEqual(result, "# Presión selectiva\n\nContenido.\n")
        call = ollama.calls[0]
        self.assertIn("not a transcript", call["instructions"])
        self.assertEqual(call["instructions"], SYNTHESIS_INSTRUCTIONS)
        self.assertIn("[00:00:10] Explicación", call["prompt"])
        self.assertIn("Diagrama en 00:00:15", call["prompt"])

    def test_rejects_non_document_model_output(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "beginning with an H1"):
            clean_markdown("This is a transcript")

    @unittest.skipUnless(
        shutil.which("ffmpeg") and shutil.which("ffprobe"),
        "ffmpeg and ffprobe are required for the integration test",
    )
    def test_processes_real_media_but_keeps_only_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            source = temp / "lecture.mp4"
            output = temp / "OFF-001.md"
            subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error",
                    "-f", "lavfi", "-i", "color=c=white:s=320x240:d=1",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
                    "-shortest", "-c:v", "libx264", "-c:a", "aac", str(source),
                ],
                check=True,
            )
            transcriber = FakeTranscriber(
                [{"start": 0, "end": 1, "text": "Concepto"}]
            )
            ollama = FakeOllama(
                [
                    "NO_USEFUL_VISUAL_CONTENT",
                    "# Concepto\n\nExplicación útil.",
                ]
            )

            segment_count, frame_count = process_video(
                source, output, transcriber, ollama, "es", "model", 30, 10
            )

            self.assertEqual(segment_count, 1)
            self.assertEqual(frame_count, 1)
            self.assertEqual(
                output.read_text(encoding="utf-8"),
                "# Concepto\n\nExplicación útil.\n",
            )
            self.assertEqual(
                sorted(path.name for path in temp.iterdir()),
                ["OFF-001.md", "lecture.mp4"],
            )


if __name__ == "__main__":
    unittest.main()
