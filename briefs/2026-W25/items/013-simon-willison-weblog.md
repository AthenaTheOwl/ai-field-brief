# GLM-5.2 is probably the most powerful text-only open weights LLM

- lane: fast-signal
- source: [Simon Willison weblog](https://simonwillison.net/2026/Jun/17/glm-52/)
- published: 2026-06-17
- confidence: high
- action_surface: tool-policy

**Gist:** Z.ai released GLM-5.2, a 753B-parameter MIT-licensed text-only model with 1M context that tops Artificial Analysis's Intelligence Index v4.1 for open weights at 51.

**Mechanism:** Open-weights model with 1M-token context ranks #1 on the open-weight intelligence index and #2 on Code Arena WebDev frontend leaderboard; tradeoff is significantly higher output token consumption than competitors.

**Why matters:** First MIT-licensed open model practitioners are using as a serious Opus/GPT-5.5 substitute for coding workloads, shifting OSS share on OpenRouter from 40% to 60% in three months.

**Try:** Pull GLM-5.2 via OpenRouter or Cloudflare Workers AI and route one real coding task through it; compare token cost and output quality against your current default.

**Related thread:** open-weights catch-up + Fable 5 fallout
