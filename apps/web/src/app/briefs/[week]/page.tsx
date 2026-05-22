import Link from "next/link";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { BriefMarkdown } from "../../../components/BriefMarkdown";
import { getBrief, listWeeks } from "../../../lib/briefs";

interface RouteParams {
  params: Promise<{ week: string }>;
}

export const dynamicParams = false;
export const revalidate = false;

export function generateStaticParams() {
  return listWeeks().map((week) => ({ week }));
}

export async function generateMetadata({
  params,
}: RouteParams): Promise<Metadata> {
  const { week } = await params;
  const brief = getBrief(week);
  if (!brief) {
    return { title: "brief not found · ai-field-brief" };
  }
  return {
    title: `${brief.title} · ai-field-brief`,
    description: `Weekly AI brief — ${brief.week}. Concrete moves and worked examples.`,
  };
}

export default async function BriefPage({ params }: RouteParams) {
  const { week } = await params;
  const brief = getBrief(week);
  if (!brief) {
    notFound();
  }

  return (
    <div className="space-y-10">
      <nav className="text-sm text-neutral-500">
        <Link href="/briefs" className="hover:underline">
          ← all briefs
        </Link>
      </nav>

      <header className="space-y-3 border-b border-neutral-200 pb-6 dark:border-neutral-800">
        <div className="text-xs uppercase tracking-wide text-neutral-500">
          {brief.week} · vol. {String(brief.volume).padStart(3, "0")}
          {brief.date ? ` · ${brief.date}` : ""}
        </div>
        <h1 className="text-3xl font-semibold tracking-tight">
          {brief.title}
        </h1>
      </header>

      <BriefMarkdown source={brief.markdown} />

      {brief.meta ? <BriefMetaPanel meta={brief.meta} /> : null}
    </div>
  );
}

function BriefMetaPanel({ meta }: { meta: NonNullable<ReturnType<typeof getBrief>>["meta"] }) {
  if (!meta) return null;
  return (
    <details className="mt-16 rounded border border-neutral-200 p-4 text-sm text-neutral-600 dark:border-neutral-800 dark:text-neutral-300">
      <summary className="cursor-pointer font-medium text-neutral-700 dark:text-neutral-200">
        sweep audit log
      </summary>
      <div className="mt-3 space-y-2">
        <p>
          generated {meta.generated_at} by {meta.generated_by}.
        </p>
        {meta.sweep ? (
          <p>
            sweep: {meta.sweep.succeeded} ok · {meta.sweep.failed} failed
            of {meta.sweep.attempted} attempted.
          </p>
        ) : null}
        {meta.sources_reviewed && meta.sources_reviewed.length > 0 ? (
          <table className="mt-2 w-full text-left text-xs">
            <thead className="text-neutral-500">
              <tr>
                <th className="pb-1 pr-3">source</th>
                <th className="pb-1 pr-3">status</th>
                <th className="pb-1 pr-3">captured</th>
                <th className="pb-1">included</th>
              </tr>
            </thead>
            <tbody>
              {meta.sources_reviewed.map((s) => (
                <tr key={s.id} className="border-t border-neutral-100 dark:border-neutral-800">
                  <td className="py-1 pr-3 font-mono">{s.id}</td>
                  <td className="py-1 pr-3">{s.status}</td>
                  <td className="py-1 pr-3">{s.items_captured ?? "-"}</td>
                  <td className="py-1">{s.items_included ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : null}
      </div>
    </details>
  );
}
