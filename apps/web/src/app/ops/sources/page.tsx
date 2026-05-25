import { buildSourceOpsQueue, type SourceReadinessStatus } from "@aifieldbrief/sources/ops";

import { SiteFooter, SiteNav } from "@/components/SiteNav";

export const dynamic = "force-dynamic";

const STATUS_CLASS: Record<SourceReadinessStatus, string> = {
  ready: "border-emerald-700 text-emerald-800 dark:border-emerald-400 dark:text-emerald-300",
  "review-due": "border-amber-700 text-amber-800 dark:border-amber-400 dark:text-amber-300",
  "connector-stub": "border-red-700 text-red-800 dark:border-red-400 dark:text-red-300",
  "connector-missing": "border-red-700 text-red-800 dark:border-red-400 dark:text-red-300",
  "mapping-missing": "border-red-700 text-red-800 dark:border-red-400 dark:text-red-300",
  "source-inactive": "border-neutral-500 text-neutral-600 dark:border-neutral-500 dark:text-neutral-300",
};

function StatusPill({ status }: { status: SourceReadinessStatus }) {
  return (
    <span
      className={`inline-flex rounded border px-2 py-1 text-xs font-medium ${STATUS_CLASS[status]}`}
    >
      {status}
    </span>
  );
}

export default function SourceOpsPage() {
  const queue = buildSourceOpsQueue();

  return (
    <div className="min-h-screen bg-white text-neutral-900 dark:bg-neutral-950 dark:text-neutral-100">
      <SiteNav tagline="source operations" />
      <main className="mx-auto max-w-6xl space-y-10 px-4 py-12">
        <section className="space-y-4">
          <h1 className="text-4xl font-semibold tracking-tight">
            Source ops
          </h1>
          <p className="max-w-3xl text-neutral-700 dark:text-neutral-200">
            Static registry freshness and connector readiness for the source
            queue. This page reads local registry metadata and registered
            connector modules only; page render does not crawl source URLs.
          </p>
        </section>

        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <SummaryCell label="sources" value={queue.summary.total} />
          <SummaryCell label="ready" value={queue.summary.ready} />
          <SummaryCell label="review due" value={queue.summary.reviewDue} />
          <SummaryCell label="connector blocked" value={queue.summary.connectorBlocked} />
          <SummaryCell label="inactive" value={queue.summary.inactive} />
        </section>

        <section className="overflow-x-auto rounded border border-neutral-200 dark:border-neutral-800">
          <table className="min-w-full border-collapse text-left text-sm">
            <thead className="bg-neutral-50 text-xs uppercase text-neutral-500 dark:bg-neutral-900 dark:text-neutral-400">
              <tr>
                <th className="whitespace-nowrap px-4 py-3 font-medium">source</th>
                <th className="whitespace-nowrap px-4 py-3 font-medium">lane / type</th>
                <th className="whitespace-nowrap px-4 py-3 font-medium">cadence</th>
                <th className="whitespace-nowrap px-4 py-3 font-medium">freshness</th>
                <th className="whitespace-nowrap px-4 py-3 font-medium">connector</th>
                <th className="whitespace-nowrap px-4 py-3 font-medium">status</th>
              </tr>
            </thead>
            <tbody>
              {queue.rows.map((row) => (
                <tr
                  key={row.id}
                  className="border-t border-neutral-200 align-top dark:border-neutral-800"
                >
                  <td className="px-4 py-4">
                    <span className="block font-mono text-xs text-neutral-500">
                      {row.id}
                    </span>
                    <span className="mt-1 block font-medium">{row.name}</span>
                  </td>
                  <td className="px-4 py-4">
                    <span className="block">{row.lane}</span>
                    <span className="mt-1 block text-neutral-500">
                      {row.registryType}
                    </span>
                  </td>
                  <td className="px-4 py-4">
                    <span className="block">{row.cadence ?? "unknown"}</span>
                    <span className="mt-1 block text-neutral-500">
                      review {row.reviewFrequency ?? "unknown"}
                    </span>
                  </td>
                  <td className="px-4 py-4">
                    <span className="block">{row.freshnessLabel}</span>
                    <span className="mt-1 block text-neutral-500">
                      last {row.lastReviewed ?? "unknown"}
                    </span>
                  </td>
                  <td className="px-4 py-4">
                    <span className="block">{row.connectorType ?? "unmapped"}</span>
                    <span className="mt-1 block text-neutral-500">
                      {row.connectorVersion ?? "no connector"}
                    </span>
                  </td>
                  <td className="px-4 py-4">
                    <StatusPill status={row.readinessStatus} />
                    <span className="mt-2 block max-w-xs text-neutral-600 dark:text-neutral-300">
                      {row.readinessReason}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}

function SummaryCell({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded border border-neutral-200 p-4 dark:border-neutral-800">
      <div className="text-2xl font-semibold">{value}</div>
      <div className="mt-1 text-sm text-neutral-500">{label}</div>
    </div>
  );
}
