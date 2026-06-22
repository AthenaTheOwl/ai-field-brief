# Zero-Touch OAuth for MCP

- lane: fast-signal
- source: [Hacker News (front page)](https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/)
- published: 2026-06-18
- confidence: medium
- action_surface: tool-policy

**Gist:** MCP enterprise-managed auth post outlining zero-touch OAuth pattern for MCP servers; hit HN front page on June 18.

**Mechanism:** Removes the manual OAuth setup step that currently blocks org-wide MCP rollout; enterprise IT can provision MCP server credentials centrally instead of per-user device flow.

**Why matters:** OAuth friction has been the gating issue for MCP adoption inside companies; if this lands cleanly, MCP server count inside enterprises jumps in H2.

**Try:** If you run an MCP server, read the spec and stub the zero-touch OAuth path against your IdP; note which scopes you'd need to pre-provision before rollout.

**Related thread:** agent runtime maturation
