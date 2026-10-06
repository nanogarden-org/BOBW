# B.o.B.W. — Origin, Chronology, and Challenge Notes

## Problem observed

Mixed human/AI knowledge workflows can preserve useful transformed content while losing source identity, processing history, or the ability to reconstruct how a derivative was produced.

B.o.B.W. was developed as an intake/provenance boundary for that problem: preserve enough evidence for human review and machine processing without treating transformation as origin.

## Specific architectural treatment

This repository focuses on:

- source identity before downstream interpretation;
- linked human-readable and machine-readable packet views;
- hashes and event records for integrity and reconstruction;
- explicit distinction between inspection, staging, acceptance, and publication;
- proposed routing that does not silently become authority.

The claim is about this particular treatment and implementation history, not ownership of provenance, chain-of-custody, content credentials, ETL lineage, or archival practice as general ideas.

## Public chronology

Git history identifies artifact versions and recorded dates. Commit dates and retained snapshots alone do not establish when an artifact became publicly accessible. Public-availability claims require a separately recorded publication or archival anchor. This packet does not establish a verified first-publication date. Neither repository chronology nor publication evidence establishes universal novelty, exclusive ownership of abstract ideas, or derivation by later work.

## Why the implementation is deliberately small

The runnable model exists to make architectural claims falsifiable. A small reference implementation is easier to inspect, port, contradict, and replace than a large platform that hides assumptions behind production complexity.

## Break it

Useful failures include cases where:

1. origin and derivative identity become ambiguous;
2. a transformation cannot be reconstructed;
3. human and machine views diverge semantically;
4. integrity checks pass while the wrong source is attached;
5. staging is mistaken for acceptance or publication;
6. routing metadata gains authority it was never meant to have.

Open an issue with a counterexample, related-work reference, or minimal reproduction. A broken invariant is useful evidence for the next version.

## Evidence and challenge scope

Hashes establish integrity of captured bytes, not upstream authorship or truth. Source URLs are operator assertions. Candidate receipt does not mean acceptance. OCR, transcription execution, and downstream acknowledgement are not implemented.

[Validation record](docs/validation.md) · [Implementation](src/bobw/core.py)

## Submit a useful challenge

[Open an issue](https://github.com/nanogarden-org/BOBW/issues/new) with the version or commit SHA, invariant challenged, minimal synthetic input, commands or reasoning steps, expected versus observed behavior, and any relevant related-work link. Identify whether the challenge concerns implemented behavior or proposed architecture. Exclude private or unlicensed source material.

Recorded processing can be traced within the captured packet. Reproduction of upstream transformations requires their inputs, tools, versions, and parameters; this implementation does not recover missing upstream processing history.
