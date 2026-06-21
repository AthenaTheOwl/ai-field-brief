# Is AI immune to groupthink?

- lane: strategy
- source: [Exponential View](https://www.exponentialview.co/p/is-ai-immune-to-groupthink)
- published: 2026-06-17
- confidence: high
- action_surface: eval

**Gist:** Rohit Krishnan guest post running a 16-prompt experiment on multi-model 'councils' and finding councils preserve only ~25% of valuable single-model ideas, with peer-review councils giving only 11% uplift for consensus ideas over unique ones.

**Mechanism:** Empirical test of three council structures (blending, peer-review, direct selection) on 8 strategy + 8 writing prompts; atomic 'idea cards' blind-rated by judges; councils systematically lose minority good ideas rather than aggregating the best from each model.

**Why matters:** If you're building multi-agent or multi-model judging stacks, the default 'just have models vote' design throws away the long tail where the value sits — you have to evaluate per problem, not assume an ensemble win.

**Try:** On your existing multi-model setup, run the experiment shape: take 16 of your real prompts, capture each single-model answer, then capture the council answer, blind-rate atomic ideas, and measure what fraction of unique good ideas survive. Kill the council if it's below ~50%.

**Related thread:** eval discipline shift
