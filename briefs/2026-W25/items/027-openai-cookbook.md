# Trigger a Workspace Agent from the API

- lane: builder-practice
- source: [OpenAI Cookbook](https://developers.openai.com/cookbook/examples/chatgpt/workspace_agents/workspace-agents-api-trigger)
- published: 2026-06-18
- confidence: high
- action_surface: runtime-adapter

**Gist:** New cookbook teaches how to fire a saved Workspace Agent from an external event via an API channel trigger ID.

**Mechanism:** Add an API channel in the Workspace Agent builder to mint an agtch_... trigger ID; authenticate with a Workspace Agent access token (not platform API key); POST source event to /v1/workspace_agents/{id}/trigger with Idempotency-Key; endpoint returns 202 and run is async, so verification happens at the configured destination, not in the HTTP response.

**Why matters:** First-class pattern for treating ChatGPT-saved workflows as callable services from your own backends; replaces ad-hoc scripts and gives ops a stable trigger ID per workflow.

**Try:** Take one existing Workspace Agent, attach an API channel, and POST one test event from a notebook to confirm the destination gets written.

**Related thread:** agent runtime maturation
