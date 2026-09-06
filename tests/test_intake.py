import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from bobw.cli import main, inventory_files, load_config
from bobw.core import build_source_packet, stage_artifact, write_record, validate_packet


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "ore.txt"
        self.source.write_bytes("原文 café\r\nEvidence, not instructions.\n".encode())
        self.output = self.root / "output"
        self.factory = self.root / "factory"

    def call(self, *args):
        with contextlib.redirect_stdout(io.StringIO()):
            return main([str(a) for a in args])

    def packets(self):
        return [json.loads(p.read_text()) for p in self.output.glob("runs/*/packets/*/record.json")]

    def test_content_identity_survives_move_but_occurrence_does_not(self):
        first = build_source_packet(self.source)
        moved = self.root / "renamed.md"
        self.source.rename(moved)
        second = build_source_packet(moved)
        self.assertEqual(first["source"]["content_id"], second["source"]["content_id"])
        self.assertNotEqual(first["source"]["occurrence_id"], second["source"]["occurrence_id"])
        self.assertEqual(first["source"]["sha256"], hashlib.sha256(moved.read_bytes()).hexdigest())

    def test_rerun_preserves_prior_context_and_bytes(self):
        self.call(self.source, "--output", self.output, "--reason", "first reason")
        original = {p: p.read_bytes() for p in self.output.rglob("*") if p.is_file()}
        self.call(self.source, "--output", self.output, "--reason", "second reason")
        self.assertEqual(len(self.packets()), 2)
        self.assertEqual({p["capture"]["reason"] for p in self.packets()}, {"first reason", "second reason"})
        for path, data in original.items():
            self.assertEqual(path.read_bytes(), data)

    def test_utf8_segments_retain_crlf_and_traceability(self):
        packet = build_source_packet(self.source)
        segment = packet["segments"][0]
        self.assertEqual(segment["transcription"].encode(), self.source.read_bytes())
        self.assertIsNone(segment["extraction_confidence"])
        self.assertIsNone(packet["capture"]["captured_at"])
        self.assertEqual(packet["capture"]["captured_by"], "unknown")
        validate_packet(packet)

    def test_deferred_extraction_is_explicit(self):
        packet = build_source_packet(self.source, text_limit=2)
        self.assertEqual(packet["processing"]["status"], "deferred_size_limit")
        self.assertEqual(packet["segments"], [])
        self.source.write_bytes(b"\xff")
        self.assertEqual(build_source_packet(self.source)["processing"]["status"], "deferred_encoding")
        pdf = self.root / "sample.pdf"
        pdf.write_bytes(b"%PDF")
        self.assertEqual(build_source_packet(pdf)["processing"]["status"], "deferred_unsupported_type")

    def test_first_bulk_run_stages_and_excludes_own_outputs(self):
        args = ("--inventory-root", self.root, "--output", self.output,
                "--stage", "--content-factory-root", self.factory)
        self.assertEqual(self.call(*args), 0)
        self.assertEqual(self.call(*args), 0)
        self.assertEqual(len(self.packets()), 2)
        self.assertEqual(len(list(self.factory.glob("B.o.B.W./inbox/*/receipt.json"))), 2)
        self.assertTrue(all(p["warehouse"]["destination_root"] == str(self.factory) for p in self.packets()))

    def test_stage_idempotent_and_receipt_matches(self):
        packet = build_source_packet(self.source, factory_root=self.factory)
        path = stage_artifact(packet, self.factory)
        self.assertEqual(path, stage_artifact(packet, self.factory))
        self.assertEqual((path / "original").read_bytes(), self.source.read_bytes())
        receipt = json.loads((path / "receipt.json").read_text())
        self.assertEqual(receipt["state"], "received_candidate")
        self.assertFalse(receipt["canonical"])
        self.assertEqual(receipt["packet_id"], packet["packet_id"])
        (path / "original").write_text("tampered")
        with self.assertRaises(FileExistsError):
            stage_artifact(packet, self.factory)

    def test_changed_source_leaves_no_published_handoff(self):
        packet = build_source_packet(self.source, factory_root=self.factory)
        self.source.write_text("changed")
        with self.assertRaises(OSError):
            stage_artifact(packet, self.factory)
        self.assertEqual(list((self.factory / "B.o.B.W." / "inbox").iterdir()), [])

    def test_staged_human_view_tampering_rejected(self):
        packet = build_source_packet(self.source, factory_root=self.factory)
        path = stage_artifact(packet, self.factory)
        (path / "human.md").write_text("unrelated material")
        with self.assertRaises(FileExistsError):
            stage_artifact(packet, self.factory)

    def test_receipt_cannot_claim_promotion_on_retry(self):
        packet = build_source_packet(self.source, factory_root=self.factory)
        path = stage_artifact(packet, self.factory)
        receipt = json.loads((path / "receipt.json").read_text())
        receipt["canonical"] = True
        (path / "receipt.json").write_text(json.dumps(receipt))
        with self.assertRaises(FileExistsError):
            stage_artifact(packet, self.factory)

    def test_rejects_destination_mismatch_and_path_traversal(self):
        packet = build_source_packet(self.source, factory_root=self.factory)
        with self.assertRaises(ValueError):
            stage_artifact(packet, self.root / "wrong")
        packet["packet_id"] = "../../escape"
        with self.assertRaises(ValueError):
            write_record(packet, self.output)
        self.assertFalse(self.output.exists())

    def test_same_packet_cannot_overwrite_published_record(self):
        packet = build_source_packet(self.source)
        path, _ = write_record(packet, self.output)
        original = path.read_bytes()
        packet["capture"]["reason"] = "replacement"
        with self.assertRaises(FileExistsError):
            write_record(packet, self.output)
        self.assertEqual(path.read_bytes(), original)

    def test_intake_cannot_mark_canonical(self):
        packet = build_source_packet(self.source)
        packet["review"]["canonical"] = True
        with self.assertRaises(ValueError):
            write_record(packet, self.output)

    def test_bulk_flags_fail_explicitly(self):
        for args in [
            ("--inventory-root", self.root, "--source-url", "https://example.org"),
            (self.source, "--inventory-root", self.root),
            (self.source, "--stage"),
        ]:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                self.call(*args, "--output", self.output)
            self.assertEqual(error.exception.code, 2)

    def test_failure_isolated_and_exit_nonzero(self):
        other = self.root / "second.txt"
        other.write_text("still processed")
        def fail_one(path, *args, **kwargs):
            if path == self.source:
                raise PermissionError("test unreadable file")
            return build_source_packet(path, *args, **kwargs)
        with patch("bobw.cli.build_source_packet", side_effect=fail_one):
            self.assertEqual(self.call("--inventory-root", self.root, "--output", self.output), 1)
        self.assertEqual(len(self.packets()), 1)
        summary = json.loads(next(self.output.glob("runs/*/summary.json")).read_text())
        self.assertEqual(summary["failed"], 1)

    def test_build_named_root_is_not_excluded_and_nested_roots_deduplicated(self):
        root = self.root / "build"
        child = root / "nested"
        child.mkdir(parents=True)
        (child / "x.md").write_text("ore")
        self.assertEqual(len(list(inventory_files(root))), 1)
        self.call("--inventory-root", root, "--inventory-root", child, "--output", self.output)
        self.assertEqual(len(self.packets()), 1)

    def test_symlinks_excluded(self):
        link = self.root / "link.txt"
        try:
            link.symlink_to(self.source)
        except OSError:
            self.skipTest("Platform does not permit symlink creation")
        self.assertNotIn(link, list(inventory_files(self.root)))
        with self.assertRaises(ValueError):
            build_source_packet(link)

    def test_rules_loaded_and_manual_route_wins(self):
        config = self.root / "config.json"
        config.write_text(json.dumps({"rules": [{"suffixes": [".txt"], "route": "raw_artifact", "reason": "Text for review"}]}))
        self.call(self.source, "--output", self.output, "--config", config)
        self.call(self.source, "--output", self.output, "--config", config, "--route", "archive")
        self.assertEqual({p["warehouse"]["route"] for p in self.packets()}, {"raw_artifact", "archive"})
        config.write_text('{"typo": true}')
        with self.assertRaises(ValueError):
            load_config(config)

    def test_missing_root_does_not_stop_next_root(self):
        self.assertEqual(self.call("--inventory-root", self.root / "missing",
                        "--inventory-root", self.root, "--output", self.output), 1)
        self.assertEqual(len(self.packets()), 1)
        self.assertEqual(self.call("--inventory-root", self.root / "missing",
                                  "--output", self.output), 1)


if __name__ == "__main__":
    unittest.main()
