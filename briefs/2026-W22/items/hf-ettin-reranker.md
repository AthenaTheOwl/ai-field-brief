# hf-ettin-reranker

- **Source:** Hugging Face Blog
- **URL:** https://huggingface.co/blog/ettin-reranker
- **Captured:** 2026-05-19
- **Priority:** medium
- **Cells:** MTRX-W22-ettin-source_gist, MTRX-W22-ettin-adoption_action, MTRX-W22-ettin-risk_and_caveats

## What

Hugging Face released the Ettin reranker family — six pointwise
cross-encoder rerankers from 17M to 1B parameters, distilled from
mxbai-rerank-large-v2. The 1B model matches the 1.54B teacher on
MTEB NDCG@10 (0.6114) while running 2.4x faster on H100 (928 vs
387 pairs/sec). The 17M model beats 33M ms-marco-MiniLM-L12-v2
by +0.051 NDCG@10 at half the parameters.

## Why it matters

For teams running retrieve-then-rerank pipelines on legacy MiniLM
rerankers, the upgrade is a config flip with measurable accuracy +
throughput gains. The 150M model is the new balanced default; the
17M and 32M models are the new CPU-bound recommendation.

## Action surface

config, eval

## Concrete move

Pilot ettin-reranker-150m as the new balanced default in a
retrieve-then-rerank pipeline. Run a domain-specific eval — the
MTEB numbers are broad-domain — and confirm the lift before
swapping the production model.

## Caveats

The MTEB numbers are broad-domain; legal, medical, and internal-
docs RAG need a fine-tune pass before any claimed gain holds. The
throughput figures assume bfloat16 + Flash Attention 2 + unpadded
inputs; default fp32 deployments will not see the headline number.
