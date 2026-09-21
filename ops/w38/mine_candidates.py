"""W38 discovery: mine the 2026-09-12..09-18 dailies and the 09-18 weekly digest for candidate items with primary-source URLs.
Output: ops/w38/candidates.tsv (date, section, url, context). Discovery input only; nothing here is citable until fetched."""
import re, html
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

C = Path(r"E:\claude_code\random-apps\_briefs-corpus")
OUT = Path(__file__).with_name("candidates.tsv")
WINDOW = [f"2026-09-{d:02d}" for d in range(12, 19)]
files = [C / "daily" / "claude" / f"{d}.md" for d in WINDOW] + [C / "weekly" / "2026-09-18.md"]
url_rx = re.compile(r"\[([^\]]{0,160})\]\(<?(https?://[^\s)>]+)>?\)")
PRIMARY = ("arxiv.org", "github.com", "openai.com", "anthropic.com", "googleblog", "deepmind", "langchain", "llamaindex",
           "huggingface", "modelcontextprotocol", "vercel", "microsoft", "aws.amazon", "cloud.google", "meta.com", "mistral",
           "nvidia", "cursor", "developers.", "engineering.", "blog.", "docs.", "substack", "simonwillison", "addyosmani")
def unwrap(u):
    if "google.com/url" in u:
        q = parse_qs(urlparse(u).query).get("q", [u])[0]
        return unquote(q)
    return u
rows, seen = [], set()
for f in files:
    if not f.exists():
        continue
    section = ""
    for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("## ") or line.startswith("### "):
            section = line.lstrip("# ").replace("\\.", ".")[:80]
        for m in url_rx.finditer(line):
            label, u = html.unescape(m.group(1)), unwrap(m.group(2))
            host = urlparse(u).netloc
            if not any(p in u for p in PRIMARY):
                continue
            key = u.split("#")[0].rstrip("/")
            if key in seen:
                continue
            seen.add(key)
            ctx = re.sub(r"\s+", " ", line)[:200]
            rows.append((f.stem, section, label[:80], u, ctx))
OUT.write_text("date\tsection\tlabel\turl\tcontext\n" + "\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")
by_file = {}
for r in rows:
    by_file[r[0]] = by_file.get(r[0], 0) + 1
print("candidates:", len(rows), by_file)
hosts = {}
for r in rows:
    h = urlparse(r[3]).netloc
    hosts[h] = hosts.get(h, 0) + 1
print("hosts:", sorted(hosts.items(), key=lambda kv: -kv[1])[:10])
