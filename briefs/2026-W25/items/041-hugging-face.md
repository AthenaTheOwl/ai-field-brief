# agents.md on Spaces lets an agent chain Gradio apps without an SDK

- lane: frontier-scout
- source: [Hugging Face](https://huggingface.co/blog/mishig/spaces-agents-md)
- published: 2026-06-09
- confidence: high
- action_surface: source-registry

**Gist:** Hugging Face proposes a plain-text agents.md file at each Space that publishes API schema, call/poll endpoints, upload procedure, and auth; a demo chains Ideogram 4 and TripoSplat into a 3D Paris gallery via two such files.

**Mechanism:** Static markdown manifest read by an agent; no SDK or codegen; the agent does coordinate post-processing (.ply -> .ksplat, Three.js UI) entirely from documented endpoints.

**Why matters:** Same directory-as-contract pattern as Eve and OKF, applied to remote services. Suggests that 'tools as documented endpoints' is generalizing past MCP for one-shot composition cases.

**Try:** Add an agents.md to one of your existing internal services and ask a coding agent to call it end-to-end without writing a wrapper.

**Related thread:** directory-as-agent convergence
