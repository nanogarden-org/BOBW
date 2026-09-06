"""Deterministic primitives for the B.o.B.W. v0.1 reference pipeline."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    """Return the exact SHA-256 of an input file without changing it."""
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_source_packet(path: Path, source_id: str) -> dict[str, Any]:
    """Build a minimal packet; no inference or canonicalization occurs here."""
    text = path.read_text(encoding="utf-8")
    checksum = sha256_file(path)
    segment_id = f"seg-{source_id}-0001"
    return {
        "packet_id": f"bobw-{source_id}",
        "schema_version": "0.1",
        "source": {
            "source_id": source_id,
            "original_path": str(path),
            "sha256": checksum,
            "source_type": "markdown",
            "rights_status": "unassessed",
        },
        "segments": [{
            "segment_id": segment_id,
            "locator": {"kind": "character_span", "start": 0, "end": len(text)},
            "origin_type": "source_statement",
            "transcription": text,
            "extraction_confidence": 1.0,
            "status": "proposed",
        }],
        "transformations": [{
            "run_id": f"run-{source_id}-001",
            "kind": "text_ingestion",
            "tool": "bobw-reference-cli",
            "tool_version": "0.1",
            "input_sha256": checksum,
            "output_ids": [segment_id],
        }],
        "review": {"human_verified": False, "notes": "Not canonical knowledge."},
    }
