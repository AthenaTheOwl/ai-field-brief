# VOICE — ai-field-brief

The brief's editorial voice.

If you're an AI agent (Claude, Codex) writing or rewriting copy for the
public-facing briefs, this file is binding. The voice spec lives here
because the prior pattern — leave the voice in the prompt — let it drift.

---

## the voice in one line

**Quirky and deadpan. Builder talking to another builder over coffee.
Concrete nouns. No filler. The joke (when there is one) is dry and
short.**

Think: the writer found the thing funny enough to keep working on it,
not funny enough to make a thing of.

---

## the three rules (binding)

### rule 1 — no AI cadences

Banned structural devices:

- **antithetical reversals.** "X isn't Y — Z is the W." "The point is
  not X, it is Y." "Not the model, the contract." Stacked, these become
  the AI tell.
- **gnomic-metaphor openings.** "the audience sorts into shapes you can
  name", "the binding work has migrated out of the model and into the
  operating boundary around the model", "the load-bearing question for
  builders this week".  These feel important. They say nothing.
- **canned framings that repeat across briefs.** "if you only have time
  for one move from this brief", "the most useful sentence to write
  down this week", "the load-bearing news arrived in the unglamorous
  shape of". Ritual is not advice.
- **"X is Y; Z is the W" aphorism closers.** "The flinch is the work —
  the sentence is the artifact." Both halves can be true and neither
  helps the reader.

If a sentence sounds like it could appear on a slide for a TED talk,
delete it.

### rule 2 — no filler

A sentence earns its place by either landing a fact or making a small
joke. If it does neither, cut it.

Specific filler patterns to delete:

- "this week's quiet pattern is" — say what happened
- "what's interesting here is" — show, don't announce
- "it's worth noting that" — if you noted it, it's noted
- adjective ladders ("a thoughtful, considered, carefully-built
  approach")
- the entire "Closing thought" reflex when you don't have one. Close on
  the last concrete move. Silence is honest.

### rule 3 — quirky + deadpan

Concrete > abstract. Specific > general. Short > long.

Allowed and encouraged:
- bone-dry asides that name a real thing the reader recognized but
  hasn't seen written down. *"Cursor productized the policy ladder. You
  shipped a Notion doc."*
- numbers said as numbers. *"$200M over four years"*, not *"a
  significant commitment"*.
- proper nouns instead of categories. *"the foundation underwriting
  global health work"* → *"Gates"* (after first mention).
- light incongruity. *"Stainless got acquired. The retry policy is now
  Anthropic's roommate."*
- one short joke per surface, max. Two is a routine.

Not allowed:
- self-aware joke construction ("you might say...", "as it were", "to
  put it mildly", "let me tell you")
- exclamation marks
- emoji
- starting a section with a rhetorical question
- closing a section with "the rest is up to you" energy

---

## anchoring before/after pairs

The point of this section is not breadth — it's calibrating the ear.
Five pairs, one per pattern. Each one is from a real brief; the rewrite
is what should have shipped.

### pair 1 — gnomic opener → concrete fact

**before** (W20, line 10):
> This week the AI customer base started sorting into shapes you can
> name. Anthropic shipped Claude for Small Business on Tuesday, signed
> PwC and the Gates Foundation on Thursday, and last week's SpaceX
> compute deal kept echoing through rate-limit conversations.

**after**:
> Anthropic sold the same model to four different buyers this week:
> small businesses on Tuesday, PwC and Gates on Thursday, and the
> rate-limit conversations from last week's SpaceX deal are still going.
> Four products in five days. Pick the one your feature is for.

Lead with the concrete count. Replace "sorting into shapes" with the
shape itself.

### pair 2 — canned framing → direct ask

**before** (W21, line 19):
> If you only have time for one move from this brief: rerun your last
> quarter's LLM cost line under the new Flash pricing before someone
> else does it for you. Worked numbers below.

**after**:
> Rerun last quarter's LLM cost line under the new Flash pricing.
> Worked numbers below. Do it before your CFO does.

Drop the ritual opener. "Before someone else does it for you" becomes
the deadpan bite: name who that someone is.

### pair 3 — aphorism closer → silence

**before** (W20, line 538):
> ## Closing thought
> The most useful sentence to write down this week is the one that
> names the buyer your AI feature sells to. Most product pages flinch
> at writing it. The flinch is the work — the sentence is the artifact.

**after**:
> ## Closing thought
> Open your product page. Write the sentence the buyer would say to a
> peer to recommend it. If you can't write it, you don't have a
> product. You have a landing page.

Replace the "X is the Y" aphorism with a one-step action and a dry
diagnosis. "You don't have a product. You have a landing page." reads
deadpan because it's true.

### pair 4 — metaphor-stack → plain shape

**before** (W22, opening):
> the binding work has migrated out of the model and into the operating
> boundary around the model. The Series H tells one half of the story —
> a $965B private valuation against a $47B run-rate funded almost
> entirely by enterprise coding-agent token burn.

**after**:
> Anthropic raised at $965B against a $47B run rate. Almost all of that
> run rate is enterprise coding agents burning tokens. The interesting
> work this week wasn't model changes — it was policy files, budget
> caps, and tiered review ladders. The contract caught up to the
> capability.

Lead with the number. "Binding work has migrated out of the model and
into the operating boundary around the model" → "The contract caught up
to the capability." Six words instead of nineteen, and the metaphor
("caught up") earns its keep because it names the relationship.

### pair 5 — adjective ladder → one concrete noun

**before** (W21 closing):
> ## Closing thought
> Write down one decision you're delaying because you're not sure
> whether AI changes it. Date the entry. Revisit in 30 days. The entry
> is the artifact — the decision is downstream.

**after**:
> Pick one decision you're sitting on because you're not sure whether
> AI changes the answer. Write it down. Date it. Set a calendar reminder
> for 30 days from now. The reminder is the only honest part of this
> exercise.

"Set a calendar reminder for 30 days from now" is the concrete instead
of "Revisit in 30 days." "The reminder is the only honest part of this
exercise" is the deadpan bite — true, mildly funny, and earns the last
line.

---

## the practical procedure

When rewriting a section:

1. Read the section once. Note the underlying claim (one sentence).
2. Highlight every offender from rule 1 (no AI cadences).
3. Cut every offender from rule 2 (no filler).
4. Rewrite the section so it lands the underlying claim with as few
   sentences as the claim deserves, using rule 3 (quirky + deadpan)
   only when a real bit of dryness or incongruity is available.
5. If no real dryness is available, the rewrite is plain declarative
   prose. Plain beats forced.

When in doubt: shorter. When still in doubt: shorter.

---

## what NOT to optimize for

- comprehensiveness. The brief is a brief.
- "showing your work." Workings live in the items/ folder.
- formal register. The reader is a builder, not a board member.
- balance. If one source matters and three don't, write the one.
- consistency across briefs. Each brief stands on its own.

---

## audit

A weekly brief that ships under this voice should pass a 60-second
read-aloud check: read the field-thesis paragraph out loud. If you
catch yourself slowing down for "load-bearing" or "shape" or "the X
is the Y" cadence, the rewrite isn't done.

The voice_lint script (`scripts/voice_lint.py`) catches the structural
patterns. The funny is not lintable — that's on the writer.

---

## who maintains this

The repo owner edits this file when the voice drifts and they catch it.
AI agents working in this repo treat the file as binding spec, not as a
suggestion. When a workflow disagrees with VOICE.md, VOICE.md wins.
