import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from bobw import build_source_packet, sha256_file
from bobw.department import build_traveler_record, sort_for_warehouse, stage_artifact


class SourcePacketTests(unittest.TestCase):
    def test_packet_retains_source_identity_and_traceability(self):
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "example.md"
            sample.write_text("hello evidence", encoding="utf-8")
            packet = build_source_packet(sample, "src-test-001")
            self.assertEqual(packet["source"]["source_id"], "src-test-001")
            self.assertEqual(packet["source"]["sha256"], hashlib.sha256(b"hello evidence").hexdigest())
            self.assertEqual(packet["segments"][0]["origin_type"], "source_statement")
            self.assertFalse(packet["review"]["human_verified"])

    def test_checksum_matches_file_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "bytes.bin"
            sample.write_bytes(b"\x00evidence\xff")
            self.assertEqual(sha256_file(sample), hashlib.sha256(b"\x00evidence\xff").hexdigest())

    def test_v02_traveler_record_preserves_identity_and_department(self):
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "captured.txt"
            sample.write_text("captured ore", encoding="utf-8")
            record = build_traveler_record(
                sample,
                capture_class="phase_change",
                domain=["quantum", "materials"],
                capture_reason="Potential infrastructure transition signal",
            )
            self.assertEqual(record["schema_version"], "0.2")
            self.assertEqual(record["department"]["owner"], "Bronson-Technologies")
            self.assertEqual(record["department"]["organization"], "nanogarden-org")
            self.assertTrue(record["source"]["source_preserved"])
            self.assertTrue(record["processing"]["derivatives_are_noncanonical"])
            self.assertFalse(record["review"]["canonical"])

    def test_sorting_stays_proposed_and_noncanonical(self):
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "captured.txt"
            sample.write_text("captured ore", encoding="utf-8")
            record = build_traveler_record(sample)
            sorted_record = sort_for_warehouse(record, "reusable_material", rationale="Needs assay")
            self.assertEqual(sorted_record["warehouse"]["route"], "reusable_material")
            self.assertEqual(sorted_record["warehouse"]["route_status"], "proposed")
            self.assertFalse(sorted_record["review"]["canonical"])

    def test_staging_is_checksum_verified_and_non_destructive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = root / "captured.txt"
            sample.write_text("captured ore", encoding="utf-8")
            record = build_traveler_record(sample)
            staged = stage_artifact(record, root / "factory")
            self.assertEqual(staged.read_text(encoding="utf-8"), "captured ore")
            self.assertEqual(staged, stage_artifact(record, root / "factory"))


if __name__ == "__main__":
    unittest.main()
