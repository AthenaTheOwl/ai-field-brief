# Enterprise-managed MCP connector access

- lane: primary-source
- source: [Anthropic / Claude.com](https://claude.com/blog/enterprise-managed-auth)
- published: 2026-06-18
- confidence: high
- action_surface: tool-policy

**Gist:** Admins now provision MCP connectors through identity providers (Okta at launch) so users get connector access automatically on first login.

**Mechanism:** Admin connects IdP to Claude and selects which MCP connectors to enable. IdP groups/roles map to per-user connector availability. Launch coverage: Asana, Atlassian, Canva, Figma, Granola, Linear, Supabase; Slack coming. Beta on Team and Enterprise.

**Why matters:** MCP moves from per-user OAuth pain to IT-governed default access. Removes the biggest blocker to MCP adoption inside regulated orgs.

**Try:** Audit your MCP connector list and tag each as IdP-eligible vs not; for the eligible ones, draft an Okta group-to-connector mapping.

**Related thread:** agent runtime maturation
