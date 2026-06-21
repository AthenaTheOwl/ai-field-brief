# Open Knowledge Format v0.1 published as a portable wiki spec for agents

- lane: frontier-scout
- source: [Google Cloud / MarkTechPost](https://www.marktechpost.com/2026/06/16/google-cloud-introduces-open-knowledge-format-okf-a-vendor-neutral-markdown-spec-for-giving-ai-agents-curated-context/)
- published: 2026-06-12
- confidence: high
- action_surface: personal-knowledge-base

**Gist:** Google Cloud released OKF v0.1, an Apache-2.0 spec for organizing org knowledge as a directory of markdown files with YAML frontmatter, plus three sample bundles (GA4, Stack Overflow, Bitcoin datasets) and a static HTML graph visualizer.

**Mechanism:** Each concept is a markdown file with a required 'type' field in YAML frontmatter; producers choose the rest of the schema; bundles render to an interactive graph via a single self-contained HTML file with no backend.

**Why matters:** First serious attempt to give the AGENTS.md / CLAUDE.md / Obsidian-vault pattern a producer-agnostic interchange format. Directly relevant to the personal-knowledge-base lane and to any control plane that wants role context to be portable.

**Try:** Convert one folder of your existing memory/ notes into an OKF bundle (one 'type' field per file) and open the bundle in the OKF static visualizer to see whether the graph view reveals missing edges.

**Related thread:** directory-as-agent convergence
