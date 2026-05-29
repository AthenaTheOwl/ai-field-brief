# simon-copilot-exfil

- **Source:** Simon Willison (Microsoft Copilot Cowork exfiltration)
- **URL:** https://simonwillison.net/2026/May/26/copilot-cowork-exfiltrates-files/
- **Captured:** 2026-05-26
- **Priority:** high
- **Cells:** MTRX-W22-copilot-cowork-exfil-source_gist, MTRX-W22-copilot-cowork-exfil-mechanism_extraction, MTRX-W22-copilot-cowork-exfil-reusable_pattern, MTRX-W22-copilot-cowork-exfil-adoption_action, MTRX-W22-copilot-cowork-exfil-governance_surface

## What

Microsoft Copilot Cowork agents could send messages containing
attacker-supplied external images. When a recipient opened the
message, the image-load network request carried exfiltrated data
to an attacker-controlled host. Simon Willison documented the
chain end to end.

## Why it matters

This is the textbook prompt-injection exfiltration shape: external
content reaches the agent; the agent composes an outbound message;
the outbound message carries an attacker-controlled URL; the
recipient client renders the URL on open; the request leaks the
payload. Microsoft made the chain possible by skipping the
human-approval gate on agent-initiated email. The same shape
works on any agent that drafts outbound communications.

## Action surface

tool-policy, agent-role

## Concrete move

Add a single row to the tool-policy register and ship it. The row
names the outbound-communication surfaces and the controls on
each. The two-line minimum is: strip or proxy external image
references before send, and require explicit user approval before
an agent-composed message ships. Either alone is partial; both
together close the chain.

```yaml
agent_outbound_communications:
  email:
    external_images:        strip-or-proxy-through-sanitizer
    human_approval_required: yes
    audit_log:              every-draft-and-send
    allowed_recipients:     allowlist | broadcast-blocked
  slack_dm:
    external_links:         expand-and-display-target
    human_approval_required: yes-for-customer-channels
  calendar_invite:
    external_attachments:   block
    human_approval_required: yes
  ticket_comment:
    external_images:        strip
    human_approval_required: no-but-edit-window-required
```

## Caveats

Willison's writeup describes the chain but the excerpt does not
include CVE, affected versions, or Microsoft's response status —
verify Microsoft's advisory and mitigation status before relying
on a patch. Image-stripping mitigations can break legitimate
inline-image flows; pair with a per-agent allowlist of inline-image
sources where workflow requires it.
