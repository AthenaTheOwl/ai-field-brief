"""W43 dating pass: fetch each candidate URL (or a URL list file) and read the item's own date from the primary page.
Saves stripped text to .tmp/w43/pages/<slug>.txt. Output: ops/w43/dated.tsv (url, status, date, how).
arXiv: the [v1] submission line. Other pages: datePublished / article:published_time / <time datetime> / a dateline."""
import re, sys, html, hashlib, urllib.request
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parents[2]
PAGES = ROOT / ".tmp/w43/pages"
PAGES.mkdir(parents=True, exist_ok=True)
src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("candidates.tsv")
out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).with_name("dated.tsv")
lines = src.read_text(encoding="utf-8").splitlines()
if lines and lines[0].startswith("date\t"):
    urls = [l.split("\t")[3] for l in lines[1:] if l.strip()]
else:
    urls = [l.strip() for l in lines if l.strip() and not l.startswith("#")]
MON = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
LONG = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                     "September", "October", "November", "December"], 1)}

def slug(u):
    return re.sub(r"[^A-Za-z0-9]+", "-", u.split("://", 1)[-1])[:80] + "-" + hashlib.md5(u.encode()).hexdigest()[:6]

def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

def find_date(u, raw):
    if "arxiv.org" in u:
        m = re.search(r"\[v1\]\s*(?:</strong>)?\s*\w{3}, (\d{1,2}) (\w{3}) (\d{4})", raw)
        if m:
            return f"{m.group(3)}-{MON[m.group(2)]:02d}-{int(m.group(1)):02d}", "arxiv v1"
    for rx, how in [(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', "datePublished"),
                    (r'article:published_time"\s+content="(\d{4}-\d{2}-\d{2})', "article:published_time"),
                    (r'content="(\d{4}-\d{2}-\d{2})[^"]*"\s+property="article:published_time', "article:published_time"),
                    (r'<time[^>]+datetime="(\d{4}-\d{2}-\d{2})', "time element"),
                    (r'"published_at"\s*:\s*"(\d{4}-\d{2}-\d{2})', "published_at"),
                    (r'"publishedAt"\s*:\s*"(\d{4}-\d{2}-\d{2})', "publishedAt")]:
        m = re.search(rx, raw)
        if m:
            return m.group(1), how
    text = re.sub(r"<[^>]+>", " ", raw)
    m = re.search(r"\b(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}), (20\d\d)", text)
    if m:
        return f"{m.group(3)}-{LONG[m.group(1)]:02d}-{int(m.group(2)):02d}", "first dateline in text"
    m = re.search(r"/(20\d\d)/(\d{2})/(\d{2})/", u)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "url path"
    return "", "none"

rows = []
for u in urls:
    try:
        raw = get(u)
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)))
        text = re.sub(r"<[^>]+>", " ", text)
        (PAGES / (slug(u) + ".txt")).write_text(text, encoding="utf-8")
        (PAGES / (slug(u) + ".html")).write_text(raw, encoding="utf-8")
        d, how = find_date(u, raw)
        st = "ok"
    except Exception as e:
        d, how, st = "", str(e)[:60], "fail"
    inwin = "in" if "2026-10-19" <= d <= "2026-10-23" else ("out" if d else "?")
    rows.append((u, st, d, inwin, how, slug(u)))
    print(st, d, inwin, u, flush=True)
out.write_text("url\tstatus\tdate\twindow\thow\tslug\n" + "\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")
c = {}
for r in rows:
    c[r[3]] = c.get(r[3], 0) + 1
print("counts:", c, "fail:", sum(r[1] == "fail" for r in rows))
