# Department Role: Customs Agent and Warehouse Sorter

## 1. Customs Agent

The Customs Agent operates at the border between external or scattered source material and the Content-Factory.

It asks:

- What arrived?
- Where did it come from?
- When and why was it captured?
- Is the supplied source still preserved?
- What transformations have occurred?
- What rights, privacy, duplicate, or ambiguity checks remain?

The output is the **Best of BOTH Worlds Traveler-Provenance Record**.

## 2. Warehouse Sorter

The Warehouse Sorter assigns a proposed material state. v0.2 supports:

| Route | Meaning |
|---|---|
| `raw_artifact` | Preserved material awaiting assay |
| `reusable_material` | Candidate material that may serve multiple outputs |
| `active_project` | Candidate evidence or component for a named project |
| `archive` | Retained for reference, history, or future reinspection |
| `waste` | Marked low-value or out of scope; retained until a separate policy permits disposal |
| `quarantine` | Unresolved rights, privacy, identity, quality, or routing condition |

Every route is a proposal until the human gate records a decision.

## Capture classes

The first classification lane is intentionally small:

- `project` — something to build, compare, or develop
- `tool` — software, model, framework, hardware, or workflow utility
- `signal_news` — event, policy, market, institutional, or social signal
- `phase_change` — evidence that a domain may be moving from lab to prototype, infrastructure, or adoption
- `unclassified` — captured before a class is known

These are capture classes, not final intellectual judgments. The Content-Factory assay may refine them later.

## Bounded authority

| Action | B.o.B.W. v0.2 authority |
|---|---|
| Read and hash a supplied source | allowed |
| Create linked human/machine records | allowed |
| Propose a route | allowed |
| Copy to B.o.B.W. staging with explicit `--stage` | allowed |
| Overwrite a different existing artifact | prohibited |
| Delete source material | prohibited |
| Declare canonical knowledge | prohibited without human promotion |
| Publish a product | downstream Shipping Dock only |
