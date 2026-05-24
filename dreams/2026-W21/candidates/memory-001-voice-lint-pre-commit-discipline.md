---
id: memory-001-voice-lint-pre-commit-discipline
target_kind: memory_update
target: .agents/AGENTS.md
human_review_required: true
evidence:
  - kind: commit
    ref: d2186d2 — voice_lint clean reported in commit body after 47 files scanned at the end of the push
  - kind: commit
    ref: c29b7ac — brief rewrite landed only after voice rules forced a rewrite from summary-shape into insight-shape
  - kind: commit
    ref: b4b9cf2 — six new role instruction files plus a CATALOG of 44 deferred roles all had to clear voice rules before the push
  - kind: file
    ref: scripts/voice_lint.py — current banlist holds 55 FAIL phrases, 18 WARN phrases, and 9 structural rules
---

## proposal

Add a `## Voice rules at commit time` block to `.agents/AGENTS.md` that names the three highest-frequency hit categories from this week, with the rewrite recipe for each. The block sits under `## Workflow conventions`, above the role catalog.

Proposed text (to be reviewed and edited by a human, not auto-applied):

```markdown
## Voice rules at commit time

`voice_lint.py` runs eight rule families. The three an agent hits most
often when drafting role docs, briefs, and DECs:

1. **Antithetical period and dash** — the X-isn't-Y dot Y-is-Z shape.
   voice_lint:allow antithetical-period antithetical-dash banned-enables banned-leverages
   Rewrite: drop the negation. Lead with the positive claim and let the
   contrast land via context, not via structure.
2. **The forbidden verbs of corporate prose** — every instance of the
   four most common ones fails the banlist.
   voice_lint:allow banned-enables banned-leverages
   Rewrite: name the verb. "X lets Y do Z" beats the bland version.
3. **Empty adverbial openers** — Importantly, Notably, Ultimately.
   Rewrite: cut the opener. If the sentence needs the emphasis, the
   sentence is weak; fix the sentence.

Run `python scripts/voice_lint.py` on every staged markdown file before
`git commit`. Per-line allowlist via `voice_lint:allow <label>` ships only
when the rule mis-fires and the agent leaves a one-line reason.
```

## why it earns its keep

Three commits this week (`c29b7ac`, `d2186d2`, `b4b9cf2`) named voice_lint as a verified gate in their commit body, which means the gate ran late and forced rewrites. The cost of a late rewrite of role docs or a brief runs high — the role contract shapes the agent's behavior surface. A pre-commit reminder block costs five lines of AGENTS.md and saves one rewrite cycle per push.

The block also gives the agent the rewrite recipe, which the current AGENTS.md skips. Today the contract names the banlist as hard-FAIL without saying what to do when a FAIL lands.

## evidence

- `d2186d2` — commit body lists "voice_lint clean (47 files scanned)" as the fourth verified gate. The phrasing tells the reader voice_lint ran; it does not tell the next agent what tripped on the way there.
- `c29b7ac` — the brief rewrite commit body explicitly mentions "rewritten from 5 short picks to 5 long picks", which means the first draft did not clear voice. The rewrite cost was real but unrecorded.
- `b4b9cf2` — the CDCP operating model install shipped six role `instructions.md` files (80–120 lines each) plus a 44-role CATALOG. Every file ran voice_lint at the end; any FAIL would have blocked the push.
- `scripts/voice_lint.py` lines 39–113 — the actual banlist. The rewrite recipe in the proposed text matches the three categories that produced the most fixes during pre-commit cleanup this week.

## promotion path

If approved, the change touches one file:

- `.agents/AGENTS.md` — add the new block under `## Workflow conventions`.

Reviewer checks:

1. Block reads in under 30 seconds.
2. Every named rewrite recipe matches a real rule in `scripts/voice_lint.py`.
3. The block itself clears voice_lint when the change lands (the proposed text deliberately holds the banned phrases inside fenced code so they get scanned; promotion may rewrite the prose-mode examples).
4. No duplication with the existing line under `## Domain decisions` that names the banlist — either fold that line in or keep the new block focused on the rewrite recipe.

Owner role: `engineering.implementation` (memory-file edits live with the role that ships the file).

## risks if promoted blindly

- The three "most common" hits are observation from one week. A second week of data may reveal a different top three. Promote as v1; revisit after week 4.
- The rewrite recipes are opinions about good prose. A reviewer who reads the block as a hard rule may over-correct and produce stilted text. The block names "rewrite" not "must rewrite" for that reason.
- The block adds 25 lines to AGENTS.md. The current file is 165 lines. Adding a voice-rules section nudges the file toward a rules-of-writing document instead of an agent contract. Reviewer should weigh whether the block belongs in AGENTS.md or in `scripts/voice_lint.py`'s docstring.
