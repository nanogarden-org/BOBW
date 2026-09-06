"""B.o.B.W. v0.2 ingestion department primitives.

The department has two bounded roles:

* Customs Agent: inspect incoming material, preserve identity, and issue a
  traveler-provenance record.
* Warehouse Sorter: propose a Content-Factory route without promoting the
  material to canonical knowledge.

The implementation is deliberately local-first and dependency-light so it can
run beside the user's existing Windows capture tools.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

DEFAULT_CONTENT_FACTORY_ROOT = r"C:\Users\user\Documents\Atlases\Content-Factory"
DEPARTMENT_VERSION = "0.2.0"

CAPTURE_CLASSES = {
    "project",
    "tool",
    "signal_news",
    "phase_change",
    "unclassified",
}

WAREHOUSE_ROUTES = {
    "raw_artifact",
    "reusable_material",
    "active_project",
    "archive",
    "waste",
    "quarantine",
}
SKIP_DIRECTORIES = {".git", "__pycache__", ".venv", "build"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _source_id(source_fingerprint: str, source_path: Path) -> str:
    """Create a stable identity that distinguishes duplicate files at paths."""
    path_fingerprint = sha256_bytes(str(source_path.resolve()).encode("utf-8"))
    return f"bobw-src-{source_fingerprint[:12]}-{path_fingerprint[:8]}"


def build_traveler_record(
    path: Path,
    *,
    capture_class: str = "unclassified",
    domain: Iterable[str] = (),
    capture_reason: str = "",
    source_url: str | None = None,
    captured_at: str | None = None,
) -> dict[str, Any]:
    """Create a v0.2 record without moving or modifying the source."""
    if capture_class not in CAPTURE_CLASSES:
        raise ValueError(f"Unknown capture class: {capture_class}")
    if not path.is_file():
        raise FileNotFoundError(path)

    checksum = sha256_file(path)
    source_id = _source_id(checksum, path)
    captured = captured_at or utc_now()
    return {
        "record_type": "bobw_traveler_provenance",
        "schema_version": "0.2",
        "department": {
            "name": "B.o.B.W. Ingestion Department",
            "version": DEPARTMENT_VERSION,
            "owner": "Bronson-Technologies",
            "organization": "nanogarden-org",
        },
        "source": {
            "source_id": source_id,
            "original_path": str(path.resolve()),
            "source_url": source_url,
            "filename": path.name,
            "size_bytes": path.stat().st_size,
            "sha256": checksum,
            "source_preserved": True,
        },
        "capture": {
            "captured_at": captured,
            "captured_by": "human",
            "capture_class": capture_class,
            "domain": sorted(set(domain)),
            "reason": capture_reason,
        },
        "customs": {
            "inspection_status": "inspected",
            "rights_status": "unassessed",
            "privacy_status": "unassessed",
            "duplicate_status": "unassessed",
            "source_authority": "supplied_source",
        },
        "processing": {
            "status": "captured",
            "derivatives_are_noncanonical": True,
            "transformations": [],
        },
        "warehouse": {
            "route": "quarantine",
            "route_status": "proposed",
            "destination_root": DEFAULT_CONTENT_FACTORY_ROOT,
            "promotion_authority": "human",
        },
        "review": {
            "human_verified": False,
            "canonical": False,
            "decision": "pending",
        },
    }


def sort_for_warehouse(record: dict[str, Any], route: str, *, rationale: str = "") -> dict[str, Any]:
    """Add a proposed route while keeping promotion human-gated."""
    if route not in WAREHOUSE_ROUTES:
        raise ValueError(f"Unknown warehouse route: {route}")
    updated = json.loads(json.dumps(record))
    updated["warehouse"].update({
        "route": route,
        "route_status": "proposed",
        "rationale": rationale,
    })
    updated["review"].update({"decision": "pending", "canonical": False})
    return updated


def stage_artifact(record: dict[str, Any], factory_root: Path) -> Path:
    """Copy a source into B.o.B.W. staging without overwriting a different file."""
    source = Path(record["source"]["original_path"])
    if not source.is_file():
        raise FileNotFoundError(source)
    destination_dir = factory_root / "B.o.B.W." / "staging" / record["source"]["source_id"]
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / source.name
    expected_hash = record["source"]["sha256"]
    if destination.exists():
        if sha256_file(destination) != expected_hash:
            raise FileExistsError(f"Refusing to overwrite a different staged artifact: {destination}")
        return destination
    shutil.copy2(source, destination)
    if sha256_file(destination) != expected_hash:
        raise IOError(f"Staged copy failed checksum verification: {destination}")
    return destination


def append_event(event_log: Path, event: dict[str, Any]) -> None:
    event_log.parent.mkdir(parents=True, exist_ok=True)
    with event_log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def inventory_files(root: Path) -> list[Path]:
    """Return files under a backlog root without mutating it."""
    if not root.is_dir():
        raise NotADirectoryError(root)
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and not any(part in SKIP_DIRECTORIES for part in path.parts)
    )


def write_record(record: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_id = record["source"]["source_id"]
    machine_path = output_dir / f"{source_id}.json"
    human_path = output_dir / f"{source_id}.md"
    machine_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    human_path.write_text(
        "# B.o.B.W. Traveler-Provenance Record\n\n"
        f"- **Source ID:** `{source_id}`\n"
        f"- **Class:** `{record['capture']['capture_class']}`\n"
        f"- **SHA-256:** `{record['source']['sha256']}`\n"
        f"- **Warehouse route:** `{record['warehouse']['route']}` (proposed)\n"
        "- **Canonical:** no; human review required\n\n"
        "## Capture reason\n\n"
        f"{record['capture']['reason'] or 'Not supplied.'}\n\n"
        "## Source\n\n"
        f"`{record['source']['original_path']}`\n",
        encoding="utf-8",
    )
    return machine_path, human_path


def main() -> None:
    parser = argparse.ArgumentParser(description="B.o.B.W. v0.2 Customs Agent and warehouse sorter")
    parser.add_argument("input", type=Path, nargs="?", help="One source file to inspect")
    parser.add_argument("--inventory-root", type=Path, action="append", default=[], help="Backlog directory to inventory; repeatable")
    parser.add_argument("--output", type=Path, required=True, help="Directory for the provenance record")
    parser.add_argument("--capture-class", choices=sorted(CAPTURE_CLASSES), default="unclassified")
    parser.add_argument("--domain", action="append", default=[], help="Domain tag; repeat for multiple domains")
    parser.add_argument("--reason", default="", help="Why this source was captured")
    parser.add_argument("--source-url", default=None)
    parser.add_argument("--route", choices=sorted(WAREHOUSE_ROUTES), default="quarantine")
    parser.add_argument("--route-reason", default="")
    parser.add_argument("--content-factory-root", type=Path, default=Path(DEFAULT_CONTENT_FACTORY_ROOT))
    parser.add_argument("--stage", action="store_true", help="Copy the source into the factory's B.o.B.W. staging area")
    parser.add_argument("--event-log", type=Path, default=None, help="Append visible JSONL events here")
    args = parser.parse_args()

    if args.input is None and not args.inventory_root:
        parser.error("provide an input file or at least one --inventory-root")

    if args.inventory_root:
        inventory_path = args.output / "inventory.jsonl"
        count = 0
        for root in args.inventory_root:
            for source in inventory_files(root):
                record = build_traveler_record(
                    source,
                    capture_class=args.capture_class,
                    domain=args.domain,
                    capture_reason=args.reason,
                )
                record = sort_for_warehouse(record, args.route, rationale=args.route_reason)
                with inventory_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
                if args.event_log:
                    append_event(args.event_log, {
                        "event": "BOBW_SOURCE_INVENTORIED",
                        "at": utc_now(),
                        "source_id": record["source"]["source_id"],
                        "path": record["source"]["original_path"],
                        "route": record["warehouse"]["route"],
                    })
                count += 1
                print(f"INVENTORIED {count:04d}  {record['source']['source_id']}  {source}")
        print(f"INVENTORY  {count} source(s) written to {inventory_path}")
        return

    record = build_traveler_record(
        args.input,
        capture_class=args.capture_class,
        domain=args.domain,
        capture_reason=args.reason,
        source_url=args.source_url,
    )
    record = sort_for_warehouse(record, args.route, rationale=args.route_reason)
    if args.stage:
        staged = stage_artifact(record, args.content_factory_root)
        record["processing"].update({"status": "staged", "staged_path": str(staged)})
    machine_path, human_path = write_record(record, args.output)
    event = {
        "event": "BOBW_RECORD_CREATED",
        "at": utc_now(),
        "source_id": record["source"]["source_id"],
        "capture_class": record["capture"]["capture_class"],
        "route": record["warehouse"]["route"],
        "machine_record": str(machine_path),
        "human_record": str(human_path),
    }
    if args.event_log:
        append_event(args.event_log, event)
    print(f"CAPTURED  {record['source']['source_id']}")
    print(f"CLASS     {record['capture']['capture_class']}")
    print(f"SORTED    {record['warehouse']['route']} (proposed; human gate pending)")
    print(f"MACHINE   {machine_path}")
    print(f"HUMAN     {human_path}")


if __name__ == "__main__":
    main()
