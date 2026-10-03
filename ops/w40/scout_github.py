"""W40 framework-runtime scout via the GitHub API: releases and changelog commits dated inside the window.
Output: ops/w40/scout.tsv. Everything here is dated by GitHub, not inferred."""
import json, subprocess
from pathlib import Path
SINCE, UNTIL = "2026-09-26T00:00:00Z", "2026-10-03T00:00:00Z"
REPOS = ["anthropics/claude-code", "modelcontextprotocol/modelcontextprotocol", "modelcontextprotocol/python-sdk",
         "modelcontextprotocol/typescript-sdk", "langchain-ai/langchain", "langchain-ai/langgraph", "langchain-ai/deepagents",
         "openai/openai-agents-python", "openai/codex", "crewAIInc/crewAI", "strands-agents/sdk-python", "vercel/ai",
         "google/adk-python", "microsoft/autogen", "microsoft/agent-framework", "pydantic/pydantic-ai", "BerriAI/litellm",
         "run-llama/llama_index", "anthropics/anthropic-sdk-python", "google-gemini/gemini-cli", "brexhq/CrabTrap",
         "aws/bedrock-agentcore-sdk-python", "browser-use/browser-use", "huggingface/smolagents"]
def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
rows = []
for repo in REPOS:
    rel = gh(f"repos/{repo}/releases?per_page=30") or []
    for x in rel:
        d = x.get("published_at") or ""
        if SINCE <= d < UNTIL:
            body = (x.get("body") or "").replace("\r", " ").replace("\n", " ")[:300]
            rows.append((repo, "release", d[:10], x.get("tag_name", ""), x.get("html_url", ""), body))
    # changelog commits for repos that keep one
    for fname in ("CHANGELOG.md",):
        commits = gh(f"repos/{repo}/commits?path={fname}&since={SINCE}&until={UNTIL}&per_page=30") or []
        for c in commits:
            rows.append((repo, "changelog-commit", c["commit"]["author"]["date"][:10], c["sha"][:7], c["html_url"],
                         c["commit"]["message"].splitlines()[0][:120]))
out = Path(__file__).with_name("scout.tsv")
out.write_text("repo\tkind\tdate\ttag_or_sha\turl\tsummary\n" + "\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")
by = {}
for r in rows:
    by[r[0]] = by.get(r[0], 0) + 1
print("in-window rows:", len(rows), by)
