"""Single and bulk intake share one pipeline; visible events and isolated failures."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .core import (CLASSES, ROUTES, TEXT_LIMIT, build_source_packet, new_id,
                   stage_artifact, utc_now, write_json, write_record)

SKIP = {".git", ".venv", "__pycache__", "build"}


def load_config(path):
    config = json.loads(path.read_text(encoding="utf-8")) if path else {}
    if not isinstance(config, dict) or set(config) - {"schema_version", "text_limit_bytes", "rules"}:
        raise ValueError("Unknown config key or invalid config object")
    if config.get("schema_version", "0.3") != "0.3":
        raise ValueError("Config schema_version must be 0.3")
    limit = config.get("text_limit_bytes", TEXT_LIMIT)
    if type(limit) is not int or not 0 <= limit <= 16 * 1024 * 1024:
        raise ValueError("Invalid text_limit_bytes (0..16777216)")
    rules = config.get("rules", [])
    if not isinstance(rules, list):
        raise ValueError("rules must be a list")
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) != {"suffixes", "route", "reason"}:
            raise ValueError("Rule requires suffixes, route, reason")
        if rule["route"] not in ROUTES or not isinstance(rule["reason"], str):
            raise ValueError("Invalid rule route or reason")
        if not isinstance(rule["suffixes"], list) or not all(isinstance(s, str) and s.startswith(".") for s in rule["suffixes"]):
            raise ValueError("Rule suffixes must be extensions beginning with '.'")
    return config


def inventory_files(root, excluded=()):
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"Inventory root must be a non-symlink directory: {root}")
    excluded = [Path(p).resolve() for p in excluded]
    def blocked(path):
        absolute = path.resolve()
        return path.is_symlink() or any(absolute == e or e in absolute.parents for e in excluded)
    def walk_error(error):
        raise error
    if blocked(root):
        return
    for directory, folders, files in os.walk(root, followlinks=False, onerror=walk_error):
        base = Path(directory)
        folders[:] = sorted(f for f in folders if f not in SKIP and not blocked(base / f))
        for name in sorted(files):
            path = base / name
            if not blocked(path) and path.is_file():
                yield path


def main(argv=None):
    parser = argparse.ArgumentParser(description="B.o.B.W. v0.3 — inspect ore and propose a factory route")
    parser.add_argument("input", type=Path, nargs="?")
    parser.add_argument("--inventory-root", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--capture-class", choices=sorted(CLASSES), default="unclassified")
    parser.add_argument("--domain", action="append", default=[])
    parser.add_argument("--reason", default="")
    parser.add_argument("--source-url")
    parser.add_argument("--source-id", help="Legacy external label; never replaces content identity")
    parser.add_argument("--language", help="Operator-supplied language tag; no automatic detection")
    parser.add_argument("--route", choices=sorted(ROUTES))
    parser.add_argument("--route-reason", default="")
    parser.add_argument("--content-factory-root", type=Path)
    parser.add_argument("--stage", action="store_true")
    args = parser.parse_args(argv)
    if bool(args.input) == bool(args.inventory_root):
        parser.error("Choose one input file OR --inventory-root (repeatable)")
    if args.inventory_root and (args.source_url or args.source_id):
        parser.error("--source-url and --source-id apply to a single input only")
    if args.stage and not args.content_factory_root:
        parser.error("--stage requires --content-factory-root")
    try:
        config = load_config(args.config)
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    output = args.output.resolve()
    factory = args.content_factory_root.resolve() if args.content_factory_root else None
    if args.input and any(args.input.resolve() == p or p in args.input.resolve().parents for p in [output, factory] if p):
        parser.error("Input is inside output or factory; choose a source outside these destinations")
    roots = sorted(set(p.resolve() for p in args.inventory_root), key=lambda p: len(p.parts))
    roots = [r for r in roots if not r.is_dir() or not any(parent in roots and parent.is_dir() for parent in r.parents)]
    if any(p.is_symlink() for p in args.inventory_root):
        parser.error("Symlink inventory roots are excluded")
    run_id = new_id("run")
    run_dir = output / "runs" / run_id
    run_dir.mkdir(parents=True)
    write_json(run_dir / "run.json", {"schema_version": "0.3", "run_id": run_id,
               "started_at": utc_now(), "status": "started", "inputs": [str(args.input)] if args.input else [str(r) for r in roots],
               "config": config, "stage_requested": args.stage})
    counts = {"packets": 0, "staged": 0, "failed": 0}
    def event(kind, **fields):
        record = {"schema_version": "0.3", "event_type": kind, "at": utc_now(), "run_id": run_id, **fields}
        with (run_dir / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        print(kind, fields.get("path", fields.get("packet_id", "")), fields.get("error", ""), flush=True)
    def process(path):
        try:
            route, rationale, basis = args.route or "quarantine", args.route_reason, "operator" if args.route else "default"
            if not args.route:
                for rule in config.get("rules", []):
                    if path.suffix.lower() in [s.lower() for s in rule["suffixes"]]:
                        route, rationale, basis = rule["route"], rule["reason"], "extension_rule"
                        break
            packet = build_source_packet(path, args.source_id, run_id=run_id,
                capture_class=args.capture_class, domain=args.domain, reason=args.reason,
                source_url=args.source_url, language=args.language, route=route,
                route_reason=rationale, route_basis=basis, factory_root=factory,
                text_limit=config.get("text_limit_bytes", TEXT_LIMIT))
            machine, human = write_record(packet, run_dir / "packets")
            counts["packets"] += 1
            event("PACKAGED", path=str(path), packet_id=packet["packet_id"],
                  content_id=packet["source"]["content_id"], occurrence_id=packet["source"]["occurrence_id"],
                  record_path=str(machine), human_path=str(human), extraction=packet["processing"]["status"])
            if args.stage:
                staged = stage_artifact(packet, factory)
                counts["staged"] += 1
                event("STAGED_CANDIDATE", packet_id=packet["packet_id"], path=str(staged))
        except (OSError, ValueError) as error:
            counts["failed"] += 1
            event("FAILED", path=str(path), error=str(error))
    event("RUN_STARTED", path=str(run_dir))
    if args.input:
        process(args.input)
    else:
        for root in roots:
            try:
                for path in inventory_files(root, [output] + ([factory] if factory else [])):
                    process(path)
            except (OSError, ValueError) as error:
                counts["failed"] += 1
                event("ROOT_FAILED", path=str(root), error=str(error))
    write_json(run_dir / "summary.json", {"run_id": run_id, "finished_at": utc_now(), **counts,
               "status": "completed_with_errors" if counts["failed"] else "completed"})
    event("RUN_FINISHED", **counts)
    print(json.dumps(counts), flush=True)
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
