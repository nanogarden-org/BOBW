# Review: v0.1 → v0.2 → v0.3

Basis: the uploaded `BOBW-v0.1-github-repo-layout.zip` and `BOBW-v0.2-repo.zip`, plus the Bronson-Technologies [architecture map](https://github.com/nanogarden-org/bronson-technologies/blob/main/portfolio/docs/architecture-map.md) inspected on 2026-09-06. The supplied snapshots are retained under `history/`.

| Area | v0.1 | v0.2 | v0.3 |
| --- | --- | --- | --- |
| Role | Dual-representation demonstration | Ingestion department charter | Department implemented around one evidence/traveler envelope |
| Text evidence | One unbounded Markdown read | Old text pipeline separate from metadata intake | Shared bounded UTF-8 evidence path |
| Reruns | Fixed output filenames | Same-ID records overwritten | Separate immutable observation packets per run |
| Identity | Caller-supplied source ID | Hash mixed with file path | Content, occurrence, run and packet identities separated |
| Bulk intake | Absent | First-run output failure; stage flag ignored | First-run output creation, shared staging, per-file failure events |
| Ambiguous flags | Limited interface | Bulk source URL and positional input could be ignored | Reject incompatible flags with a visible usage error |
| Factory destination | Concept only | Custom destination not reflected in record | Packet destination must match requested staging root |
| Sorting | Concept only | Operator-selected route | Operator route or documented extension rules, always proposed |
| Handoff | Concept only | Source copy without full packet receipt | Verified original, paired views and local candidate receipt |
| Contracts | YAML examples | Additional examples; validation overstated | Contract index plus explicit runtime invariant checks |
| Capture truth | Minimal provenance | Processing time labeled human capture | Observation separate from unknown capture; no invented actor |
| Operations | Simple demonstration | Inventory without complete event consistency | Versioned run/event records, counts and failure exit status |
| Licensing | Suggested placeholders | Unconfirmed Apache / CC suggestions | MIT approved by owner to match TurtleML; historical suggestions retained |

## Where B.o.B.W. stands

The public architecture places B.o.B.W. at intake and Traveler-Provenance on the lineage path. V0.3 supplies a concrete local candidate packet for that boundary. It does not implement the entire portfolio architecture, nor establish that the local Content-Factory has a compatible reader installed.

The former v0.1 `source_packet.json` output and v0.2 standalone traveler are unified rather than maintained as two incompatible truths. Historical records remain valid historical artifacts; v0.3 does not reinterpret their review decisions or recreate missing provenance.

The next useful increments are upstream source manifests, OCR region records, a multilingual derivative contract, a receiving Content-Factory adapter, and a queryable cross-run content index. These are described as pending rather than implied by folder names.
