# Architecture

B.o.B.W. begins from a simple constraint: a schema without context is brittle, and prose without identity and structure is difficult to process safely. The system maintains two representations linked by one evidence spine.

## Representation layers

| Layer | Purpose | Typical formats |
|---|---|---|
| Preserved source | Original evidence; never silently altered | PDF, image, audio, `.md`, CSV |
| Evidence segments | Addressable source portions and extraction observations | YAML / JSON |
| Human legibility layer | Meaning, uncertainty, readable citations, review | Markdown / HTML |
| Machine legibility layer | Typed fields, validation, retrieval and routing | YAML / JSON |
| Interpretive overlay | Explicitly non-source suggestions, entities, relations, claims | YAML / JSON |

## Human legibility layer

The human view must expose the source excerpt or a stable link to it, source location, original language, derivation status, ambiguity, and review state. It can be pleasant to read, but not by hiding uncertainty.

## Machine legibility layer

The machine view is structured enough for deterministic validation and later ML workflows. Each field that represents source-derived content retains a `segment_id`; each transformation retains its run identity and tool/model version.

## Reconciliation

The two views are derived from the same `evidence_segment` records. Neither is the master copy. The preserved source is authoritative for what was supplied; a human-approved canonical record is authoritative only after an explicit promotion event.

## Integration boundary

- **Atlas:** B.o.B.W. exports candidate nodes and relation overlays with stable addresses. Atlas must retain their source and transformation paths.
- **Content Factory:** B.o.B.W. exports candidate source/components. It does not grant rights, editorial approval, or release permission.
- **Other agents:** consume the human or machine view according to their task, but must preserve source IDs and status fields.

See [workflow.md](workflow.md) and [governance.md](governance.md).
