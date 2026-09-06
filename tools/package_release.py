"""Create a source-only download and verify local HTML links. Run from any directory."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", "__pycache__", ".venv", "output", "dist", "build"}


class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"} and value and ":" not in value and not value.startswith("#"):
                target = (self.page.parent / value.split("#")[0]).resolve()
                if not target.exists():
                    raise ValueError(f"Broken local link: {self.page} -> {value}")


def included(path):
    parts = path.relative_to(ROOT).parts
    return not any(p in EXCLUDED or p.endswith(".egg-info") for p in parts) and path.suffix not in {".pyc", ".pyo", ".zip"}


def main():
    for page in (ROOT / "site").glob("*.html"):
        parser = Links()
        parser.page = page
        parser.feed(page.read_text(encoding="utf-8"))
    destination = ROOT.parent / "BOBW-v0.3-repo.zip"
    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and included(p))
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in files if p.name != "release-manifest.json"}
    manifest_path = ROOT / "release-manifest.json"
    manifest_path.write_text(json.dumps({"version": "0.3.0", "algorithm": "sha256", "files": manifest}, indent=2) + "\n", encoding="utf-8")
    files = sorted(set(files + [manifest_path]))
    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, ROOT.name + "/" + str(path.relative_to(ROOT)))
    with ZipFile(destination) as archive:
        assert archive.testzip() is None
    print(f"Packaged {len(files)} files: {destination}")
    print("SHA-256:", hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
