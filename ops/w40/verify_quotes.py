"""Faithfulness gate for W40 cells: every ref_type=quote span must appear verbatim (whitespace-normalized,
HTML-unescaped) in its live source. GitHub release pages are read through the API body; arXiv through the abs page."""
import re, sys, json, html, subprocess, urllib.request, yaml
from pathlib import Path
cells = yaml.safe_load(open(Path(__file__).parents[2] / "briefs/2026-W40/matrix/cells.yaml", encoding="utf-8"))["cells"]
cache = {}
def norm(s):
    s = html.unescape(s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()
def fetch(uri):
    if uri in cache:
        return cache[uri]
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/releases/tag/(.+)$", uri)
    if m:
        r = subprocess.run(["gh", "api", f"repos/{m.group(1)}/releases/tags/{m.group(2)}", "--jq", ".body"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True)
        text = r.stdout
    else:
        req = urllib.request.Request(uri, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        text = re.sub(r"<[^>]+>", " ", raw)
    cache[uri] = norm(text)
    return cache[uri]
fails, n = [], 0
for c in cells:
    for ref in c["source_refs"]:
        if ref["ref_type"] != "quote":
            continue
        n += 1
        try:
            ok = norm(ref["quote_or_span"]) in fetch(ref["uri"])
        except Exception as e:
            ok, err = False, str(e)
        if not ok:
            fails.append((c["id"], ref["uri"], ref["quote_or_span"][:90]))
print(f"quotes checked: {n}; failed: {len(fails)}")
for f in fails:
    print("  FAIL", *f)
sys.exit(1 if fails else 0)
