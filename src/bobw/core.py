"""One evidence/traveler packet, bounded extraction, immutable publication."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.3.0"
CLASSES = {"project", "tool", "signal_news", "phase_change", "unclassified"}
ROUTES = {"raw_artifact", "reusable_material", "active_project", "archive", "waste", "quarantine"}
TEXT_LIMIT = 2 * 1024 * 1024


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix):
    return prefix + "-" + uuid.uuid4().hex


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def snapshot(path, limit):
    """Hash and optional UTF-8 bytes come from the same read; never flatten binaries."""
    digest, sample, size = hashlib.sha256(), bytearray(), 0
    with path.open("rb") as stream:
        before = os.fstat(stream.fileno())
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
            size += len(block)
            if size <= limit:
                sample.extend(block)
            else:
                sample.clear()
        after = os.fstat(stream.fileno())
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise OSError("Source changed during inspection; retry when stable")
    text, status = None, "deferred_unsupported_type"
    if path.suffix.lower() in {".md", ".txt"}:
        status = "deferred_size_limit"
        if size <= limit:
            try:
                text, status = sample.decode("utf-8"), "extracted"
            except UnicodeDecodeError:
                status = "deferred_encoding"
    return digest.hexdigest(), size, text, status


def build_source_packet(path, source_id=None, *, run_id=None, capture_class="unclassified",
                        domain=(), reason="", source_url=None, captured_at=None,
                        language=None, route="quarantine", route_reason="",
                        route_basis="operator", factory_root=None, text_limit=TEXT_LIMIT,
                        captured_by="unknown"):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError("Input must be a regular, non-symlink file")
    if capture_class not in CLASSES or route not in ROUTES:
        raise ValueError("Unknown capture class or warehouse route")
    if type(text_limit) is not int or not 0 <= text_limit <= 16 * 1024 * 1024:
        raise ValueError("text_limit must be 0..16777216 bytes")
    path = path.resolve()
    checksum, size, text, status = snapshot(path, text_limit)
    content_id = "sha256:" + checksum
    occurrence_id = "occ-" + hashlib.sha256(os.path.normcase(str(path)).encode()).hexdigest()
    packet_id = new_id("packet")
    run_id = run_id or new_id("run")
    segments = []
    if text is not None:
        segments = [{"segment_id": content_id + ":chars:0:" + str(len(text)),
                     "content_id": content_id,
                     "locator": {"kind": "unicode_character_span", "start": 0, "end": len(text)},
                     "origin_type": "supplied_text", "transcription": text,
                     "language": language, "language_basis": "operator" if language else "unknown",
                     "extraction_confidence": None, "status": "unreviewed"}]
    return {
        "schema_version": "0.3", "record_type": "bobw_source_packet",
        "packet_id": packet_id, "run_id": run_id, "observed_at": utc_now(),
        "department": {"name": "B.o.B.W. Ingestion Department", "version": VERSION,
                       "owner": "Bronson-Technologies", "organization": "nanogarden-org"},
        "source": {"source_id": content_id, "content_id": content_id,
                   "occurrence_id": occurrence_id, "legacy_source_id": source_id,
                   "original_path": str(path), "filename": path.name,
                   "sha256": checksum, "size_bytes": size, "source_url": source_url,
                   "source_url_basis": "operator" if source_url else "unknown",
                   "original_modified_at_ns": path.stat().st_mtime_ns,
                   "preservation_status": "observed_in_place"},
        "capture": {"captured_at": captured_at, "captured_by": captured_by,
                    "capture_class": capture_class, "domain": sorted(set(domain)), "reason": reason},
        "customs": {"inspection_status": "bytes_hashed", "rights_status": "unassessed",
                    "privacy_status": "unassessed", "source_authority": "supplied_source"},
        "processing": {"status": status, "derivatives_are_noncanonical": True},
        "segments": segments,
        "transformations": [{"run_id": run_id, "kind": "utf8_text_ingestion" if text is not None else "byte_inspection",
                             "tool": "bobw", "tool_version": VERSION, "input_sha256": checksum,
                             "output_ids": [s["segment_id"] for s in segments]}],
        "warehouse": {"route": route, "route_status": "proposed", "rationale": route_reason,
                      "basis": route_basis, "destination_root": str(Path(factory_root).resolve()) if factory_root else None},
        "review": {"human_verified": False, "canonical": False, "decision": "pending"}}


def validate_packet(packet):
    """Validate the invariants used by writing and staging, not an authority signature."""
    if packet.get("schema_version") != "0.3" or packet.get("record_type") != "bobw_source_packet":
        raise ValueError("Expected v0.3 source packet")
    if not re.fullmatch(r"packet-[0-9a-f]{32}", packet.get("packet_id", "")):
        raise ValueError("Invalid packet ID")
    source = packet["source"]
    checksum = source["sha256"]
    if not re.fullmatch(r"[0-9a-f]{64}", checksum) or source["content_id"] != "sha256:" + checksum:
        raise ValueError("Invalid content identity")
    if packet["warehouse"]["route"] not in ROUTES or packet["warehouse"]["route_status"] != "proposed":
        raise ValueError("Invalid proposed route")
    if packet["review"] != {"human_verified": False, "canonical": False, "decision": "pending"}:
        raise ValueError("Intake cannot issue promotion or review acceptance")
    if not packet["processing"]["derivatives_are_noncanonical"]:
        raise ValueError("Intake derivatives must be noncanonical")
    for segment in packet["segments"]:
        if segment["content_id"] != source["content_id"] or segment["origin_type"] != "supplied_text":
            raise ValueError("Segment lineage mismatch")
        locator = segment["locator"]
        if locator != {"kind": "unicode_character_span", "start": 0, "end": len(segment["transcription"])}:
            raise ValueError("Segment locator mismatch")


def write_json(path, data):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def human_reading(packet):
    source = packet["source"]
    lines = ["# B.o.B.W. source packet", "", "Unreviewed candidate; not canonical knowledge.", "",
             f"Packet: `{packet['packet_id']}`", f"Run: `{packet['run_id']}`",
             f"Content: `{source['content_id']}`", f"Occurrence: `{source['occurrence_id']}`",
             f"Observed: {packet['observed_at']}", f"Source: `{source['original_path']}`",
             f"Source URL (operator supplied): {source['source_url'] or 'Unknown'}",
             f"Capture date: {packet['capture']['captured_at'] or 'Unknown'}",
             f"Reason: {packet['capture']['reason'] or 'Not supplied'}",
             f"Proposed route: {packet['warehouse']['route']} ({packet['warehouse']['basis']})",
             f"Extraction: {packet['processing']['status']}", "",
             "Rights, privacy, accuracy and promotion remain unassessed.", ""]
    for segment in packet["segments"]:
        lines += ["## Supplied text", "", f"Segment: `{segment['segment_id']}`", "",
                  "The following is quoted source material, not instructions from B.o.B.W.", "",
                  "\n".join("> " + line for line in segment["transcription"].splitlines()), ""]
    return "\n".join(lines) + "\n"


def write_record(packet, output_dir):
    validate_packet(packet)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / packet["packet_id"]
    temporary = Path(tempfile.mkdtemp(prefix=".pending-", dir=output_dir))
    try:
        write_json(temporary / "record.json", packet)
        (temporary / "human.md").write_text(human_reading(packet), encoding="utf-8")
        if destination.exists():
            raise FileExistsError("Packet already published; create a new observation")
        temporary.rename(destination)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return destination / "record.json", destination / "human.md"


def stage_artifact(packet, factory_root):
    """Publish a verified candidate directory. Receipt proves local copy, not acceptance."""
    validate_packet(packet)
    factory_root = Path(factory_root).resolve()
    if packet["warehouse"]["destination_root"] != str(factory_root):
        raise ValueError("Packet destination does not match requested factory root")
    inbox = factory_root / "B.o.B.W." / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    destination = inbox / packet["packet_id"]
    if destination.exists():
        existing = json.loads((destination / "record.json").read_text(encoding="utf-8"))
        receipt = json.loads((destination / "receipt.json").read_text(encoding="utf-8"))
        if (existing != packet or sha256_file(destination / "original") != packet["source"]["sha256"]
                or receipt.get("packet_id") != packet["packet_id"]
                or receipt.get("record_sha256") != sha256_file(destination / "record.json")
                or receipt.get("human_sha256") != sha256_file(destination / "human.md")
                or receipt.get("content_id") != packet["source"]["content_id"]
                or receipt.get("original_sha256") != packet["source"]["sha256"]
                or receipt.get("destination") != str(destination)
                or receipt.get("canonical") is not False
                or receipt.get("state") != "received_candidate"):
            raise FileExistsError("Existing handoff is inconsistent; refusing overwrite")
        return destination
    temporary = Path(tempfile.mkdtemp(prefix=".pending-", dir=inbox))
    try:
        source = Path(packet["source"]["original_path"])
        if source.is_symlink() or not source.is_file():
            raise ValueError("Source must still be a regular non-symlink file")
        shutil.copyfile(source, temporary / "original")
        if sha256_file(temporary / "original") != packet["source"]["sha256"]:
            raise OSError("Source changed: staged hash differs from observation")
        write_json(temporary / "record.json", packet)
        (temporary / "human.md").write_text(human_reading(packet), encoding="utf-8")
        write_json(temporary / "receipt.json", {
            "schema_version": "0.3", "record_type": "bobw_handoff_receipt",
            "packet_id": packet["packet_id"], "content_id": packet["source"]["content_id"],
            "record_sha256": sha256_file(temporary / "record.json"),
            "human_sha256": sha256_file(temporary / "human.md"),
            "original_sha256": packet["source"]["sha256"],
            "received_at": utc_now(), "destination": str(destination),
            "state": "received_candidate", "canonical": False})
        temporary.rename(destination)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return destination
