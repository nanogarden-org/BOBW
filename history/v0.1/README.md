# B.o.B.W. — Best of BOTH Worlds

> **A dual-ingestion, provenance-first interface for people and AI systems.**

B.o.B.W. preserves the same source material in linked human-readable and machine-readable forms. It is designed for projects where plain text alone loses structure and schemas alone lose context: scanned archives, multilingual research, course transcripts, policy documents, technical notebooks, and AI memory systems.

## Project legibility header

**What is this?** A local-first dual-ingestion and provenance architecture.  
**How is it different?** It retains structured and narrative representations as linked evidence channels instead of flattening one into the other.  
**What does it do?** It produces inspectable Markdown, YAML/JSON records, OCR evidence locations, and review-ready transformation histories from the same source.

## Start here

- [Public overview](site/index.html) — open locally in a browser.
- [Architecture](docs/architecture.md) — concepts, records, and boundaries.
- [Workflow](docs/workflow.md) — what happens to a source packet.
- [Use cases](docs/use-cases.md) — where dual ingestion helps.
- [Governance](docs/governance.md) — provenance, ambiguity, and promotion rules.
- [Machine contracts](schemas/) — YAML examples that the code validates.
- [Minimal reference code](src/bobw/) — deterministic source-packet construction.

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

The CLI writes a `source_packet.yaml` and `human_reading.md` from one input. It is intentionally small: the value of v0.1 is the traceable contract, not pretending that one OCR or LLM engine is universal.

## Status

**Design/reference skeleton.** No deployment, external publication, rights clearance, or autonomous canonicalization is implied by this repository.

## License intent

Suggested split: code under [Apache-2.0](LICENSE), documentation under [CC BY 4.0](LICENSE-DOCS.md). Confirm the final licensing decision before any public release.
