# Windows operations

Extract the download. Open its `site/index.html` for the browser guide. Double-click `start-demo.cmd` for a local demonstration; it pauses with visible status. Python 3.10+ must be available as `python`.

To use the installed CLI, open a terminal in the extracted repository folder and run:

```console
python -m pip install -e .
```

Inspect a transcript without copying it into the factory:

```console
bobw "C:\yt-whisper-main\transcripts\example.txt" --output "C:\BOBW-output" --capture-class tool --reason "Evaluate for a project" --config config/intake.example.json
```

Replace `example.txt` with an existing filename. For a single source you may add `--source-url "https://..."` and `--language en`; both are recorded as operator-supplied metadata.

Inventory the transcript backlog:

```console
bobw --inventory-root "C:\yt-whisper-main\transcripts" --output "C:\BOBW-output" --config config/intake.example.json
```

Copy candidates into the intended factory:

```console
bobw --inventory-root "C:\yt-whisper-main\transcripts" --output "C:\BOBW-output" --config config/intake.example.json --stage --content-factory-root "C:\Users\user\Documents\Atlases\Content-Factory"
```

Repeat `--inventory-root` to inspect multiple directories. Choose export-only directories where possible: pointing at an entire tool project also inventories its code and metadata. Use a separate output directory outside the source tree. Automatically excluded directories are described in [architecture](architecture.md).

## Visible outcomes

`PACKAGED` means both views were written. `STAGED_CANDIDATE` means the verified original and receipt were published into the local inbox. `FAILED` or `ROOT_FAILED` records the affected source and error. Exit status is 0 for a completed run, 1 for processing failures, or 2 for invalid command syntax. The console shows totals; each run's `events.jsonl` contains paths and identities.

`PACKAGED` does not imply that extraction succeeded. Inspect `processing.status`: deferred size, encoding or unsupported-type states still produce traceable metadata. Rights and privacy remain unassessed.

Each rerun creates new observations and, if staging, additional copies. Earlier records are not overwritten. V0.3 has no `--skip-existing` or automatic resume. For large corpora, inventory first and stage a selected batch. An interrupted run lacks `summary.json`; keep it as partial evidence and rerun the affected batch to create new observations.

## Upgrade from v0.2

Keep the old output folder unchanged. Install v0.3 and select a new output location. `bobw` and `bobw-intake` are now aliases. The old fixed output names, `--event-log`, and direct `sort_for_warehouse` API are retired; events live inside each run. `--source-id` remains an optional legacy label for single inputs. `build_traveler_record` is an alias with the v0.3 `build_source_packet` signature; old keyword signatures are not guaranteed.

No migration of historical review state is performed. Do not treat fresh intake of an old record as recovery of its original source history.
