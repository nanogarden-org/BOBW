# B.o.B.W. v0.3 — Best of BOTH Worlds

**The Content-Factory ingestion department: Customs Agent and warehouse sorter for your accumulated ore.**

B.o.B.W. records what arrived, keeps its evidence traceable, produces linked human-readable and machine-readable packets, and proposes where it belongs. It lowers the handling cost of a large personal corpus while keeping the path from source to usable component visible.

**Bronson-Technologies · part of nanogarden-org.** [Attribution](docs/attribution.md)

## What, why, where and how

- [Open the browser guide](site/index.html): What / Why / Where / How, with links to code and contracts.
- [Purpose and department charter](docs/purpose.md): responsibility, authority and benefit.
- [Architecture](docs/architecture.md): source identities, evidence, traveler and handoff.
- [Changes from v0.1 and v0.2](docs/version-review.md): findings, corrections and remaining limits.
- [Windows operations](docs/operations.md): copyable commands and visible outcomes.
- [Content-Factory contract](docs/content-factory-integration.md): candidate inbox and receiving responsibility.
- [Component index](components/catalog.yaml): first boundary for a future Content-Factory repository index.
- [Current capabilities and next work](docs/status.md): implemented versus planned.

## Try it

Install Python 3.10 or newer, extract this folder, and double-click **start-demo.cmd** on Windows. It reads only the synthetic fixture and writes a new run beneath `output/demo`. Python must be available as `python`.

For an installed command, open a terminal in this folder:

```console
python -m pip install -e .
bobw fixtures/example_note.md --output output/demo --config config/intake.example.json
```

Both `bobw` and `bobw-intake` now invoke the same pipeline. A run prints `RUN_STARTED`, `PACKAGED`, optional `STAGED_CANDIDATE`, failures, and `RUN_FINISHED`. It creates:

| Artifact | Purpose |
| --- | --- |
| `runs/<run-id>/run.json` | Initial run identity, inputs and routing configuration |
| `runs/<run-id>/packets/<packet-id>/record.json` | Source identity, traveler metadata, segments, transformations, proposed route |
| `runs/<run-id>/packets/<packet-id>/human.md` | Human view generated from that same record |
| `runs/<run-id>/events.jsonl` | Durable event stream and packet index |
| `runs/<run-id>/summary.json` | Completion status and counts |

Without `--stage`, originals stay in place; inspection does not create an archival copy. With staging, a verified original copy, paired views and a receipt enter the configured factory's `B.o.B.W./inbox`. The receipt means **local candidate copy received**, not review acceptance or publication.

## Release status

V0.3 is a tested local reference implementation. It supports file inventory, streaming hashes, bounded UTF-8 Markdown/text extraction, extension-based routing proposals and optional verified candidate staging. Large text and unsupported formats remain explicitly deferred. Native OCR, translation, Whisper execution, ChatGPT archive parsing and downstream consumer acknowledgement are **not implemented**.

Run manual checks with `python -m unittest discover -s tests -v`. No hosted CI workflows are included. See [validation](docs/validation.md).

The supplied v0.1 and v0.2 snapshots are retained under [history](history/README.md), outside the active package. Their commands and license placeholders are historical. V0.3 does not silently migrate existing records.

Public repository: [nanogarden-org/BOBW](https://github.com/nanogarden-org/BOBW). This repository contains the v0.3.0 source release. See [GitHub handoff](docs/github-handoff.md) for hosting and release details.

Licensed under the [MIT License](LICENSE), matching [TurtleML](https://github.com/nanogarden-org/TurtleML/blob/main/LICENSE), with copyright (c) 2026 nanogarden-org. Project attribution: Bronson-Technologies, part of nanogarden-org. The license covers this software and associated documentation; ingested third-party material retains its own terms.
