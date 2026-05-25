import Link from "next/link";

import { SiteFooter, SiteNav } from "@/components/SiteNav";
import { listBriefs } from "@/lib/briefs";
import { buildSubscriberOpsStatus } from "@/lib/subscriber-ops";

export const dynamic = "force-dynamic";

function StatusPill({ ready }: { ready: boolean }) {
  return (
    <span
      className={`rounded border px-2 py-1 text-xs font-medium ${
        ready
          ? "border-emerald-700 text-emerald-800 dark:border-emerald-400 dark:text-emerald-300"
          : "border-amber-700 text-amber-800 dark:border-amber-400 dark:text-amber-300"
      }`}
    >
      {ready ? "ready" : "blocked"}
    </span>
  );
}

export default function SubscriberOpsPage() {
  const status = buildSubscriberOpsStatus(listBriefs(), process.env);

  return (
    <div className="min-h-screen bg-white text-neutral-900 dark:bg-neutral-950 dark:text-neutral-100">
      <SiteNav tagline="subscriber operations" />
      <main className="mx-auto max-w-4xl space-y-10 px-4 py-12">
        <section className="space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <h1 className="text-4xl font-semibold tracking-tight">
              Subscriber ops
            </h1>
            <StatusPill ready={status.ready} />
          </div>
          <p className="max-w-2xl text-neutral-700 dark:text-neutral-200">
            Credential readiness, digest preview, and operator links for the
            weekly email surface. This page reports whether required keys are
            present without printing secret values.
          </p>
        </section>

        <section className="grid gap-4 md:grid-cols-2">
          <div className="rounded border border-neutral-200 p-5 dark:border-neutral-800">
            <h2 className="text-lg font-medium">Latest digest</h2>
            <dl className="mt-4 space-y-3 text-sm">
              <div>
                <dt className="text-neutral-500">Week</dt>
                <dd className="font-mono">{status.latest.week}</dd>
              </div>
              <div>
                <dt className="text-neutral-500">Subject</dt>
                <dd>{status.latest.subject}</dd>
              </div>
              <div>
                <dt className="text-neutral-500">Preview</dt>
                <dd>{status.latest.previewText}</dd>
              </div>
            </dl>
          </div>

          <div className="rounded border border-neutral-200 p-5 dark:border-neutral-800">
            <h2 className="text-lg font-medium">Configuration</h2>
            <ul className="mt-4 space-y-3 text-sm">
              {status.checks.map((check) => (
                <li
                  key={check.id}
                  className="flex items-start justify-between gap-3"
                >
                  <span>
                    <span className="block font-medium">{check.label}</span>
                    <span className="text-neutral-500">
                      {check.acceptedKeys.join(" or ")}
                    </span>
                  </span>
                  <StatusPill ready={check.configured} />
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-2">
          <div className="rounded border border-neutral-200 p-5 dark:border-neutral-800">
            <h2 className="text-lg font-medium">Operator links</h2>
            <ul className="mt-4 space-y-4 text-sm">
              {status.endpoints.map((endpoint) => (
                <li key={endpoint.href}>
                  <Link href={endpoint.href} className="font-medium hover:underline">
                    {endpoint.label}
                  </Link>
                  <p className="mt-1 text-neutral-600 dark:text-neutral-300">
                    {endpoint.purpose}
                  </p>
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded border border-neutral-200 p-5 dark:border-neutral-800">
            <h2 className="text-lg font-medium">Next actions</h2>
            <ul className="mt-4 list-disc space-y-2 pl-5 text-sm text-neutral-700 dark:text-neutral-200">
              {status.nextActions.map((action) => (
                <li key={action}>{action}</li>
              ))}
            </ul>
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
