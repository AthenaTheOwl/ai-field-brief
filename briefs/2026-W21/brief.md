# Contract speed, not model speed

**week of 2026-05-18 · audience: builder-tpms thinking about AI · vol. 001**

This week's quiet pattern is that AI is finishing its handshake with
institutions that move slowly. KPMG signed a multi-year deployment. PwC
deepened its partnership. The Gates Foundation committed $200M over
several years. Each headline arrives with the unglamorous shape of
contracts, integration work, and internal training programs for
workforces measured in the hundreds of thousands.

The model-of-the-week ritual rolled on at Google, where Gemini 3.5
Flash landed directly in Gmail and Calendar on day one of general
availability. Anthropic, meanwhile, acquired the company whose tooling
already powers its own SDK. Most of it lives off the launch stage.
All of it changes the shape of the year.

## This week

### Anthropic acquires Stainless

Stainless makes the tooling that generates client SDKs from OpenAPI
specs. The Anthropic SDKs in Python and TypeScript already build on it;
this acquisition turns that dependency from incidental into load-bearing.
Slow read: Anthropic is buying its way into owning the developer stack
a floor at a time — SDK generation now, who knows what next. A small
footnote — Stainless's customer list includes OpenAI. That arrangement
presumably continues, and whether public confirmation arrives either
way is its own signal.

[anthropic.com/news/anthropic-acquires-stainless](https://www.anthropic.com/news/anthropic-acquires-stainless)

### KPMG, PwC, and the Gates Foundation in five days

Three deployment announcements between May 14 and May 19. Gates is
$200M over multiple years, focused on global health. PwC calls its
rollout a "core function" deployment. KPMG names 276,000 seats.
Contract scale, not pilot scale. The interesting question, for anyone
who works around large firms — how does a 276k-seat Claude rollout
change a firm's incident-response, audit, knowledge-management, and
training stacks? Not eighteen months from now. This year.

[anthropic-kpmg](https://www.anthropic.com/news/anthropic-kpmg) · [gates-foundation-partnership](https://www.anthropic.com/news/gates-foundation-partnership) · [pwc-expanded-partnership](https://www.anthropic.com/news/pwc-expanded-partnership)

### Project Glasswing initial update

Anthropic published an update on a collaborative effort to secure
critical software infrastructure across major technology and financial
firms. The framing reads like a vendor-level security program, more
than a product feature. AI vendors are starting to inhabit the role
cloud vendors filled around 2014 — the security and compliance posture
becomes the product, in the customer's eyes, before any single feature
does.

[research/glasswing-initial-update](https://www.anthropic.com/research/glasswing-initial-update)

### Gemini 3.5 Flash, day-zero GA across Workspace

Google launched Gemini 3.5 Flash straight to general availability and
embedded it across Gmail, Calendar, and other Workspace surfaces. The
new Flash costs more than the prior Flash, and Google made it the
default model end users get without a paid plan. The slower-to-cheap
pattern matters more than the model card; cost ceilings are where most
customer math eventually breaks.

[simonwillison.net coverage](https://simonwillison.net/2026/May/19/gemini-35-flash/)

### Simon Willison's "Last Six Months in LLMs in Five Minutes"

Annotated slides from a PyCon US lightning talk covering what changed
between November and May. A five-minute reorientation if you've fallen
off the standard names. The blog earns a long subscription — Andrej
Karpathy [publicly subscribes via NetNewsWire](https://x.com/karpathy/status/1933582359347278246)
and reads "everything," which is unusual praise from him.

[5-minute-llms](https://simonwillison.net/2026/May/19/5-minute-llms/)

## Worth your time

**Eugene Yan, "How to Work and Compound with AI"** (May 3). Four
frames: context infrastructure, taste configuration, verification,
delegation. The piece doesn't promise speed; it argues that work done
with sufficient context leaves behind structure the next attempt can
reuse, and that the leftover structure is where compounding lives.
Eugene now works at Anthropic, so the post doubles as a window
into how an Anthropic MTS thinks about practitioner workflow.
[eugeneyan.com/writing/working-with-ai](https://eugeneyan.com/writing/working-with-ai/)

**Simon Willison, "Datasette Agent"** (May 21). Three years of work on
the `llm` library finally merged with Datasette. The artifact is
smaller than the time horizon — Simon's personal infra has compounded
for 23 years, which Karpathy also flagged this week. Few readers can
reproduce the path. The discipline behind it is the part that travels.
[simonwillison.net/2026/May/21/datasette-agent](https://simonwillison.net/2026/May/21/datasette-agent/)

**Hamel Husain, "Evals Skills for Coding Agents"** (March 2). Pulled
back into focus by the Stainless news — if Anthropic plans to own
more of the developer stack, the eval gap on coding agents is where
the next year of practitioner work lives. Hamel co-teaches AI evals to
engineers at OpenAI, Anthropic, and Google; the methodology in this
post is the closest thing to a shared baseline.
[hamel.dev/blog/posts/evals-skills](https://hamel.dev/blog/posts/evals-skills/index.html)

## Watchlist

- **What a 276k-seat Claude rollout changes inside KPMG.** If you have
  colleagues there, ask six months out about audit, review, and
  training updates. The answer travels.
- **Whether the OpenAI–Stainless contract continues.** Public
  confirmation either way is a real read on how Anthropic plans to
  hold the developer-stack acquisitions.
- **The Gemini 3.5 Flash pricing curve.** Last year's "Flash means
  cheap" assumption may be on hold; the new Flash costs more than its
  predecessor. Watch the next price update.

## Closing thought

The week's frontier moved at contract speed, not at model speed. The
next round of enterprise rollouts may tell us more about 2026 than the
next model card does.
