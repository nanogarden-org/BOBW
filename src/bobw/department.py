"""v0.3 department entry point; shares the evidence pipeline."""
from .cli import main, inventory_files
from .core import build_source_packet, stage_artifact, write_record

build_traveler_record = build_source_packet

if __name__ == "__main__":
    raise SystemExit(main())
