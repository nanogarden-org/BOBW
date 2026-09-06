# Validation record

Validation environment: Linux, Python 3; execution date 2026-09-06. The supplied Windows workers and live Content-Factory directory were not available here.

Manual regression suite: `python -m unittest discover -s tests -v`.

18 tests cover content identity across relocation; unchanged prior observations on rerun; Unicode and CRLF evidence; explicit extraction deferral; first-run bulk staging; output exclusions; idempotent handoff; corrupted original/human view/receipt rejection; changed-source cleanup; destination and path-ID validation; immutable packets; refusal of canonical status; incompatible CLI flags; file failure isolation; nested root selection; missing roots; symlinks; and routing rules.

The editable package installs using local build dependencies with `--no-index --no-build-isolation --no-deps`. The installed CLI and module entry point are exercised against the synthetic fixture. Runtime JSON is parsed, packet/receipt hashes are checked, and local HTML links are checked during release packaging.

This is functional verification of the local reference implementation. It is not certification of Windows operation, power-loss behavior, hostile concurrent filesystem modification, network filesystem atomicity, OCR, translation, or the external transcription and archive tools. Human review remains required for source interpretation and promotion.
