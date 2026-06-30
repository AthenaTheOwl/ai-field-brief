import Link from "next/link";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { BriefMarkdown } from "../../../components/BriefMarkdown";
import { getBrief, listWeeks } from "../../../lib/briefs";

interface RouteParams {
  params: Promise<{ week: string }>;
}

type BriefMeta = NonNullable<ReturnType<typeof getBrief>>["meta"];
type SourceReview = NonNullable<NonNullable<BriefMeta>["sources_reviewed"]>[number];

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
    return { title: "brief not found - ai-field-brief" };
  }
  return {
    title: `${brief.title} - ai-field-brief`,
    description: `Weekly AI brief - ${brief.week}. Concrete moves and worked examples.`,
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
          {"<- all briefs"}
        </Link>
      </nav>

      <header className="space-y-3 border-b border-neutral-200 pb-6 dark:border-neutral-800">
        <div className="text-xs uppercase tracking-wide text-neutral-500">
          {brief.week} - vol. {String(brief.volume).padStart(3, "0")}
          {brief.date ? ` - ${brief.date}` : ""}
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

function sourceLabel(source: SourceReview, index: number): string {
  return source.label ?? source.id ?? source.url ?? `source ${index + 1}`;
}

function sourceDisposition(source: SourceReview): string {
  return (source.disposition ?? source.status ?? source.error ?? "reviewed").replaceAll(
    "_",
    " ",
  );
}

function sourceMixSummary(sources: SourceReview[]): string {
  const counts = sources.reduce<Record<string, number>>((acc, source) => {
    const key = sourceDisposition(source);
    acc[key] = (acc[key] ?? 0) + 1;
    return acc;
  }, {});

  return Object.entries(counts)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([label, count]) => `${label}: ${count}`)
    .join("; ");
}

function BriefMetaPanel({ meta }: { meta: BriefMeta }) {
  if (!meta) return null;

  const sources = meta.sources_reviewed ?? [];
  const sourceSummary = sourceMixSummary(sources);
  const hasCaptureCounts = sources.some(
    (source) =>
      source.items_captured != null ||
      source.items_included != null ||
      source.last_item_date != null,
  );

  return (
    <details className="mt-16 rounded border border-neutral-200 p-4 text-sm text-neutral-600 dark:border-neutral-800 dark:text-neutral-300">
      <summary className="cursor-pointer font-medium text-neutral-700 dark:text-neutral-200">
        publication notes
      </summary>
      <div className="mt-3 space-y-3">
        <p>
          Generated {meta.generated_at} by {meta.generated_by}.
        </p>
        {meta.sweep ? (
          <p>
            Source sweep: {meta.sweep.succeeded} reviewed, {meta.sweep.failed} failed
            of {meta.sweep.attempted} attempted.
          </p>
        ) : null}
        {sourceSummary ? <p>Source mix: {sourceSummary}.</p> : null}
        {meta.notes && meta.notes.length > 0 ? (
          <ul className="list-disc space-y-1 pl-5">
            {meta.notes.map((note) => (
              <li key={note}>{note}</li>
            ))}
          </ul>
        ) : null}
        {sources.length > 0 ? (
          <table className="mt-2 w-full text-left text-xs">
            <thead className="text-neutral-500">
              <tr>
                <th className="pb-1 pr-3">source</th>
                <th className="pb-1 pr-3">disposition</th>
                {hasCaptureCounts ? (
                  <>
                    <th className="pb-1 pr-3">captured</th>
                    <th className="pb-1 pr-3">included</th>
                    <th className="pb-1">last item</th>
                  </>
                ) : null}
              </tr>
            </thead>
            <tbody>
              {sources.map((source, index) => {
                const label = sourceLabel(source, index);
                return (
                  <tr
                    key={`${label}-${index}`}
                    className="border-t border-neutral-100 dark:border-neutral-800"
                  >
                    <td className="py-1 pr-3">
                      {source.url ? (
                        <a
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="underline decoration-neutral-300 underline-offset-2 hover:decoration-neutral-600"
                        >
                          {label}
                        </a>
                      ) : (
                        label
                      )}
                    </td>
                    <td className="py-1 pr-3">{sourceDisposition(source)}</td>
                    {hasCaptureCounts ? (
                      <>
                        <td className="py-1 pr-3">{source.items_captured ?? "-"}</td>
                        <td className="py-1 pr-3">{source.items_included ?? "-"}</td>
                        <td className="py-1">{source.last_item_date ?? "-"}</td>
                      </>
                    ) : null}
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : null}
      </div>
    </details>
  );
}
