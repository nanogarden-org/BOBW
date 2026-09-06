# v0.2 Operations

## Install locally

From the repository directory in PowerShell:

```powershell
python3 -m pip install -e .
```

## Create a record for a transcript or archive file

```powershell
bobw-intake "C:\yt-whisper-main\transcripts\example.txt" `
  --output "C:\Users\user\Documents\BOBW\records" `
  --capture-class tool `
  --domain ai `
  --reason "Captured as a reusable implementation reference" `
  --route reusable_material `
  --event-log "C:\Users\user\Documents\BOBW\events\events.jsonl"
```

## Inventory a backlog directory

Inventory is the safe first pass for the accumulated ore. It hashes every file, writes one JSON record per line, and leaves the backlog in place. Repeat `--inventory-root` for multiple source systems:

```powershell
bobw-intake --inventory-root "C:\yt-whisper-main" --inventory-root "C:\chatgpt-chrome-archive" --output "C:\Users\user\Documents\BOBW\inventory" --capture-class unclassified --route quarantine --event-log "C:\Users\user\Documents\BOBW\events\events.jsonl"
```

The inventory skips `.git`, `__pycache__`, `.venv`, and `build` directories. It does not delete, move, overwrite, or promote anything.

PowerShell uses the backtick at the end of a line to continue a command. The command can also be entered as one line.

## Stage a verified copy into Content-Factory

Add the explicit staging flag:

```powershell
bobw-intake "C:\yt-whisper-main\transcripts\example.txt" --output "C:\Users\user\Documents\BOBW\records" --capture-class tool --route reusable_material --stage
```

The source remains in place. A different artifact already occupying the destination is never overwritten.

## Inspect the existing YouTube queue

The correct single-file argument is:

```powershell
python3 yt_whisper.py --file to-be-transcribed.txt --output .\transcripts --language en --skip-existing
```

For long recordings, use the chunked worker:

```powershell
python3 yt_whisper_chunked.py --file to-be-transcribed.txt --output .\transcripts --language en --skip-existing
```

Do not concatenate filenames after `--file`; `urls.txtto-be-transcribed.txt` is interpreted as one path.

## Visible status events

Use `--event-log` to append JSON Lines records. Each line is an observable state change that can later feed a dashboard or Content-Factory report.

```text
CAPTURED → INSPECTED → SORTED (proposed) → STAGED (optional) → ASSAY → PROMOTED (human)
```

## Failure policy

- retry with chunking when full-file transcription exceeds memory
- retain the failed run as lineage
- do not mark a source invalid because one adapter failed
- preserve partial outputs as derivatives only after checksum and completeness checks
- route unresolved rights, privacy, identity, or quality issues to `quarantine`
