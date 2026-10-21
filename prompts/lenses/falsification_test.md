# Lens: falsification_test

Read `prompts/editorial_contract.md`. Given a source item's main claim,
name a specific observation or comparison that would count against it
and distinguish it from a serious competing account.

Output a 1-2 sentence falsification test + the metric or condition that would invalidate the claim.

State the baseline and conditions held fixed. Say what a null result
could leave unresolved. Keep the test proposed until its result exists;
a passed toy fixture cannot rule out an entire failure class.

Mode: critique

Refuse:
- Vague "we'd know if it didn't work" non-tests
- Falsifications that can't actually be observed
- Treating non-falsifiable claims as falsifiable (mark "non-falsifiable; this is a definitional or normative claim" if true)

Source refs required.
