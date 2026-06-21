# ChatGPT scheduled tasks GA, Pulse sunset

- lane: primary-source
- source: [OpenAI Help Center (release notes)](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- published: 2026-06-17
- confidence: high
- action_surface: workflow

**Gist:** ChatGPT rolled out a dedicated Scheduled page for managing reminders and recurring work, made tasks faster and more reliable, and sunset Pulse (Pro retains 14 days).

**Mechanism:** Scheduled tasks now support specific times or time-of-day windows (morning/afternoon/evening). Notifications reworked. Pulse feature retired; Pro users get a 14-day grace window.

**Why matters:** Cron-style triggers are now a first-class ChatGPT surface, which competes directly with custom scheduler shims. If you built a Pulse-style daily-digest workflow, plan a migration.

**Try:** Move one daily prompt you currently run via cron into ChatGPT scheduled tasks and compare reliability over a week.

**Related thread:** agent runtime maturation
