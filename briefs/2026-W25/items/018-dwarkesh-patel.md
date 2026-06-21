# The data black hole at the center of AI

- lane: fast-signal
- source: [Dwarkesh Patel](https://www.dwarkesh.com/p/the-sample-efficiency-black-hole)
- published: 2026-06-19
- confidence: high
- action_surface: watchlist

**Gist:** Solo essay arguing AI progress is still mostly more data, not better sample efficiency: humans see ~200M tokens to adulthood, frontier models train on 10s-100s of trillions.

**Mechanism:** Patel frames the ~1M-fold token gap as evidence that current scaling can't close the sample-efficiency gap, implying humans operate on different learning principles than transformer-style induction.

**Why matters:** The capability-pessimism case from inside the AI-bull tent; sets the framing for the upcoming GPT-5.6 launch and is the contrarian backdrop for the open-weights rally.

**Try:** Pick one of your evals where you suspect the model is interpolating from training data and design a held-out variant the training set could not have memorized; see if the score collapses.

**Related thread:** capability ceiling debate
