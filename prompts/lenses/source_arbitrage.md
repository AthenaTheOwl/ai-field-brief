# Lens: Source Arbitrage

Decide whether this source is useful before it becomes obvious.

Output:
- early_signal: yes / no / unclear
- why_others_might_miss_it
- mechanism_to_extract
- adoption_window: now / next_month / monitor
- mainstream_lag_indicator
- false_positive_risk
- demotion_rule

Rules:
- Do not reward obscurity by itself.
- Reward concrete shipped behavior, repo changes, reproducible demos,
  maintainer comments, or adoption signals.
- Penalize funding-only posts, launch copy without technical detail,
  and reposts of already-mainstream claims.
- If the item has no action surface, mark early_signal as no.
