# memory-shortage

- **Source:** Simon Willison (HBM memory shortage)
- **URL:** https://simonwillison.net/2026/May/22/memory-shortage/
- **Captured:** 2026-05-22
- **Priority:** medium
- **Cells:** MTRX-W22-memory-shortage-source_gist, MTRX-W22-memory-shortage-mechanism_extraction, MTRX-W22-memory-shortage-adoption_action, MTRX-W22-memory-shortage-governance_surface, MTRX-W22-stratechery-nvidia-source_gist, MTRX-W22-stratechery-dc-veto-source_gist, MTRX-W22-zvi-ai-170-source_gist

## What

HBM allocation is moving from roughly 2% of wafer capacity at the
start of 2026 to an expected 20% by year-end. Each gigabyte of
HBM consumes roughly 3x the wafer area of standard DRAM, so the
allocation shift crowds out conventional DRAM and consumer RAM
prices are rising as a downstream effect. Stratechery the same
week covered NVIDIA's revised earnings reporting separating
hyperscaler GPU sales (under commoditization pressure) from
enterprise and other (where NVIDIA controls the stack). The
data-center-veto roundup landed the political-economy half: local
zoning, water, and power-permit processes are now the binding
constraint on AI-infra siting. Zvi's W22 read confirmed the
federal AI Executive Order was postponed indefinitely while
Illinois SB 315 advanced.

## Why it matters

Capex planning that assumes federal preemption of state AI rules,
or assumes HBM availability scales to demand, or assumes
hyperscaler GPU procurement remains the dominant margin pool, is
now planning against the wrong physical facts. The infra economic
frame this quarter shifts from "how many GPUs" to "tokens-per-watt
at which siting decision under which state auditing regime."
Hardware buyers should plan on 12-24 months of elevated DRAM
pricing.

## Action surface

architecture, watchlist, source-registry

## Concrete move

Add three rows to the AI infra dashboard: HBM allocation share by
quarter (track Samsung / SK Hynix / Micron capex notes), $/token
at current utilization, tokens/W on the dominant deployment tier.
If your buildout schedule has a 2026-H2 site selection, model
local-permitting risk as a top-3 schedule risk and consider
pre-permitted brownfield sites as a fallback. Treat Illinois
SB 315 as the concrete US compliance anchor and stop budgeting
around the postponed federal EO.

## Caveats

The 20%-by-end-2026 HBM allocation is a single-source forecast in
Willison's summary; verify against vendor capex disclosures.
Stratechery's commoditization framing on hyperscaler GPUs is the
author's interpretation of the reporting change. The
data-center-veto roundup names the shape but does not enumerate
incidents; verify against on-the-ground permit data before
propagating to capex planning.
