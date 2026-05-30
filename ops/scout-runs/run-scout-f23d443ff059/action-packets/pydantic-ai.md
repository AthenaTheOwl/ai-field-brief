# Action packet: Port one ai-field-brief lens to a Pydantic AI Agent with typed output_type

- Source: `pydantic-ai` (https://github.com/pydantic/pydantic-ai)
- Snapshot: `ops/scout-snapshots/run-scout-f23d443ff059/pydantic-ai-github.html`
- Cell ids: MTRX-scout-run-scout-f23d443ff059-pydantic-ai-action_packet, MTRX-scout-run-scout-f23d443ff059-pydantic-ai-repo_project_scan
- Disposition: prototype
- Effort: small (one snapshot, one Agent definition, one comparison run)

## Hypothesis

A typed Pydantic output_type on an Agent eliminates the JSON-shape repair code we currently rely on in lens cell generation, and the resulting Agent definition is small enough to live as a reusable capability bundle in CDCP — without forcing us to adopt the full pydantic_ai runtime across all roles.

## Test

In a throwaway branch, install `pydantic-ai`, define one Agent whose `output_type` is a Pydantic model mirroring the current source_arbitrage cell schema (id, lens_id, mode, content, source_ref_quote, confidence, faithfulness_status). Run it against the same `pydantic-ai-github.html` snapshot via Anthropic provider; compare validation-error rate and lines-of-glue-code vs. the current StructuredOutput tool-call path.

## Success metric

Zero schema-repair retries across 5 snapshots AND glue-code line count drops by at least 30% vs. the current path, observable within one week.

## Risk

Adopts a framework the user has flagged as soup risk; even pattern-only adoption may leak through if we keep the runtime dep. Logfire tie-in could pull in unwanted observability surface.

## Kill criterion

Kill if the validation-error rate is not strictly lower than the current StructuredOutput path, or if removing the dep requires reimplementing more than one helper. Demote to archive if we end up importing `pydantic_ai.Agent` instead of using it as design inspiration.
