# Vercel Passport puts agents behind OIDC identity providers

- lane: frontier-scout
- source: [Vercel / The Register](https://www.theregister.com/devops/2026/06/19/vercel-debuts-eve-open-source-agent-framework-tries-to-fix-shadow-ai-with-passport/5258726)
- published: 2026-06-19
- confidence: high
- action_surface: tool-policy

**Gist:** Alongside Eve, Vercel launched Passport, an OIDC layer that routes both apps and agents through Okta/Entra/Auth0 and issues short-lived credentials for Slack/GitHub/Snowflake/Salesforce in place of static keys.

**Mechanism:** Identity-provider gating at the deployment edge; agent connection layer mints short-lived per-task tokens rather than long-lived secrets; private-by-default with centralized audit.

**Why matters:** Concrete pattern for the agent-identity gap that comes up whenever roles in a control plane need to call out to real SaaS. Worth tracking as a reference for how the policy engine layer should issue tool credentials.

**Try:** Enumerate every long-lived token currently embedded in your agent harness; map each to the equivalent Passport-style short-lived credential issuer that would replace it.

**Related thread:** agent runtime maturation
