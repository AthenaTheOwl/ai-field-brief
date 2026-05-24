---
id: memory-003-jsonschema-ref-needs-registry
target_kind: memory_update
target: .agents/AGENTS.md
human_review_required: true
status: promoted
promotion_date: 2026-05-24
evidence:
  - kind: file
    ref: scripts/validate_schemas.py lines 84–107 — build_registry() exists because $ref-by-URL was reaching for DNS during CI
  - kind: file
    ref: scripts/validate_schemas.py line 89 — comment "CI runs offline; local dev shouldn't depend on DNS"
  - kind: file
    ref: scripts/validate_decisions.py lines 32–46 — same pattern, remote-then-cache fallback at FETCH_TIMEOUT_SECONDS = 5
  - kind: file
    ref: ops/schemas-cache/ — seven cached cross-repo schemas, mirror of athena-site/ops/schemas/
---

## proposal

Add a `## Cross-repo schema rule` block to `.agents/AGENTS.md` under `## Cross-repo links`. The block names the rule: a schema that points at another schema by URL fails in CI unless the validator builds a `referencing.Registry` of every local schema first. The block also names the cache-fallback pattern for any new validator script.

Proposed text (to be reviewed and edited by a human, not auto-applied):

```markdown
## Cross-repo schema rule

The repo's `*.schema.json` files use absolute `$id` URLs that point at
`athena-site/ops/schemas/`. Two consequences a new validator script must
plan for:

1. **`$ref` to a sibling schema needs a registry.** `jsonschema` resolves
   absolute `$ref` URLs by HTTP fetch by default. CI runs offline. Build
   a `referencing.Registry` of every discovered schema, keyed by `$id`,
   and pass it to the validator (see `scripts/validate_schemas.py`
   `build_registry()` for the pattern).
2. **Remote-then-cache for cross-repo schemas.** A validator that
   consumes a cross-repo schema fetches the canonical URL with a
   5-second timeout and falls back to `ops/schemas-cache/<name>.json`
   on any failure (URLError, TimeoutError, JSONDecodeError, OSError).
   See `scripts/validate_decisions.py` `load_remote_schema()` /
   `load_cached_schema()`.

The agent that writes a new `validate_<thing>.py` copies one of these
two scripts as the starting point.
```

## why it earns its keep

`validate_schemas.py` `build_registry()` exists because the naive pattern (instantiate `jsonschema.Draft202012Validator(schema)` and call it) tries to fetch every `$ref` URL over the wire. CI runs offline; local dev runs over a flaky connection. The fix is twelve lines of boilerplate per validator script. Today the pattern lives in the script's docstring; a new validator script that skips the pattern fails the first time CI runs with no internet.

Spec 0011 (`b4b9cf2`) shipped three new validator scripts in one commit (`validate_roles.py`, `validate_tools.py`, `validate_policies.py`). All three followed the pattern, which suggests the author read the prior scripts first. Naming the rule in AGENTS.md makes that read explicit instead of optional.

## evidence

- `scripts/validate_schemas.py` line 89: `"CI runs offline; local dev shouldn't depend on DNS."` The comment is the institutional memory; the AGENTS.md block promotes it from comment to contract.
- `scripts/validate_decisions.py` lines 32–46: the remote-then-cache pattern with explicit exception list. The exception list matters — a bare `except` would swallow signal.
- `scripts/validate_schemas.py` `build_registry()` returns `None` if `referencing` is not installed, so a downstream call falls back gracefully. The pattern is worth naming because the graceful-fallback shape is non-obvious.
- `ops/schemas-cache/` holds seven JSON files mirroring `athena-site/ops/schemas/`. The cache is the proof the pattern is repo-wide, not script-local.

## promotion path

If approved, the change touches one file:

- `.agents/AGENTS.md` — add the new block under `## Cross-repo links`.

Reviewer checks:

1. The block matches the actual code in `validate_schemas.py` and `validate_decisions.py` line-for-line on the import names and exception list.
2. The block names a starting-point script the next agent copies from. Reviewer picks: `validate_schemas.py` (registry pattern) or `validate_decisions.py` (cache fallback) or both.
3. The block does not duplicate `scripts/validate_schemas.py`'s docstring; if the reviewer thinks the rule belongs in the docstring instead, the AGENTS.md block links to the docstring.

Owner role: `engineering.implementation`.

## risks if promoted blindly

- The pattern depends on the `referencing` and `jsonschema` Python libraries being installed in CI. The current CI configuration installs them; a future stripped-down CI might not. Reviewer should confirm the CI workflow file (`.github/workflows/ci.yml`) installs the deps before promoting the block as a hard rule.
- The 5-second fetch timeout is a guess. Reviewer may want a `SCHEMA_FETCH_TIMEOUT` constant pulled out so the value lives in one place.
- A block that names "always build a registry" is over-prescriptive. A validator that consumes a single schema with no `$ref` does not need a registry. The block should name the rule with the conditional "when your schema has `$ref` to a sibling" instead of as a blanket requirement.
