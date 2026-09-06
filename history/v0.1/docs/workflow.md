# Workflow

## 1. Intake

Preserve the file, calculate a checksum, assign a source ID, and record supplied provenance. Input is `unassessed`; no implication of rights or accuracy is made.

## 2. Extract

Extract text and, for OCR, reading order, page coordinates, tables, captions, and confidence. An extraction run is a record of an observation, not a replacement source.

## 3. Segment

Create stable IDs for addressable portions of the source. Segments carry locators such as pages and bounding boxes, or timestamps for audio/video.

## 4. Produce paired outputs

Generate human-facing Markdown and machine-facing YAML/JSON from the same segments. The reference CLI implements this minimum path; later adapters can add OCR, translation, and relation extraction.

## 5. Reconcile and review

Flag uncertain text, duplicate candidates, language ambiguity, missing provenance, and conflicts. Do not conceal an unresolved disagreement through normalization.

## 6. Promote or quarantine

Only a named human authority can promote an output to canonical/shared knowledge or an accepted Content Factory component. Everything else remains source, candidate, proposed, or unresolved.

The data examples in [`../schemas/`](../schemas/) show each required status field.
