# simon-copilot-exfil

- **Source:** Simon Willison's Weblog
- **URL:** https://simonwillison.net/2026/May/26/copilot-cowork-exfiltrates-files/
- **Captured:** 2026-05-26
- **Priority:** high
- **Cells:** MTRX-W22-copilot-source_gist, MTRX-W22-copilot-mechanism_extraction, MTRX-W22-copilot-adoption_action, MTRX-W22-copilot-governance_surface

## What

Microsoft Copilot Cowork allowed agents to send emails to user
inboxes without explicit approval. Because messages can contain
external images that trigger network requests, attacker-controlled
prompt injection could exfiltrate OneDrive pre-authenticated
download links when the user opened the message.

## Why it matters

This is the textbook prompt-injection exfiltration chain: external
content reaches the agent; agent composes outbound communication;
communication carries an attacker-supplied external resource URL;
recipient client requests the resource; request URL leaks the
payload. The Microsoft product made the attack possible by skipping
the human-approval gate on agent-initiated email.

## Action surface

tool-policy, agent-role

## Concrete move

Two-line defense for any agent that drafts outbound communication:
(1) strip or proxy external image references before send;
(2) require explicit user approval before any agent-composed
message ships. Add an "outbound communications" row to the tool-
policy register with explicit allowed-vs-disallowed actions per
surface (email, Slack DM, calendar invite, ticket comment).

## Caveats

The post characterizes the attack but does not detail Microsoft's
remediation. Status of the fix at time of writing is unconfirmed;
treat agent-initiated outbound communications as the highest-risk
tool category regardless of vendor.
