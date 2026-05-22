import Link from "next/link";
import type { Metadata } from "next";
import { listBriefs } from "../../lib/briefs";

export const dynamic = "force-static";
export const revalidate = false;

export const metadata: Metadata = {
  title: "briefs · ai-field-brief",
  description:
    "Weekly AI digest with concrete moves and worked examples. Updated every Friday.",
};

export default function BriefsIndexPage() {
  const briefs = listBriefs();

  return (
    <div className="space-y-10">
      <header className="space-y-3">
        <h1 className="text-3xl font-semibold tracking-tight">briefs</h1>
        <p className="text-neutral-600 dark:text-neutral-300">
          Weekly digest of what changed in AI this week, plus concrete
          moves you can run before next Friday. Short reflections, picks
          with comment, worked examples. Five-to-fifteen-minute read.
        </p>
      </header>

      <ul className="space-y-8 border-t border-neutral-200 dark:border-neutral-800">
        {briefs.map((b) => (
          <li
            key={b.week}
            className="border-b border-neutral-200 pb-8 dark:border-neutral-800"
          >
            <Link
              href={`/briefs/${b.week}`}
              className="group block space-y-2"
            >
              <div className="text-xs uppercase tracking-wide text-neutral-500">
                {b.week} · vol. {String(b.volume).padStart(3, "0")}
                {b.date ? ` · ${b.date}` : ""}
              </div>
              <h2 className="text-xl font-medium group-hover:underline">
                {b.title}
              </h2>
              {b.meta?.sweep ? (
                <p className="text-sm text-neutral-500">
                  sweep: {b.meta.sweep.succeeded} ok ·{" "}
                  {b.meta.sweep.failed} failed of{" "}
                  {b.meta.sweep.attempted} attempted
                </p>
              ) : null}
            </Link>
          </li>
        ))}
      </ul>

      {briefs.length === 0 ? (
        <p className="text-neutral-500">
          No briefs published yet. Run the playbook to publish one.
        </p>
      ) : null}
    </div>
  );
}
