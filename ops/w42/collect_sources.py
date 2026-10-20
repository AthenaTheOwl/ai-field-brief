"""Re-fetch the public primary surfaces checked for the W42 scoped issue.

The private Drive leads are deliberately absent. Cache lives in ignored .tmp.
This collects sources; it does not verify claims or run a registry-wide sweep.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import html
import hashlib
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".tmp" / "w42-primary"
PAGES = {
    "google-eval": "https://cloud.google.com/blog/topics/developers-practitioners/four-eval-engineering-lessons",
    "anthropic-scion": "https://www.anthropic.com/engineering/redesigning-source-control",
    "deepseek-release": "https://api-docs.deepseek.com/news/news261017/",
    "deepseek-card": "https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/raw/main/README.md",
    "langchain-blog": "https://www.langchain.com/blog",
    "google-developers": "https://developers.googleblog.com/en/search/?technology=AI",
    "agentcore": "https://aws.amazon.com/blogs/machine-learning/tag/amazon-bedrock-agentcore/",
}
REPOS = {
    "langgraph": "langchain-ai/langgraph", "langsmith": "langchain-ai/langsmith-sdk",
    "openai-agents": "openai/openai-agents-python", "google-adk": "google/adk-python",
    "strands": "strands-agents/sdk-python", "mcp": "modelcontextprotocol/typescript-sdk",
    "cloudflare-agents": "cloudflare/agents", "llamaindex": "run-llama/llama_index",
    "crewai": "crewAIInc/crewAI", "e2b": "e2b-dev/E2B",
    "braintrust": "braintrustdata/braintrust-sdk", "langfuse": "langfuse/langfuse",
    "agentops": "AgentOps-AI/agentops",
}


def fetch(item):
    key, url = item
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 ai-field-brief source-audit", "Accept": "application/json, text/html, text/plain"})
        with urllib.request.urlopen(request, timeout=25) as response:
            raw = response.read().decode("utf-8", "replace")
        record = {"id": key, "url": url, "status": "ok", "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest()}
        if key in REPOS:
            (CACHE / f"{key}.txt").write_text(raw, encoding="utf-8")
            releases = json.loads(raw)
            record["releases"] = [{"tag": row["tag_name"], "published_at": row["published_at"], "url": row["html_url"], "body": row.get("body", "")} for row in releases]
        else:
            # Keep article text, excluding embedded application scripts and
            # analytics configuration that are irrelevant to the source note.
            article = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
            text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", article)))
            (CACHE / f"{key}.txt").write_text(text, encoding="utf-8")
            (CACHE / f"{key}.text.txt").write_text(text, encoding="utf-8")
        return record
    except Exception as exc:
        return {"id": key, "url": url, "status": "failed", "error": str(exc)}


if __name__ == "__main__":
    # The committed ops/w42/source-sweep.json is the dated sweep record the
    # brief cites; a rerun writes beside the cache unless --out says otherwise.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / ".tmp" / "w42" / "source-sweep.json", help="sweep report file (default: .tmp/w42/source-sweep.json)")
    out = parser.parse_args().out
    CACHE.mkdir(parents=True, exist_ok=True)
    surfaces = {**PAGES, **{key: f"https://api.github.com/repos/{repo}/releases?per_page=5" for key, repo in REPOS.items()}}
    with ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(fetch, surfaces.items()))
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "method": "20 public primary surfaces; not a full registry sweep", "surfaces": records}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for record in records:
        dates = ", ".join(f"{r['tag']} ({r['published_at'][:10]})" for r in record.get("releases", [])[:2])
        print(record["id"], record["status"], record.get("error", dates))
