# Content-Factory Integration

## Integration target

The default local integration root is:

```text
C:\Users\user\Documents\Atlases\Content-Factory
```

B.o.B.W. is an intake department within that system, not a replacement for the factory. It contributes preserved records and candidate routing decisions to the existing lifecycle:

```text
IDEA / OBSERVATION
  → COGNITIVE OFFLOAD
  → RAW ARTIFACT
  → ASSAY
  → WASTE / ARCHIVE / REUSABLE MATERIAL / ACTIVE PROJECT
  → COMPONENT
  → PRODUCTION
  → OUTPUT
  → SHIPPING DOCK
```

## Proposed B.o.B.W. namespace

When staging is explicitly requested, v0.2 uses this non-destructive area:

```text
Content-Factory\B.o.B.W.\
├── staging\       # copied source artifacts, checksum verified
├── records\       # JSON machine records and Markdown human records
├── events\        # append-only visible processing events
├── exports\       # candidate handoff packages
└── quarantine\    # unresolved material and review holds
```

The namespace keeps B.o.B.W. operational records separate from the factory's accepted production structures. A later human decision may update a pointer or create a downstream component; it does not rewrite the source record.

## Existing tool handoffs

### YouTube / Whisper

`C:\yt-whisper-main` remains the capture and transcription worker. B.o.B.W. records the original URL, queue context, transcript path, model, language, chunking method, completion state, and failures as processing lineage.

For long audio, the chunked Whisper worker is the appropriate retry path. A failed full-file allocation is a processing event, not evidence that the source itself is invalid.

### ChatGPT Chrome Archive

`C:\chatgpt-chrome-archive` remains an archive source. B.o.B.W. should ingest its Markdown, raw HTML, metadata, verification records, message boundaries, and SHA-256 fingerprints as supplied artifacts. Archived assistant interpretations remain derivatives and are not silently promoted to canonical knowledge.

## Recommended operating modes

1. **Inventory:** inspect and hash sources; write records outside the factory.
2. **Stage:** explicitly copy verified source artifacts into `Content-Factory\B.o.B.W.\staging`.
3. **Assay:** review rights, privacy, duplicate status, quality, class, domain, and route.
4. **Handoff:** export a candidate record to the appropriate factory registry or project packet.
5. **Promote:** human authority advances material into reusable, active, component, or production state.

The default code path is inventory/record creation. Staging requires an explicit flag.
