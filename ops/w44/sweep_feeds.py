"""W44 primary-feed sweep: fetch active vendor and practitioner index pages / feeds from sources/registry.yaml and list
links whose own feed entry or nearby index text carries a date inside 2026-10-24..2026-10-30. Index text dates are
leads only; each pick is re-dated from its own page before use. Output: ops/w44/feed_sweep.json + .tmp/w44/feeds/."""
import html, json, re, urllib.request
from concurrent.futures import ThreadPoolExecutor
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin

import yaml

ROOT = Path(__file__).parents[2]
CACHE = ROOT / ".tmp/w44/feeds"
CACHE.mkdir(parents=True, exist_ok=True)
IDS = ["anthropic-news", "anthropic-engineering", "claude-blog", "anthropic-alignment", "openai-news", "openai-research",
       "deepmind-blog", "google-ai-blog", "google-research-blog", "aws-ml-blog", "aws-open-source-blog", "huggingface-blog",
       "langchain-blog", "google-developers-ai-blog", "llamaindex-blog", "mcp-official-blog", "cloudflare-agents-changelog",
       "openai-api-changelog", "claude-platform-release-notes", "microsoft-research-blog", "microsoft-official-blog",
       "vercel-news", "cursor-changelog", "nvidia-dev-blog", "mistral-news", "meta-ai-blog", "meta-engineering",
       "simon-willison", "drew-breunig", "hamel-husain", "chip-huyen", "swyx-blog", "addy-osmani", "lilianweng-blog-rss",
       "karpathy-bearblog", "redis-ai-blog", "replicate-blog", "openai-harness-engineering"]
DAYS = range(24, 31)
DATE_RX = re.compile(r"\b(?:Oct(?:ober)?\.? ?(2[4-9]|30),? 2026|2026-10-(2[4-9]|30)|(2[4-9]|30) Oct(?:ober)? 2026|2026/10/(2[4-9]|30))\b")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ai-field-brief-sweep",
                                               "Accept": "text/html,application/xhtml+xml,application/xml,application/rss+xml"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def sweep(src):
    out = {"id": src["id"], "url": src["url"], "status": "ok", "hits": []}
    try:
        raw = get(src["url"])
        (CACHE / f"{src['id']}.html").write_text(raw, encoding="utf-8")
        items = re.findall(r"(?is)<(item|entry)\b.*?</\1>", raw)
        if items:  # RSS / Atom
            for it in re.findall(r"(?is)<(?:item|entry)\b.*?</(?:item|entry)>", raw):
                t = re.search(r"(?is)<title[^>]*>(.*?)</title>", it)
                l = re.search(r"(?is)<link[^>]*href=\"([^\"]+)\"|<link>(.*?)</link>", it)
                d = re.search(r"(?is)<(pubDate|published|updated|dc:date)>(.*?)</\1>", it)
                if not d:
                    continue
                ds = d.group(2).strip()
                try:
                    iso = parsedate_to_datetime(ds).date().isoformat()
                except Exception:  # noqa: BLE001
                    iso = ds[:10]
                if "2026-10-24" <= iso <= "2026-10-30":
                    title = html.unescape(re.sub(r"<!\[CDATA\[|\]\]>|<[^>]+>", "", t.group(1))).strip() if t else ""
                    link = (l.group(1) or l.group(2) or "").strip() if l else ""
                    out["hits"].append({"date": iso, "title": title[:120], "url": link, "how": "feed date"})
            out["kind"] = "feed"
            return out
        out["kind"] = "html"
        # HTML index: anchor text + href, with an in-window date inside the anchor block or within 300 chars after it
        for m in re.finditer(r"(?is)<a\b[^>]*href=\"([^\"#]+)\"[^>]*>(.*?)</a>", raw):
            href, inner = m.group(1), m.group(2)
            window = inner + raw[m.end(): m.end() + 300]
            dm = DATE_RX.search(re.sub(r"<[^>]+>", " ", window))
            if dm:
                text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", inner))).strip()
                out["hits"].append({"date_text": dm.group(0), "title": text[:120], "url": urljoin(src["url"], href),
                                    "how": "index text near link"})
        # de-dup by url
        seen, uniq = set(), []
        for h in out["hits"]:
            if h["url"] not in seen:
                seen.add(h["url"])
                uniq.append(h)
        out["hits"] = uniq
        if not out["hits"]:
            out["in_window_text_dates"] = len(DATE_RX.findall(re.sub(r"<[^>]+>", " ", raw)))
    except Exception as e:  # noqa: BLE001
        out["status"] = f"failed: {str(e)[:80]}"
    return out


reg = {s["id"]: s for s in yaml.safe_load(open(ROOT / "sources/registry.yaml", encoding="utf-8"))["sources"]}
srcs = [reg[i] for i in IDS if i in reg and reg[i].get("status") == "active"]
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(sweep, srcs))
(ROOT / "ops/w44/feed_sweep.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
for r in res:
    print(f"{r['id']:32s} {r['status'][:40]:40s} {r.get('kind','-'):5s} hits={len(r['hits'])} {r.get('in_window_text_dates','')}")
