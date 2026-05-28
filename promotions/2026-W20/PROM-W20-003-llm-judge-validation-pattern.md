---
id: PROM-W20-003
brief: 2026-W20
pick_slug: hamel-revenge-of-the-data-scientist-judge-validation
target_repo: trace-to-eval-harness
target_artifact_type: skill
date: 2026-05-25
status: proposed
landed_commit: null
---

## What

Land the LLM-judge-as-classifier validation pattern from the brief
(hand-label 50, run judge, compute precision and recall, fail the judge
prompt below 0.85 on either) as a SKILL.md in trace-to-eval-harness,
with a runnable `eval/validate_judge.py` template under the SKILL.

## Why this earns a promotion

trace-to-eval-harness is the eval-discipline repo. The judge validation
pattern is the missing piece between "we have a judge" and "the judge
gates a release"; codifying it as a SKILL means any portfolio repo can
import the discipline. The 50-sample pass is one afternoon — landing
the SKILL makes it routinely doable instead of someone re-deriving it
each quarter.

## Where it would land

`trace-to-eval-harness/.agents/skills/validate-llm-judge/SKILL.md`
with a `validate_judge.py` template alongside. The brief pick's worked
artifact is the body.

## How we'd know it worked

The next portfolio repo that ships an LLM judge runs the validation
SKILL, files the precision/recall numbers, and gates release on the
0.85 threshold.

## Source

Brief pick:
[briefs/2026-W20/brief.md - Revenge of the Data Scientist](../../briefs/2026-W20/brief.md#hamel-husain-revenge-of-the-data-scientist--pick-one-llm-judge-and-validate-it-as-a-classifier-this-week).
