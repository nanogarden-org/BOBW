# Governance and boundaries

## B.o.B.W. may

- preserve supplied sources and record checksums;
- generate derived transcriptions, translations, normalizations, and structures;
- calculate confidence and flag ambiguity;
- propose entities, relations, classifications, and duplicate candidates;
- create human- and machine-readable packages.

## B.o.B.W. may not

- present OCR, translation, or model inference as original source text;
- silently overwrite, merge, or discard source variants;
- infer rights, permission, authorship, or publication clearance;
- autonomously make a record canonical;
- publish, distribute, or submit material externally.

## Required distinctions

Every substantive record must identify one of these origins:

```yaml
origin_type: source_statement | extraction | translation | normalization | model_inference | human_confirmation
```

and one lifecycle state:

```yaml
status: unassessed | proposed | verified | unresolved | rejected | accepted_component
```

## Gate contract

`accepted_component` requires a named human decision and a retained reference to the evidence segments that support it. A rights/privacy decision, editorial decision, and release decision remain distinct gates.
