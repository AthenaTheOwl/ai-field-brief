# candidate sources

Sources surfaced during curation passes but not yet promoted into
`registry.yaml`. Each entry names a verifiable tie to Anthropic / OpenAI
/ a tier-1 super-user; promote with `status: active` once a manual review
pass confirms cadence + intake + signal.

The file is read by humans, not by the run workflow.

## How an entry earns promotion

1. Verifiable tie to a primary surface (lab employee blog, lab-cited
   reference, published endorsement by a recognized operator).
2. Posts at least monthly OR breaks news the existing registry would
   miss.
3. Has a stable URL or RSS that the connector can ingest.

## Awaiting review

### Karpathy / X public reading habits

- **Andrej Karpathy on X** (`x.com/karpathy`). No RSS. Subscribes
  publicly to [Simon Willison's blog](https://simonwillison.net) and
  has called out [karpathy.ai](https://karpathy.ai) personal notes
  (`Software 3.0` era posts). Intake: `human-notes` — clip-worthy
  threads only via the browser extension when the spec 0002 webhook
  source lands.

### Anthropic employees with public sites

- **Chris Olah** — interpretability lead; co-author of the Anthropic
  circuits work. Personal site at https://colah.github.io is sparse
  but each post matters.
- **Jack Clark** — Anthropic policy / co-founder. Weekly newsletter
  *Import AI* at https://importai.substack.com — high-signal weekly
  AI digest written by an Anthropic founder.
- **Catherine Olsson, Tom Brown, Jared Kaplan, Sam McCandlish** —
  occasional posts on Anthropic's research index, already covered by
  `anthropic-research`.

### OpenAI employees with public sites

- **Andrej Karpathy** (ex-OpenAI, ex-Tesla). See above.
- **Lilian Weng** — ex-OpenAI Head of Safety Systems; blog at
  https://lilianweng.github.io covers RLHF, agent design, safety with
  citation-grade rigor.
- **Greg Brockman / Sam Altman** — X-only. Press-tour-heavy; lower
  signal than the lab's official news feed.

### Applied LLMs co-authors not yet in registry

- **Bryan Bischof** — https://www.bryanwbischof.com. Co-author of the
  Applied LLMs report.
- **Charles Frye** — https://charlesfrye.github.io. Co-author.
  Strong on infra + GPU.
- **Jason Liu** — https://jxnl.co. Author of the `instructor` library;
  Structured Outputs in Python.
- **Shreya Shankar** — https://www.shreya-shankar.com. Co-author;
  evals + data systems.

### Latent-Space-adjacent

- **Vanishing Gradients** (Hugo Bowne-Anderson) — the podcast where
  the Applied LLMs authors discussed the 42 lessons. RSS via the
  Fireside link.
- **AI Engineer Summit talks** — published on the Latent Space YouTube
  channel; covered already through `latent-space` but worth a separate
  entry for the talk archive.

### Strategy-tier candidates

- **Stratechery (Ben Thompson)** — paid newsletter; the canonical
  business-of-AI analyst. Behind a paywall — `intake: human-notes`
  only.
- **Astral Codex Ten (Scott Alexander)** — irregular AI takes; high
  rigor when posted. https://www.astralcodexten.com.
- **Tom Tunguz** — VC analysis of the AI market.

### Research-tier candidates

- **AI Alignment Forum** — https://www.alignmentforum.org. Anthropic
  alignment researchers cross-post here. `intake: full` once a
  bandwidth limit is in place; high volume.
- **arXiv `cs.AI`, `cs.CL`, `cs.LG`** — already covered as a planned
  source type (`arxiv-feed`); add specific categories under
  `registry.yaml` when the connector lands.
- **Hugging Face Daily Papers** — https://huggingface.co/papers.
  Already planned as `hf-papers` source type.

### Agent benchmark watch

- **SWE-bench+** — extension of SWE-bench-style coding tasks with
  broader verified repair surfaces. Candidate use: harden the factory's
  brownfield gates and held-out-test policy.
- **SpecBench** — benchmark focused on specification-following and
  implementation against written contracts. Candidate use: calibrate
  `expected_artifacts`, `module_map`, and first-action gates.
- **ImpossibleBench** — adversarial task family for exposing shortcut
  behavior and overfitting to visible tests. Candidate use: decide when
  a task needs `held_out_tests` as a permission boundary.
- **Vendor eval postmortems** — especially OpenAI's SWE-bench Verified
  evaluation notes. Candidate use: prevent public portfolio claims from
  overstating what a benchmark score means.

Promotion rule: these enter `registry.yaml` only when the weekly issue
needs an evaluation-method source, not as general news feeds.

### Vendor-watch breadth

- **Google DeepMind blog** — https://deepmind.google/discover/blog.
  Frontier-lab parity coverage.
- **Meta AI blog** — https://ai.meta.com/blog. Llama + open-model
  releases.
- **Mistral, Cohere, AI21, Reka** — secondary vendor changelogs;
  consolidate as a single `vendor-changelog` lane entry per company
  when the connector lands.
- **Hugging Face Blog** — https://huggingface.co/blog.

### Other LinkedIn / Substack candidates surfaced during 2026-05-22 sweep

- **The AI Corner (Ruben Dominguez)** — promoted to registry as
  `the-ai-corner`. Heavy on Anthropic / Claude product coverage;
  hype-penalty kept higher than the other strategy entries.

## Provenance log

Each promotion to `registry.yaml` should record the evidence here.

| Date       | Action                           | Source                  | Evidence                                                                                       |
|------------|----------------------------------|-------------------------|------------------------------------------------------------------------------------------------|
| 2026-05-22 | initial seed                     | (all 15 registry entries) | curated sweep with web-search tier-1 endorsements per entry                                  |
| 2026-05-22 | candidate (link from LinkedIn)   | the-ai-corner           | user-shared LinkedIn shortlink; resolved to https://www.the-ai-corner.com/t/claude-and-anthropic |
| 2026-05-22 | candidate                        | jack-clark / import-ai  | Anthropic co-founder authors weekly digest; high prior to promote                              |
| 2026-05-22 | candidate                        | lilian-weng             | ex-OpenAI Head of Safety; citation-grade RLHF + agent notes                                    |
