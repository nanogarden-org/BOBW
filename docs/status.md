# Current status and next increments

Version: **0.3.0**. Reviewed: **2026-09-06**. Release type: local reference implementation.

| Capability | Status |
| --- | --- |
| Inventory, streaming hash, source/content/location identities | Implemented |
| Immutable per-run packets and linked Markdown/JSON | Implemented |
| UTF-8 `.txt` / `.md` extraction up to configured size | Implemented |
| Operator classification and extension-rule route proposals | Implemented |
| Verified local candidate staging and receipt | Implemented |
| Per-file failure isolation, durable events, run summary | Implemented |
| Browser URL capture and Whisper execution | Existing external tools described by owner; not bundled or called |
| ChatGPT export message/role/HTML provenance | Adapter pending; plain exported text can be ingested |
| OCR layout/coordinates, confidence and visual review | High-priority planned adapter |
| Language detection and translations | Planned; supplied Unicode text retained now |
| Semantic classification, relations and trajectory clustering | Planned |
| Full-corpus search, duplicate index and resume | Planned |
| Factory consumer acknowledgement and promotion interface | Planned |
| Windows runtime verification | Not performed in this Linux environment |
| Standalone GitHub hosting | Public source repository: [nanogarden-org/BOBW](https://github.com/nanogarden-org/BOBW) |

## Next sequence

1. Test the fixture and a small real batch on Windows; confirm inbox location.
2. Define and implement upstream manifests for transcript and chat workers, preserving original source identity and processing history.
3. Implement the Content-Factory receiver and separate review decision records.
4. Add OCR evidence regions and multilingual derivatives with visible uncertainty.
5. Add cross-run indexing, resumable batches and deduplicated storage before staging the full archive.

The observed long-video Whisper memory failure belongs to the external transcription worker. This release's bounded text read does not repair that worker. It should be addressed there with separately verified chunking/resumption.
