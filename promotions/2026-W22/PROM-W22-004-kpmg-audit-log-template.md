---
id: PROM-W22-004
brief: 2026-W22
pick_slug: kpmg-digital-gateway-consultancy-grade-audit-log
target_repo: athena-site
target_artifact_type: portfolio-policy
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

Land the reseller-audit questionnaire YAML the brief defined as a
portfolio artifact: vendor-log + reseller-log + upstream-provider-log
SLAs, reconciliation procedure, incident path ownership, training
carve-out, PE portfolio data segregation.

## Why this earns a promotion

Three audit logs (provider, reseller, customer) is the new shape any
portfolio repo selling into PE or consultancy clients has to answer
for. supplier-risk-rag has the most direct exposure; athena-site is
where the canonical template should live so the procurement-side repos
can fork from it. The brief pick gives the YAML; landing it in
athena-site costs minutes and removes a copy-paste cycle later.

## Where it would land

`athena-site/ops/reseller-audit-questions.yaml` (or under a `policies/`
subdir). `athena-site/factory.md` or the `/factory` page links to it.

## How we'd know it worked

supplier-risk-rag-agent's next vendor review uses the template
verbatim, and the answer to "which audit log governs when they
disagree" is written down.

## Source

Brief pick:
[briefs/2026-W22/brief.md - KPMG Digital Gateway](../../briefs/2026-W22/brief.md#kpmg-digital-gateway-powered-by-claude--write-your-consultancy-grade-audit-log-answer-this-quarter).
