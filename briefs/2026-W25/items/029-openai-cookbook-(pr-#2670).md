# Polish deployment manager app list and details

- lane: builder-practice
- source: [OpenAI Cookbook (PR #2670)](https://github.com/openai/openai-cookbook/pull/2670)
- published: 2026-06-17
- confidence: high
- action_surface: architecture

**Gist:** Update to the Agents SDK deployment-manager example: filters the Apps list to only managed deployments and standardizes container naming.

**Mechanism:** examples/agents_sdk/deployment_manager/app/ now hides removed deployments instead of leaving stale 'imported project' rows; container labels and Docker names derive from app name; deployment diagrams open in new tabs; trace lists kept compact.

**Why matters:** Small but telling: the reference deployment-manager pattern is converging on a real ops UI (named containers, filtered lists). Worth lifting as scaffold for in-house agent dashboards.

**Try:** Pull the deployment_manager/app folder and run it locally against one of your own agents to see the trace/app-list shape.

**Related thread:** agent runtime maturation
