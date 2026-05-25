import Link from "next/link";
import { listBriefs } from "../lib/briefs";
import { SiteFooter, SiteNav } from "../components/SiteNav";

export const dynamic = "force-static";
export const revalidate = false;

export default function HomePage() {
  const briefs = listBriefs();
  const latest = briefs[0];

  return (
    <div className="min-h-screen bg-white text-neutral-900 dark:bg-neutral-950 dark:text-neutral-100">
      <SiteNav tagline="weekly AI digest with concrete moves" />
      <main className="mx-auto max-w-3xl space-y-12 px-4 py-12">
        <section className="space-y-4">
          <h1 className="text-4xl font-semibold tracking-tight">
            ai-field-brief
          </h1>
          <p className="text-lg text-neutral-700 dark:text-neutral-200">
            A weekly AI digest for builder-TPMs. Each pick names one
            thing to do before next Friday and shows the artifact — a
            contract test, an incident runbook, a procurement
            checklist, a unit-economics table, a judge prompt.
          </p>
          <p className="text-neutral-600 dark:text-neutral-300">
            Sources curated for primary-source signal: Anthropic,
            OpenAI, Latent Space, Simon Willison, Dwarkesh, Eugene
            Yan, Hamel Husain, Applied LLMs, plus a small set of
            strategy reads.
          </p>
        </section>

        <section className="space-y-4">
          <h3 className="text-sm font-medium uppercase tracking-wide text-neutral-500">
            what makes this different
          </h3>
          <ul className="space-y-3 text-neutral-700 dark:text-neutral-200">
            <li>
              <strong className="font-medium">
                Concrete moves, not summaries.
              </strong>{" "}
              Every pick ends with one move you can run this week, and
              the worked artifact that goes with it.
            </li>
            <li>
              <strong className="font-medium">
                Voice-lint enforced.
              </strong>{" "}
              The eight-gate CI runs <code>scripts/voice_lint.py</code>{" "}
              against every brief. The banlist covers the usual AI
              cadence and the antithetical-reversal patterns; failure
              blocks the merge.
            </li>
            <li>
              <strong className="font-medium">
                Primary-source curated.
              </strong>{" "}
              The source list lives in{" "}
              <code>sources/registry.yaml</code> with lane, cadence,
              and quality tags. Selection rule: each entry has a
              verifiable tie to a tier-one operator.
            </li>
          </ul>
        </section>

        {latest ? (
          <section className="space-y-3 rounded border border-neutral-200 p-6 dark:border-neutral-800">
            <div className="text-xs uppercase tracking-wide text-neutral-500">
              latest · {latest.week}
              {latest.date ? ` · ${latest.date}` : ""}
            </div>
            <h2 className="text-2xl font-medium">
              <Link href={`/briefs/${latest.week}`} className="hover:underline">
                {latest.title}
              </Link>
            </h2>
            <p className="text-sm text-neutral-600 dark:text-neutral-300">
              {latest.meta?.sources_reviewed
                ? `${latest.meta.sources_reviewed.filter((s) => s.status === "ok").length} sources swept, ${latest.meta.sources_reviewed.reduce((sum, s) => sum + (s.items_included ?? 0), 0)} items included.`
                : "Read the latest brief."}
            </p>
            <p>
              <Link
                href={`/briefs/${latest.week}`}
                className="text-sm font-medium hover:underline"
              >
                read →
              </Link>
            </p>
          </section>
        ) : null}

        <section className="space-y-3">
          <h3 className="text-sm font-medium uppercase tracking-wide text-neutral-500">
            what's in the archive
          </h3>
          <ul className="space-y-2 text-neutral-700 dark:text-neutral-200">
            {briefs.slice(0, 10).map((b) => (
              <li key={b.week}>
                <Link
                  href={`/briefs/${b.week}`}
                  className="hover:underline"
                >
                  <span className="font-mono text-sm text-neutral-500">
                    {b.week}
                  </span>{" "}
                  — {b.title}
                </Link>
              </li>
            ))}
          </ul>
          {briefs.length > 10 ? (
            <Link href="/briefs" className="text-sm hover:underline">
              see all {briefs.length} →
            </Link>
          ) : null}
        </section>

        <section className="space-y-2 text-sm text-neutral-600 dark:text-neutral-300">
          <h3 className="text-sm font-medium uppercase tracking-wide text-neutral-500">
            subscribe
          </h3>
          <p className="flex flex-wrap gap-x-4 gap-y-2">
            <a href="/feed.xml" className="hover:underline">
              RSS
            </a>
            <a href="/atom.xml" className="hover:underline">
              Atom
            </a>
            <a href="/feed.json" className="hover:underline">
              JSON Feed
            </a>
          </p>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
