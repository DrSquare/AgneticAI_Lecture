"""Build the public lecture website using only Python's standard library."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lecture_launcher.public_policy import is_public_path, validate_public_data, validate_public_file
DIST = ROOT / "dist"
ALLOWED = {".html", ".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".ico", ".pdf", ".xlsx", ".csv", ".json", ".md", ".txt"}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src", "data-read"} and value:
                self.urls.append(value)

def build():
    subprocess.run([sys.executable, str(ROOT / "refresh_lecture_index.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "refresh_lecture_index.py"), "--check"], cwd=ROOT, check=True)
    page = (ROOT / "LECTURE_DEMOS.html").read_text(encoding="utf-8")
    data = json.loads(re.search(r'<script type="application/json" id="lecture-data">(.*?)</script>', page, re.S)[1])
    validate_public_data(data)
    files = set()
    queue = []

    def add(url, base=ROOT):
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return
        candidate = ((ROOT if parsed.path.startswith("/") else base) / unquote(parsed.path).lstrip("/")).resolve()
        if not candidate.is_relative_to(ROOT) or any(p.startswith(".") for p in candidate.relative_to(ROOT).parts):
            raise ValueError(f"Non-public path: {url}")
        if not is_public_path(candidate.relative_to(ROOT).as_posix()):
            raise ValueError(f"Internal preparation file cannot be published: {url}")
        if candidate.suffix.lower() not in ALLOWED:
            raise ValueError(f"Unsupported public file: {url}")
        if not candidate.is_file():
            raise FileNotFoundError(f"Broken public link: {url}")
        if candidate not in files:
            files.add(candidate)
            queue.append(candidate)

    def scan_html(text, base=ROOT):
        links = Links()
        links.feed(text)
        for url in links.urls:
            add(url, base)

    add("LECTURE_DEMOS.html")
    for demo in data["demos"]:
        for artifact in demo["available"]:
            add(artifact["path"])
        for step in demo["steps"]:
            scan_html(step["action"])
            scan_html(step["point"])
    for path, document in data["documents"].items():
        add(path)
        scan_html(document["html"])
    while queue:
        source = queue.pop()
        if source.suffix.lower() == ".html":
            scan_html(source.read_text(encoding="utf-8"), source.parent)

    # Only replace this builder's own output directory, never project sources.
    if DIST.resolve() != ROOT / "dist" or DIST.is_symlink():
        raise ValueError("Unexpected publish directory")
    if DIST.exists():
        if not (DIST / "site-manifest.json").is_file():
            raise ValueError("Refusing to replace an unrecognized dist directory")
        shutil.rmtree(DIST)
    DIST.mkdir()
    manifest = []
    for source in sorted(files):
        validate_public_file(source)
        relative = source.relative_to(ROOT)
        target = DIST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        manifest.append({"path": relative.as_posix(), "bytes": source.stat().st_size, "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
    (DIST / "index.html").write_text(page, encoding="utf-8")
    (DIST / "404.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found</title><body style="font:1.1rem system-ui;max-width:40rem;margin:15vh auto;padding:2rem"><h1>Page not found</h1><p>This lecture file may have moved.</p><p><a href="/">Return to the four demo workspace</a></p></body></html>', encoding="utf-8")
    (DIST / "_headers").write_text("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n/*.html\n  Cache-Control: public, max-age=0, must-revalidate\n", encoding="utf-8")
    (DIST / "site-manifest.json").write_text(json.dumps({"project": "Agentic AI Lecture", "entry": "index.html", "files": manifest}, indent=2) + "\n", encoding="utf-8")
    print(f"Published bundle: {len(manifest)} linked files plus index, 404, headers and manifest; {sum(item['bytes'] for item in manifest):,} bytes")
    return 0

if __name__ == "__main__":
    raise SystemExit(build())
