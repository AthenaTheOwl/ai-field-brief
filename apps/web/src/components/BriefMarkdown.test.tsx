import { describe, expect, it } from "vitest";

import { stripBriefChrome } from "./BriefMarkdown";

describe("stripBriefChrome", () => {
  it("removes publish metadata comments before stripping the page-owned H1", () => {
    const body = stripBriefChrome(`<!--
iso_week: 2026-W27
through_date: 2026-06-30
-->

# Frameworks are becoming the control plane for agent work

## Field thesis

The useful agent framework is no longer a prettier way to call a model.
`);

    expect(body).not.toContain("<!--");
    expect(body).not.toContain("iso_week");
    expect(body).not.toContain("# Frameworks are becoming");
    expect(body.trimStart()).toMatch(/^## Field thesis/);
  });

  it("keeps ordinary body headings intact", () => {
    const body = stripBriefChrome(`# Title

## Top signals

### 1. First signal
`);

    expect(body.trim()).toBe("## Top signals\n\n### 1. First signal");
  });
});
