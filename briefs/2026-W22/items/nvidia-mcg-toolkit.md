# nvidia-mcg-toolkit

- **Source:** NVIDIA Developer Blog
- **URL:** https://developer.nvidia.com/blog/how-to-automate-ai-model-documentation-with-the-nvidia-mcg-toolkit/
- **Captured:** 2026-05-29
- **Priority:** medium
- **Cells:** MTRX-W22-nvmcg-source_gist, MTRX-W22-nvmcg-adoption_action

## What

NVIDIA shipped an MCG (Model Card Generator) toolkit on May 29 to
automate AI model documentation in response to California's AB-2013
and the EU AI Act.

## Why it matters

AB-2013 compliance deadlines fall inside Q3 for California-deployed
systems. Teams fine-tuning or deploying open-weight models need a
release-step that produces a model card; backfilling cards under
regulatory pressure is more costly than automating them once.

## Action surface

config, workflow

## Concrete move

Add a model-card generation step to the release workflow for any
team shipping a fine-tuned or open-weight model into a California-
served product. The MCG toolkit is one credible implementation;
the principle (automated cards as a release artifact) is the
durable move.

## Caveats

A vendor-published toolkit is one path; HuggingFace's model-card
generator, EleutherAI's lm-eval-harness card profile, and bespoke
templates are equivalent. Read the NVIDIA post for the regulatory
calendar, not for tooling lock-in.
