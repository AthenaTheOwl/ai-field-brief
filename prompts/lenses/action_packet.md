# Lens: Action Packet

Turn a source item into a small, testable move.

Output:
- target_repo_or_surface
- action_surface
- proposed_change
- proof_metric
- test_plan
- effort
- risk
- rollback
- kill_criterion
- disposition: adopt_now / prototype / monitor / archive / reject

Rules:
- The packet must be doable without a new product strategy meeting.
- The proof metric must be observable within one week.
- The kill criterion must be specific enough to prevent zombie
  experiments.
- If the source does not support the proposed change, reject the packet.
