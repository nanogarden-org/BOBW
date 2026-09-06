# Architecture

One packet is both the traveler and the evidence envelope. [core.py](../src/bobw/core.py) owns it; [cli.py](../src/bobw/cli.py) orchestrates individual and bulk intake. Both command names share this implementation.

| Identity | Definition | Effect of reruns or moves |
| --- | --- | --- |
| Content ID | `sha256:` plus full hash of supplied bytes | Unchanged when identical bytes move |
| Occurrence ID | Hash of normalized absolute local path | Changes when location changes; not cross-machine identity |
| Run ID | Unique ID for an invocation | New for every run |
| Packet ID | Unique observation envelope | New for each file observation, preserving prior context |
| Segment ID | Content ID plus Unicode character span | Stable for the same exact text and region |

`source_id` aliases content identity. A supplied legacy ID is retained separately. A transcript hash identifies the supplied transcript, not the original video. Source URLs are operator assertions and are labeled accordingly. `observed_at` is the processing time; unknown original capture time remains null.

## Source handling

Hashing reads 1 MiB blocks. Text extraction is limited to 2 MiB by default, configurable up to 16 MiB. Hashing and text bytes come from the same pass; a source stat change during reading fails inspection. UTF-8 Markdown and text retain original characters and line endings in JSON. Unsupported formats, oversized text and invalid UTF-8 produce explicit deferred status and no invented segments.

The human view quotes the same segment text and identifies it as supplied evidence. Markdown presentation may normalize display line endings; JSON and original bytes remain the exact evidence channels. No source text is executed. No language, confidence score or upstream processing history is inferred.

## Persistence and handoff

Each packet is assembled in a temporary sibling directory and renamed into place. Existing packet paths are never rewritten by B.o.B.W. Staging copies bytes to a temporary directory, verifies their hash, and publishes the complete candidate directory with a receipt. A failed verification leaves no published candidate. A retry of the same packet verifies and reuses its handoff; a new intake run creates a new observation and candidate copy.

Application-level immutability does not protect against external disk edits. Receipts are local integrity records, not signatures or permissions. Atomic directory rename assumes a local filesystem; power-loss recovery and network shares are not certified. Run event writes are flushed and fsynced. A terminated run lacks `summary.json`; completed packets remain available. Automatic resume and deduplicated blob storage are future work.

## Sorting and validation

`--route` overrides routing rules. Otherwise, the first extension match in the validated [JSON configuration](../config/intake.example.json) proposes a route; unmatched files go to quarantine. The YAML [contract index](../schemas/contracts.yaml) is documentation, not runtime configuration. Runtime checks validate selected identity, traceability and noncanonical invariants. They are not a general schema engine or hostile-packet parser.

Directory walking prunes output and factory destinations, symlinks, and named internal build/cache directories below each root. Roots named `build` still work. Overlapping directory roots are collapsed. Individual file failures are logged and processing continues; a directory traversal error ends that root and continues with the next root. No semantic duplicate merge occurs: shared content IDs make duplicates identifiable downstream.
