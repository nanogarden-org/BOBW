# Content-Factory integration

Intended local factory: `C:\Users\user\Documents\Atlases\Content-Factory`.

B.o.B.W. is independently versioned and owns intake packets, events and the candidate inbox. It can run beside `C:\yt-whisper-main` and `C:\chatgpt-chrome-archive`. Those directories were described by the owner; their code and the live Windows factory were not available to this implementation session.

## Implemented handoff

With `--stage --content-factory-root <root>`, each observation enters `<root>/B.o.B.W./inbox/<packet-id>/`:

| File | Meaning |
| --- | --- |
| `original` | Verified byte copy; original filename is in the record |
| `record.json` | Traveler, source identity, evidence, transformations and proposed route |
| `human.md` | Readable view of the same packet |
| `receipt.json` | Local copy completion, content hash and record hash |

The receipt state is `received_candidate`. It establishes local delivery only. The packet still says `observed_in_place` because it records the earlier observation; the separate receipt records the subsequent copy. The sorter does not move candidates into production directories or delete waste.

## Receiver contract — pending implementation

A Content-Factory consumer should verify the receipt against `record.json` and `original`, index packet/content/occurrence IDs, and create a separate acknowledgement. It should reuse the packet ID for idempotency and retain later assay, rights, review and promotion decisions as new linked records. It must distinguish repeated observations of identical content from new evidence.

The receiver must treat all source text and routing metadata as untrusted content. No text in a transcript or chat can grant execution or publication authority. Promotion belongs to a separate accepted review decision, not the ingestion receipt.

## Neighbor components

- Capture workers own browser capture and transcription. V0.3 accepts their exported `.txt` or `.md` files; it does not run the workers or preserve their missing upstream metadata automatically.
- Chat archival workers own message boundaries, raw HTML and export metadata. Ingesting a Markdown export does not reconstruct roles, timestamps or relationships to adjacent files.
- OCR and translation workers should emit source regions, language, uncertainty and linked derivatives. Those adapters remain priorities for a later version.
- Factory assay and production own interpretation and acceptance. Shipping Dock and later commerce/release components remain downstream.

The [component catalog](../components/catalog.yaml) records these boundaries without inventing repository URLs for components that have not been created.
