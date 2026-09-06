"""CLI for the narrow B.o.B.W. reference demonstration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import build_source_packet


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a B.o.B.W. dual-ingestion demonstration packet.")
    parser.add_argument("input", type=Path, help="UTF-8 Markdown input")
    parser.add_argument("--output", type=Path, required=True, help="Output directory")
    parser.add_argument("--source-id", default="src-local-001")
    args = parser.parse_args()
    packet = build_source_packet(args.input, args.source_id)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "source_packet.json").write_text(json.dumps(packet, indent=2), encoding="utf-8")
    text = packet["segments"][0]["transcription"]
    readable = f"# Human reading\n\n**Source ID:** `{args.source_id}`  \n**Status:** proposed; not canonical knowledge.\n\n---\n\n{text}"
    (args.output / "human_reading.md").write_text(readable, encoding="utf-8")


if __name__ == "__main__":
    main()
