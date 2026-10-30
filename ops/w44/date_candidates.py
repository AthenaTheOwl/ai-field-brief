"""W44 dating pass: fetch every mined candidate's own primary page and read its publication date from the page
(arXiv [v1] line, page datePublished / article:published_time / <time>, URL date path, GitHub or Hugging Face API).
Pages are cached as stripped text under .tmp/w44/pages/. Output: ops/w44/dated.tsv. The digest date is never used."""
import csv, html, json, re, subprocess, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).parents[2]
CACHE = ROOT / ".tmp/w44/pages"
CACHE.mkdir(parents=True, exist_ok=True)
LO, HI = "2026-10-24", "2026-10-30"
MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
MONL = {m: i for i, m in enumerate("January February March April May June July August September October November December".split(), 1)}


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ai-field-brief-dating"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None


def strip(raw):
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))


def arxiv_id(u):
    m = re.search(r"(?:arxiv\.org/(?:abs|html|pdf)/|huggingface\.co/papers/)(\d{4}\.\d{4,5})", u)
    return m.group(1) if m else None


def date_one(i, url):
    out = {"n": i, "url": url, "date": "", "how": "", "status": "ok", "title": ""}
    try:
        aid = arxiv_id(url)
        if aid:
            raw = get(f"https://arxiv.org/abs/{aid}")
            txt = strip(raw)
            (CACHE / f"{i:03d}.txt").write_text(txt, encoding="utf-8")
            m = re.search(r"\[v1\]\s+\w{3},\s+(\d{1,2}) (\w{3}) (\d{4})", txt)
            if m:
                out["date"] = f"{m.group(3)}-{MON[m.group(2)]:02d}-{int(m.group(1)):02d}"
                out["how"] = "arxiv v1"
            t = re.search(r'<meta name="citation_title" content="([^"]+)"', raw)
            out["title"] = html.unescape(t.group(1))[:90] if t else ""
            return out
        m = re.match(r"https://github\.com/([^/]+/[^/#?]+)/?$", url)
        if m:
            j = gh(f"repos/{m.group(1)}")
            if j:
                out.update(date=j["created_at"][:10], how="github repo created_at", title=(j.get("description") or "")[:90])
            else:
                out["status"] = "gh-404"
            return out
        m = re.match(r"https://huggingface\.co/([^/]+/[^/#?]+)/?$", url)
        if m and m.group(1).split("/")[0] not in ("papers", "blog"):
            j = json.loads(get(f"https://huggingface.co/api/models/{m.group(1)}"))
            out.update(date=j.get("createdAt", "")[:10], how="hf createdAt", title=m.group(1))
            return out
        raw = get(url)
        txt = strip(raw)
        (CACHE / f"{i:03d}.txt").write_text(txt, encoding="utf-8")
        t = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
        out["title"] = html.unescape(re.sub(r"\s+", " ", t.group(1))).strip()[:90] if t else ""
        for rx, how in ((r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', "datePublished"),
                        (r'article:published_time"?\s+content="(\d{4}-\d{2}-\d{2})', "article:published_time"),
                        (r'content="(\d{4}-\d{2}-\d{2})[^"]*"\s+property="article:published_time', "article:published_time"),
                        (r'<time[^>]+datetime="(\d{4}-\d{2}-\d{2})', "time element")):
            m = re.search(rx, raw)
            if m:
                out.update(date=m.group(1), how=how)
                return out
        m = re.search(r"/(20\d\d)[/-](\d{2})[/-](\d{2})/", url)
        if m:
            out.update(date=f"{m.group(1)}-{m.group(2)}-{m.group(3)}", how="url path")
            return out
        m = re.search(r"\b(" + "|".join(MONL) + r") (\d{1,2}), (20\d\d)\b", txt)
        if m:
            out.update(date=f"{m.group(3)}-{MONL[m.group(1)]:02d}-{int(m.group(2)):02d}", how="first long-form date in text")
            return out
        out["how"] = "no date found"
    except Exception as e:  # noqa: BLE001
        out["status"] = f"fail: {str(e)[:60]}"
    return out


rows = list(csv.DictReader(open(ROOT / "ops/w44/candidates.tsv", encoding="utf-8"), delimiter="\t"))
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(lambda p: date_one(*p), [(i + 1, r["url"]) for i, r in enumerate(rows)]))
for r, row in zip(res, rows):
    d = r["date"]
    r["window"] = "in" if d and LO <= d <= HI else ("out" if d else "undated")
    r["digest_date"] = row["date"]
with open(ROOT / "ops/w44/dated.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["n", "digest_date", "date", "window", "how", "status", "title", "url"], delimiter="\t")
    w.writeheader()
    w.writerows(res)
from collections import Counter
print(Counter(r["window"] for r in res), Counter(r["status"][:8] for r in res))
