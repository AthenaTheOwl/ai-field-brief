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
      <SiteNav />
      <main className="mx-auto max-w-3xl space-y-12 px-4 py-12">
        <section className="space-y-4">
          <h1 className="text-4xl font-semibold tracking-tight">
            ai-field-brief
          </h1>
          <p className="text-lg text-neutral-700 dark:text-neutral-200">
            Weekly digest of what changed in AI. Less news, more
            insight. Every pick comes with a concrete move you can run
            before next Friday and a worked example.
          </p>
          <p className="text-neutral-600 dark:text-neutral-300">
            Sources curated for primary-source signal: Anthropic,
            OpenAI, Latent Space, Simon Willison, Dwarkesh, Eugene Yan,
            Hamel Husain, plus a small set of strategy reads.
          </p>
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
      </main>
      <SiteFooter />
    </div>
  );
}
