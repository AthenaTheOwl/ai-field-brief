"""One-shot: render briefs/2026-W25/{brief.md,meta.yaml} from the workflow output."""
from __future__ import annotations

import json
from pathlib import Path

OUTPUT = Path(r"C:\Users\Vignesh\AppData\Local\Temp\claude\e--claude-code-random-apps\dd454cb3-2fa8-4527-a78d-eae9446681f4\tasks\wn196fd1p.output")
BRIEFS = Path(r"e:\claude_code\random-apps\ai-field-brief\briefs\2026-W25")

ISO_WEEK = "2026-W25"
THROUGH_DATE = "2026-06-21"
VOLUME = 2

def main():
    BRIEFS.mkdir(parents=True, exist_ok=True)
    payload = json.loads(OUTPUT.read_text(encoding="utf-8"))["result"]
    brief = payload["brief"]
    swept = payload["sources_swept_total"]
    failed = payload["sources_failed_total"]
    items_collected = payload["items_collected"]
    raw_items = payload["raw_items"]
    lane_notes = payload["lane_notes_raw"]

    # --- brief.md ---
    lines: list[str] = []
    lines.append("<!--")
    lines.append("meta:")
    lines.append(f"  iso_week: {ISO_WEEK}")
    lines.append(f"  through_date: {THROUGH_DATE}")
    lines.append("  profile_id: broad_builder")
    lines.append(f"  sources_swept_count: {swept}")
    lines.append(f"  items_collected: {items_collected}")
    lines.append(f"  volume: {VOLUME:03d}")
    lines.append("  mode: workflow-driven")
    lines.append("-->")
    lines.append("")
    lines.append(f"# {brief['title']}")
    lines.append("")
    lines.append(f"**week of 2026-06-15 - audience: builder-tpms thinking about AI - vol. {VOLUME:03d}**")
    lines.append("")
    lines.append("## Field thesis")
    lines.append("")
    lines.append(brief["field_thesis"])
    lines.append("")
    lines.append(f"{len(brief['top_signals'])} top signals, {len(brief['watchlist'])} watchlist items, {swept} sources reviewed ({failed} failed).")
    lines.append("")
    lines.append("## Top signals")
    lines.append("")
    for i, t in enumerate(brief["top_signals"], 1):
        lines.append(f"### {i}. {t['name']}")
        lines.append("")
        lines.append(f"**Source:** [{t['source_name']}]({t['source_url']})")
        lines.append("")
        lines.append(f"**Payload:** {t['payload']}")
        lines.append("")
        lines.append(f"**Mechanism:** {t['mechanism']}")
        lines.append("")
        lines.append(f"**Why it matters:** {t['why_matters']}")
        lines.append("")
        lines.append(f"**Reusable pattern:** {t['reusable_pattern']}")
        lines.append("")
        lines.append(f"**Action surface:** {t['action_surface']}")
        lines.append("")
        lines.append(f"**Try:** {t['try_action']}")
        lines.append("")
        if t.get("systems_map"):
            lines.append(f"**Systems map:** {t['systems_map']}")
            lines.append("")
        if t.get("transferable_principle"):
            lines.append(f"**Transferable principle:** {t['transferable_principle']}")
            lines.append("")
        lines.append(f"**Confidence:** {t['confidence']}")
        lines.append("")
        lines.append("---")
        lines.append("")
    lines.append("## Reusable patterns")
    lines.append("")
    for p in brief["reusable_patterns"]:
        lines.append(f"- **{p['pattern']}** — {p['one_line']}")
    lines.append("")
    lines.append("## Action queue")
    lines.append("")
    for a in brief["action_queue"]:
        lines.append(f"- **{a['action']}**")
        lines.append(f"  - surface: {a['surface']}")
        lines.append(f"  - rationale: {a['rationale']}")
    lines.append("")
    lines.append("## Watchlist")
    lines.append("")
    for w in brief["watchlist"]:
        lines.append(f"- **{w['item']}**")
        lines.append(f"  - revisit when: {w['revisit_trigger']}")
    lines.append("")
    lines.append("## Sources reviewed")
    lines.append("")
    for s in brief["sources_reviewed"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("## Lane notes")
    lines.append("")
    for n in lane_notes:
        lines.append(f"**{n['lane']}**: {n['notes']}")
        lines.append("")

    brief_md = BRIEFS / "brief.md"
    brief_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {brief_md} ({len(lines)} lines)")

    # --- meta.yaml ---
    meta_yaml = BRIEFS / "meta.yaml"
    meta_lines = [
        f"iso_week: {ISO_WEEK}",
        f"through_date: {THROUGH_DATE}",
        "profile_id: broad_builder",
        f"volume: {VOLUME}",
        "mode: workflow-driven",
        f"sources_swept_count: {swept}",
        f"sources_failed_count: {failed}",
        f"items_collected: {items_collected}",
        f"items_included: {len(brief['top_signals'])}",
        "workflow_run_id: wn196fd1p",
        "workflow_trace: wf_77db0372-eea",
        "synthesis_actor: claude-opus-4-7 (via Workflow tool, ultracode parallel sweep)",
        "lanes_returned:",
    ]
    for n in lane_notes:
        meta_lines.append(f"  - {n['lane']}")
    meta_lines.append("")
    meta_lines.append("# lane sweep yield (items collected per lane)")
    by_lane = {}
    for it in raw_items:
        by_lane.setdefault(it.get("lane", "unknown"), 0)
        by_lane[it["lane"]] += 1
    meta_lines.append("lane_yield:")
    for lane, n in sorted(by_lane.items()):
        meta_lines.append(f"  {lane}: {n}")
    meta_yaml.write_text("\n".join(meta_lines) + "\n", encoding="utf-8")
    print(f"wrote {meta_yaml}")

    # --- items/ (one file per collected item, slim) ---
    items_dir = BRIEFS / "items"
    items_dir.mkdir(exist_ok=True)
    for i, it in enumerate(raw_items, 1):
        slug = f"{i:03d}-{(it.get('source_name', 'src')[:30].lower().replace(' ', '-').replace('/', '-'))}.md"
        item_lines = [
            f"# {it.get('title', '(no title)')}",
            "",
            f"- lane: {it.get('lane')}",
            f"- source: [{it.get('source_name')}]({it.get('source_url')})",
            f"- published: {it.get('published_at')}",
            f"- confidence: {it.get('confidence')}",
            f"- action_surface: {it.get('action_surface', '—')}",
            "",
            f"**Gist:** {it.get('gist')}",
            "",
            f"**Mechanism:** {it.get('mechanism')}",
            "",
            f"**Why matters:** {it.get('why_matters')}",
            "",
        ]
        if it.get("try_action"):
            item_lines.append(f"**Try:** {it['try_action']}")
            item_lines.append("")
        if it.get("related_to"):
            item_lines.append(f"**Related thread:** {it['related_to']}")
            item_lines.append("")
        (items_dir / slug).write_text("\n".join(item_lines), encoding="utf-8")
    print(f"wrote {len(raw_items)} item notes to {items_dir}")

if __name__ == "__main__":
    main()
