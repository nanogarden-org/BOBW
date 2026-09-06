import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from bobw import build_source_packet, sha256_file


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


if __name__ == "__main__":
    unittest.main()
