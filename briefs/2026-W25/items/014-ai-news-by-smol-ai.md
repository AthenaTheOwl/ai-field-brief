# GLM 5.2: the top Frontend Coding model in the world, IndexShare reduces costs

- lane: fast-signal
- source: [AI News by Smol AI](https://news.smol.ai/issues/26-06-16-glm-52)
- published: 2026-06-16
- confidence: high
- action_surface: runtime-adapter

**Gist:** Day-of writeup of GLM-5.2 release with ecosystem deployment map and benchmark detail.

**Mechanism:** 744B MoE / 40B active per token with IndexShare sparse-attention (reuses top-k indices across layer groups) cuts long-context inference cost ~2.9x at 1M tokens; day-zero support in vLLM, SGLang, Ollama, OpenRouter, Cloudflare Workers AI, Baseten; Terminal-Bench 2.1 score 81.0 first open model over 80.

**Why matters:** IndexShare is the specific architectural lever making 1M-context inference economical on open weights; ecosystem day-zero coverage means deployment without waiting for adapter PRs.

**Try:** Stand up GLM-5.2 on vLLM or SGLang at 200k+ context, measure prefill/decode TPS against your current sparse-attention baseline, and log the actual cost-per-task delta.

**Related thread:** open-weights catch-up
