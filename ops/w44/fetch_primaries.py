"""W44: fetch the shortlisted primaries in full to .tmp/w44/prim/<key>.txt (stripped text) and .raw (HTML), and GitHub
release bodies via the API to .tmp/w44/prim/<key>.txt. Prints the page's own date fields for re-dating."""
import html, json, re, subprocess, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).parents[2]
OUT = ROOT / ".tmp/w44/prim"
OUT.mkdir(parents=True, exist_ok=True)
PAGES = {
    "cf-kv": "https://blog.cloudflare.com/kv-cache-exposure-remediation/",
    "meta-jit": "https://engineering.fb.com/2026/10/29/security/catching-bugs-before-they-land-jittestings-human-on-the-loop-approach-at-full-scale/",
    "msr-synth": "https://www.microsoft.com/en-us/research/blog/from-synthetic-enterprise-data-evaluations-to-real-microsoft-copilot-ai-confidence/",
    "ai2-novelty": "https://huggingface.co/blog/allenai/novelty-bench",
    "vercel-virtual": "https://vercel.com/blog/ai-gateway-virtual-models",
    "vercel-virtual-cl": "https://vercel.com/changelog/virtual-models-now-available-on-ai-gateway",
    "vercel-agent-67": "https://vercel.com/changelog/vercel-agent-sessions-now-cost-67-percent-less",
    "vercel-alerts": "https://vercel.com/changelog/vercel-agent-can-now-validate-alerts-before-paging-you",
    "gemini-carbon": "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/",
    "mistral-l4": "https://mistral.ai/news/mistral-large-4-oss/",
    "google-sleep": "https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning/",
    "breunig": "https://www.dbreunig.com/2026/10/24/the-state-of-context-engineering.html",
    "lc-company-harness": "https://www.langchain.com/blog/the-five-components-of-building-a-company-harness",
    "lc-openwiki": "https://www.langchain.com/blog/building-evidence-grounded-agent-memory-with-openwiki-and-graphs",
    "lc-mda-010": "https://www.langchain.com/blog/managed-deep-agents-v0-10-browser-use-and-asynchronous-subagents",
    "llama-dpp": "https://www.llamaindex.ai/blog/introducing-the-document-parsing-protocol",
    "llama-maxeffort": "https://www.llamaindex.ai/blog/introducing-max-effort-for-extract-agentic-plus",
    "claude-cost-gcp": "https://claude.com/resources/articles/how-to-manage-costs-and-demonstrate-roi-for-claude-code-on-google-cloud",
    "anthropic-s1": "https://www.anthropic.com/news/s1-sec",
    "anthropic-pbf": "https://www.anthropic.com/news/public-benefit-fund",
    "anthropic-gsa": "https://www.anthropic.com/news/expanding-partnership-gsa",
    "anthropic-drug": "https://www.anthropic.com/research/early-progress-drug-development",
    "simon-vibegame": "https://simonwillison.net/2026/Oct/28/vibe-game-development/",
    "nvidia-nemoclaw": "https://developer.nvidia.com/blog/build-specialized-agents-on-a-stack-you-control-with-nvidia-nemoclaw/",
    "granite-switch": "https://huggingface.co/blog/ibm-granite/granite-switch-4-1-1",
    "meta-privacylib": "https://engineering.fb.com/2026/10/27/security/privacylib/",
    "vercel-agentenv": "https://vercel.com/changelog/run-scale-ais-agentenv-evals-on-vercel-sandbox",
    "arxiv-skillinf": "https://arxiv.org/abs/2610.35434",
    "arxiv-dynaflow": "https://arxiv.org/abs/2610.34467",
    "arxiv-cle": "https://arxiv.org/abs/2610.33956",
}
RELEASES = {
    "cc-2.1.314": ("anthropics/claude-code", "v2.1.314"), "cc-2.1.312": ("anthropics/claude-code", "v2.1.312"),
    "cc-2.1.311": ("anthropics/claude-code", "v2.1.311"), "bt-3.42.0": ("braintrustdata/braintrust-sdk", "braintrust@3.42.0"),
    "bt-3.41.0": ("braintrustdata/braintrust-sdk", "braintrust@3.41.0"), "lf-4.72.0": ("langfuse/langfuse", "v4.72.0"),
    "lf-4.71.0": ("langfuse/langfuse", "v4.71.0"), "lg-1.2.17": ("langchain-ai/langgraph", "1.2.17"),
    "lg-1.2.18": ("langchain-ai/langgraph", "1.2.18"), "lg-ckpt-4.3.1": ("langchain-ai/langgraph", "checkpoint==4.3.1"),
    "da-code-0.2.2": ("langchain-ai/deepagents", "deepagents-code==0.2.2"), "cfa-0.32.0": ("cloudflare/agents", "agents@0.32.0"),
    "cfa-0.31.0": ("cloudflare/agents", "agents@0.31.0"), "codex-0.166.0": ("openai/codex", "rust-v0.166.0"),
    "crewai-1.15.33": ("crewAIInc/crewAI", "1.15.33"), "lc-core-1.7.2": ("langchain-ai/langchain", "langchain-core==1.7.2"),
    "gemini-cli-0.66.0": ("google-gemini/gemini-cli", "v0.66.0"), "agentcore-1.25.1": ("aws/bedrock-agentcore-sdk-python", "v1.25.1"),
}


def page(item):
    key, url = item
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ai-field-brief"})
        raw = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
        (OUT / f"{key}.raw").write_text(raw, encoding="utf-8")
        art = re.sub(r"(?is)<(script|style|svg)\b[^>]*>.*?</\1>", " ", raw)
        txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", art)))
        (OUT / f"{key}.txt").write_text(txt, encoding="utf-8")
        dates = sorted(set(re.findall(r'(?:datePublished|dateModified|published_time|modified_time)"?\s*(?::|content=)\s*"([^"]{10,25})', raw)))[:4]
        return f"{key:20s} ok   {len(txt):7d} {dates}"
    except Exception as e:  # noqa: BLE001
        return f"{key:20s} FAIL {e}"


def rel(item):
    key, (repo, tag) = item
    r = subprocess.run(["gh", "api", f"repos/{repo}/releases/tags/{tag}"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", shell=True)
    if r.returncode:
        return f"{key:20s} FAIL gh"
    j = json.loads(r.stdout)
    (OUT / f"{key}.txt").write_text(j.get("body") or "", encoding="utf-8")
    return f"{key:20s} ok   published_at={j['published_at']} {j['html_url']}"


keys = set(sys.argv[1:])
with ThreadPoolExecutor(8) as ex:
    for line in ex.map(page, [(k, v) for k, v in PAGES.items() if not keys or k in keys]):
        print(line)
    for line in ex.map(rel, [(k, v) for k, v in RELEASES.items() if not keys or k in keys]):
        print(line)
