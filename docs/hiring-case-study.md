# BOBW — engineering case study

## Problem

Document and AI workflows can lose the connection between a source file, its processed output, and the decision to accept it.

## Contribution

Designed a local intake and candidate-staging reference implementation that links captured source identity, machine-readable records, human-readable evidence, and integrity checks. This is an author-owned portfolio account of the work; repository history and attribution records provide the inspectable contribution trail. It does not imply independent external validation.

## Constraints

Preserve exact captured evidence while providing a usable human view; inspection and staging must not silently promote material to accepted or published status.

## Decision

Use linked packet views, distinct content/occurrence/run identities, and verified candidate receipts. Keep routing as a proposal.

## Working result and verification

v0.3 local reference implementation: file inventory, streaming hashes, bounded Markdown/text extraction, routing proposals, and optional verified candidate staging.

[Validation record](docs/validation.md) · [Implementation](src/bobw/core.py)

The dated validation record describes 18 local regression tests and its environment. This documentation pass does not constitute a new test run.

## Limits

Hashes establish integrity of captured bytes, not upstream authorship or truth. Source URLs are operator assertions. Candidate receipt does not mean acceptance. OCR, transcription execution, and downstream acknowledgement are not implemented.

## Business application

Document intake automation, traceable AI workflows, integrity checks, and controlled handoffs. These are relevant applications of the demonstrated design skills, not claims of deployed client outcomes or measured savings.

## Review path

Read the [project summary](../README.md), inspect the evidence above, then use the [challenge instructions](../ORIGIN.md#submit-a-useful-challenge).
