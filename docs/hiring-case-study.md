# BOBW — engineering case study

## Problem

Document and AI workflows can lose the connection between a source file, its processed output, and the decision to accept it.

## What I built

I designed a local intake and candidate-staging reference implementation that links captured source identity, machine-readable records, human-readable evidence, and integrity checks.

## Constraints

Preserve exact captured evidence while providing a usable human view; inspection and staging must not silently promote material to accepted or published status.

## Decision

Use linked packet views, distinct content/occurrence/run identities, and verified candidate receipts. Keep routing as a proposal.

## Working result and verification

v0.3 local reference implementation: file inventory, streaming hashes, bounded Markdown/text extraction, routing proposals, and optional verified candidate staging.

[Validation record](validation.md) · [Implementation](../src/bobw/core.py)

Validation recorded September 6, 2026: 18 local regression tests on Linux with Python 3. See the validation record for coverage and platform limits.

## Limits

Hashes establish integrity of captured bytes, not upstream authorship or truth. Source URLs are operator assertions. Candidate receipt does not mean acceptance. OCR, transcription execution, and downstream acknowledgement are not implemented.

## Applications

Document intake automation, traceable AI workflows, integrity checks, and controlled handoffs.

## Further reading

Read the [project summary](../README.md), inspect the evidence above, then use the [challenge instructions](../ORIGIN.md#submit-a-useful-challenge).
