<!--
meta:
  iso_week: <YYYY-WNN>
  through_date: <YYYY-MM-DD>            # last date of the brief window
  profile_id: <profile-id>              # from config/profiles.yaml (e.g. personal, broad_builder)
  matrix_run_id: <run-id>               # from ops/run-records/, optional
  sources_swept_count: <int>            # optional
  cells_verified_count: <int>           # optional
  volume: <NNN>
-->

# <title — what the week was about, not what shipped>

**week of <YYYY-MM-DD> · audience: <one line> · vol. <NNN>**

## Field thesis

<One paragraph — the deepest pattern across the week. Not a TL;DR; a
viewpoint. Names the frame that threads the picks together. The kind
of opening you'd find in Farnam Street's *Brain Food*, Stratechery's
day-after note, or a considered weekly letter.>

## Top signals

### 1. <name the thing, not the headline>

**Source:** [<source name>](<url>)
**Payload:** <one-sentence summary of what the source says>
**Mechanism:** <what changed, or what pattern is exposed — the
concrete behavior or structural shift, not the narrative>
**Why it matters:** <why this is useful to a reader in this profile>
**Reusable pattern:** <what transfers beyond this source>
**Action surface:** <one or two of: prompt, config, eval, workflow,
agent-role, tool-policy, runtime-adapter, source-registry,
architecture, experiment, watchlist, creative-os,
software-control-plane, personal-knowledge-base>
**Try:** <small testable action the reader runs before next Friday>
**Systems map:** <1-2 sentences naming the underlying mechanism>
**Transferable principle:** <1 sentence + 1 example of where else it applies>
**Falsification test:** <what observation would prove this wrong>
**Adoption ladder:**
  - Minimum viable: <smallest useful step>
  - Mid: <incremental expansion>
  - Full: <complete enrollment>
  - Monitoring: <signals to watch at each step>
**Confidence:** <high / medium / low>
**Evidence:** <cell_id_1>, <cell_id_2>, ...

### 2. <pick 2>

<same shape — vary the cadence; one pick can be tighter, one can be
longer comment.>

**Source:** [<source>](<url>)
**Payload:** <...>
**Mechanism:** <...>
**Why it matters:** <...>
**Reusable pattern:** <...>
**Action surface:** <label>
**Try:** <...>
**Systems map:** <1-2 sentences naming the underlying mechanism>
**Transferable principle:** <1 sentence + 1 example of where else it applies>
**Falsification test:** <what observation would prove this wrong>
**Adoption ladder:**
  - Minimum viable: <smallest useful step>
  - Mid: <incremental expansion>
  - Full: <complete enrollment>
  - Monitoring: <signals to watch at each step>
**Confidence:** <high / medium / low>
**Evidence:** <cell_ids>

### 3. <pick 3>

<same shape>

**Source:** [<source>](<url>)
**Payload:** <...>
**Mechanism:** <...>
**Why it matters:** <...>
**Reusable pattern:** <...>
**Action surface:** <label>
**Try:** <...>
**Systems map:** <1-2 sentences naming the underlying mechanism>
**Transferable principle:** <1 sentence + 1 example of where else it applies>
**Falsification test:** <what observation would prove this wrong>
**Adoption ladder:**
  - Minimum viable: <smallest useful step>
  - Mid: <incremental expansion>
  - Full: <complete enrollment>
  - Monitoring: <signals to watch at each step>
**Confidence:** <high / medium / low>
**Evidence:** <cell_ids>

## Reusable patterns

- **<pattern one>.** Where it applies: <one line>. Caveats: <one line>.
- **<pattern two>.** Where it applies: <one line>. Caveats: <one line>.
- **<pattern three>.** Where it applies: <one line>. Caveats: <one line>.

## Action queue

| Candidate | Surface | Effort | Risk | Test |
|---|---|---|---|---|
| <action one> | <surface> | <S/M/L> | <low/med/high> | <one-line test plan> |
| <action two> | <surface> | <S/M/L> | <low/med/high> | <one-line test plan> |
| <action three> | <surface> | <S/M/L> | <low/med/high> | <one-line test plan> |

## Watchlist

- **<question one>.** Revisit trigger: <named event or date that
  promotes this off the watchlist>.
- **<question two>.** Revisit trigger: <...>.
- **<question three>.** Revisit trigger: <...>.

## Archive notes

High-quality items the sweep surfaced but that did not earn a pick this
week. Kept searchable, not surfaced — recorded so the corpus stays
honest about what the week contained.

- **<author>, "<title>"** ([<source>](<url>)). <one-line note on why
  the item lands in archive instead of a Top signal>.
- **<author>, "<title>"** ([<source>](<url>)). <one-line note>.

## Sources reviewed

| Source | Status | Note |
|---|---|---|
| <source id> | ok | items captured / items included |
| <source id> | failed | <error from sweep> |
| <source id> | skipped | <reason> |

## Closing thought

<One sentence or short paragraph. A frame, a question, or a quote from
a primary source. Not a summary.>

---

<!-- voice notes for the author / agent:
  - no banned phrases (see scripts/voice_lint.py BANNED_FAIL)
  - no antithetical reversals (the "X isnt Y, Z is the W" cadence) voice_lint:allow antithetical-dash
  - no empty adverbial openers (Importantly, Notably, etc.)
  - every claim links to a primary source where possible
  - the brief is published; it reads in 5-10 minutes

  evidence-spine rules (see AGENTS.md):
  - every Top signal carries an Evidence: line listing one or more
    verified matrix cell ids
  - every Top signal carries a Confidence: label (high / medium / low)
  - every Top signal carries all four systems-thinking fields
    (Systems map, Transferable principle, Falsification test,
    Adoption ladder) per DEC-MTRX-007 and DEC-CDCP-020; a pick
    missing any of the four belongs in Archive notes, not Top signals
  - every watchlist item carries a Revisit trigger
  - every action queue row carries a Test column
  - no forced action angle: if a source has nothing actionable, it
    belongs in Archive notes, not Top signals

  action surface labels (from config/action_surface_taxonomy.yaml):
    prompt
    config
    eval
    workflow
    agent-role
    tool-policy
    runtime-adapter
    source-registry
    architecture
    experiment
    watchlist
    creative-os
    software-control-plane
    personal-knowledge-base
-->
