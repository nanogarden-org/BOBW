# B.o.B.W. v0.2 — Best of BOTH Worlds

> **A dual-ingestion, provenance-first Customs Agent and warehouse sorter for the Content-Factory.**

B.o.B.W. receives the user's accumulated “ore”—browser captures, YouTube transcripts, ChatGPT archives, documents, scans, images, notes, datasets, and other source material—and prepares it for the Content-Factory. It preserves the same source material in linked human-readable and machine-readable forms.

## Project legibility header

**What is this?** The B.o.B.W. Ingestion Department: a local-first Customs Agent and warehouse sorter.  
**How is it different?** It retains structured and narrative representations as linked evidence channels instead of flattening one into the other.  
**What does it do?** It inspects incoming material, records traveler provenance, proposes a Content-Factory route, and keeps human promotion authority visible.

## Start here

- [Public overview](site/index.html) — open locally in a browser.
- [Architecture](docs/architecture.md) — concepts, records, and boundaries.
- [Workflow](docs/workflow.md) — what happens to a source packet.
- [Use cases](docs/use-cases.md) — where dual ingestion helps.
- [Governance](docs/governance.md) — provenance, ambiguity, and promotion rules.
- [Purpose](docs/purpose.md) — department identity, purpose, ownership, and boundaries.
- [What and why](docs/what-and-why.md) — the problem and dual-ingestion rationale.
- [Department role](docs/department-role.md) — Customs Agent, sorter, classes, and routes.
- [Content-Factory integration](docs/content-factory-integration.md) — local root and handoffs.
- [Operations](docs/operations.md) — exact Windows commands and visible status.
- [Attribution](docs/attribution.md) — Bronson-Technologies / nanogarden-org identity.
- [Machine contracts](schemas/) — YAML examples that the code validates.
- [Reference code](src/bobw/) — packets, traveler records, sorting, staging, and events.

## Repository map

```text
site/       Browser-readable explanations of what, where, why, and how
docs/       Deeper technical and governance documentation
schemas/    YAML contracts and example data
src/        Small, inspectable reference implementation
tests/      Contract tests that guard the core invariants
fixtures/   Safe sample inputs for demonstrations
```

## Core invariant

No extracted, normalized, translated, or inferred record may sever its link to the supplied source and its transformation history. Model-generated interpretation is not source text and cannot become canonical knowledge without explicit human promotion.

## Quick demonstration

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
bobw fixtures/example_note.md --output build/demo
```

The v0.1-compatible CLI writes a source packet and human reading. The v0.2 department CLI adds a traveler-provenance JSON record, human-readable record, proposed warehouse route, optional checksum-verified staging, and append-only event logging:

```bash
bobw-intake fixtures/example_note.md --output build/records \
  --capture-class tool --domain ai \
  --reason "Reusable reference material" \
  --route reusable_material --event-log build/events/events.jsonl
```

## Status

**Department reference implementation.** No deployment, external publication, rights clearance, or autonomous canonicalization is implied by this repository. B.o.B.W. is attributed to Bronson-Technologies within nanogarden-org.

## License intent

Suggested split: code under [Apache-2.0](LICENSE), documentation under [CC BY 4.0](LICENSE-DOCS.md). Confirm the final licensing decision before any public release.
