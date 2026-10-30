"""W43 primary-feed sweep: fetch vendor/practitioner index pages and feeds, save them under .tmp/w43/feeds/,
and print every link that sits near an in-window date string (2026-10-19..23). Output: ops/w43/feeds.tsv.
A hit here is a lead; each item is still dated from its own page before use."""
import re, html, urllib.request
from pathlib import Path

ROOT = Path(__file__).parents[2]
OUT = ROOT / ".tmp/w43/feeds"
OUT.mkdir(parents=True, exist_ok=True)
FEEDS = {
    "anthropic-news": "https://www.anthropic.com/news",
    "anthropic-engineering": "https://www.anthropic.com/engineering",
    "anthropic-research": "https://www.anthropic.com/research",
    "anthropic-alignment": "https://alignment.anthropic.com",
    "claude-api-release-notes": "https://platform.claude.com/docs/en/release-notes/overview",
    "claude-apps-release-notes": "https://support.claude.com/en/articles/12138966-release-notes",
    "openai-news-rss": "https://openai.com/news/rss.xml",
    "openai-api-changelog": "https://developers.openai.com/api/docs/changelog",
    "openai-alignment": "https://alignment.openai.com/",
    "deepmind-blog": "https://deepmind.google/discover/blog/",
    "google-research-rss": "https://research.google/blog/rss/",
    "google-developers-ai": "https://developers.googleblog.com/en/search/?technology=AI",
    "google-cloud-ai-blog": "https://cloud.google.com/blog/products/ai-machine-learning",
    "gemini-api-changelog": "https://ai.google.dev/gemini-api/docs/changelog",
    "microsoft-research-feed": "https://www.microsoft.com/en-us/research/blog/feed/",
    "microsoft-security-blog": "https://www.microsoft.com/en-us/security/blog/",
    "aws-ml-blog": "https://aws.amazon.com/blogs/machine-learning/",
    "aws-opensource-blog": "https://aws.amazon.com/blogs/opensource/",
    "mistral-news": "https://mistral.ai/news/",
    "huggingface-blog": "https://huggingface.co/blog",
    "simon-willison-atom": "https://simonwillison.net/atom/everything/",
    "langchain-blog": "https://www.langchain.com/blog",
    "llamaindex-blog": "https://www.llamaindex.ai/blog",
    "mcp-blog": "https://blog.modelcontextprotocol.io/",
    "cloudflare-agents-changelog": "https://developers.cloudflare.com/changelog/product/agents/",
    "cloudflare-blog-rss": "https://blog.cloudflare.com/rss/",
    "vercel-changelog": "https://vercel.com/changelog",
    "cursor-changelog": "https://cursor.com/changelog",
    "github-changelog": "https://github.blog/changelog/",
    "meta-ai-blog": "https://ai.meta.com/blog/",
}
DATE_RX = re.compile(r"(2026-10-(19|20|21|22|23)|Oct(?:ober|\.)? (19|20|21|22|23),? 2026|(19|20|21|22|23) Oct(?:ober)? 2026|2026/10/(19|20|21|22|23))")
rows = []
for name, url in FEEDS.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        st = "ok"
    except Exception as e:
        raw, st = "", "fail " + str(e)[:50]
    (OUT / f"{name}.html").write_text(raw, encoding="utf-8")
    hits = []
    for m in DATE_RX.finditer(raw):
        window = raw[max(0, m.start() - 1500): m.end() + 1500]
        links = re.findall(r'(?:href="|<link>|<id>)(https?://[^"<]+|/[^"<]+)', window)
        hits.append((m.group(0), links[-3:] if links else []))
    n = len(hits)
    rows.append((name, url, st, str(n)))
    print(f"{name}\t{st}\t{n} in-window date strings\tbytes={len(raw)}", flush=True)
(Path(__file__).with_name("feeds.tsv")).write_text("feed\turl\tstatus\tin_window_date_strings\n" +
                                                   "\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")
