"""Faithfulness gate for W44 cells (copied from ops/w41): every ref_type=quote span must appear verbatim (whitespace-normalized,
HTML-unescaped) in its live source. GitHub release pages and pull requests are read through the API body; other pages
through their HTML with script/style blocks removed and tags replaced by spaces."""
import re, sys, json, html, subprocess, urllib.request, yaml
from urllib.parse import unquote
from pathlib import Path
cells = yaml.safe_load(open(Path(__file__).parents[2] / "briefs/2026-W44/matrix/cells.yaml", encoding="utf-8"))["cells"]
cache = {}
SCRIPT_RX = re.compile(r"(?is)<(script|style)\b[^>]*>.*?</\1>")
def norm(s):
    s = html.unescape(s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()
def gh_body(path):
    r = subprocess.run(["gh", "api", path, "--jq", ".body"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True)
    return r.stdout
def fetch(uri):
    if uri in cache:
        return cache[uri]
    rel = re.match(r"https://github\.com/([^/]+/[^/]+)/releases/tag/(.+)$", uri)
    pull = re.match(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)$", uri)
    if rel:
        text = gh_body(f"repos/{rel.group(1)}/releases/tags/{unquote(rel.group(2))}")
    elif pull:
        text = gh_body(f"repos/{pull.group(1)}/pulls/{pull.group(2)}")
    else:
        req = urllib.request.Request(uri, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        text = re.sub(r"<[^>]+>", " ", SCRIPT_RX.sub(" ", raw))
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
