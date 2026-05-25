import type { BriefRecord } from "./briefs";
import { buildLatestDigestEmail } from "./email-digest";

type Env = Record<string, string | undefined>;

export interface SubscriberOpsCheck {
  id: string;
  label: string;
  configured: boolean;
  acceptedKeys: string[];
}

export interface SubscriberOpsStatus {
  ready: boolean;
  latest: {
    week: string;
    subject: string;
    previewText: string;
  };
  checks: SubscriberOpsCheck[];
  endpoints: Array<{
    label: string;
    href: string;
    purpose: string;
  }>;
  nextActions: string[];
}

function hasAny(env: Env, keys: string[]): boolean {
  return keys.some((key) => Boolean(env[key]?.trim()));
}

export function buildSubscriberOpsStatus(
  briefs: BriefRecord[],
  env: Env,
): SubscriberOpsStatus {
  const digest = buildLatestDigestEmail(briefs);
  const checks: SubscriberOpsCheck[] = [
    {
      id: "resend-api-key",
      label: "Resend API key",
      configured: hasAny(env, ["RESEND_API_KEY"]),
      acceptedKeys: ["RESEND_API_KEY"],
    },
    {
      id: "resend-segment",
      label: "Resend segment",
      configured: hasAny(env, ["RESEND_SEGMENT_ID", "RESEND_AUDIENCE_ID"]),
      acceptedKeys: ["RESEND_SEGMENT_ID", "RESEND_AUDIENCE_ID"],
    },
    {
      id: "digest-from-email",
      label: "Digest sender",
      configured: hasAny(env, ["DIGEST_FROM_EMAIL", "RESEND_FROM_ADDRESS"]),
      acceptedKeys: ["DIGEST_FROM_EMAIL", "RESEND_FROM_ADDRESS"],
    },
    {
      id: "cron-secret",
      label: "Cron bearer secret",
      configured: hasAny(env, ["CRON_SECRET"]),
      acceptedKeys: ["CRON_SECRET"],
    },
  ];
  const missing = checks.filter((check) => !check.configured);

  return {
    ready: missing.length === 0,
    latest: {
      week: digest.week,
      subject: digest.subject,
      previewText: digest.previewText,
    },
    checks,
    endpoints: [
      {
        label: "Subscriber capture",
        href: "/api/subscribe",
        purpose: "POST email addresses into the configured Resend segment.",
      },
      {
        label: "Digest dry run",
        href: "/api/cron/weekly-digest?dry_run=1",
        purpose: "Preview the next broadcast without sending email.",
      },
      {
        label: "RSS feed",
        href: "/feed.xml",
        purpose: "Public fallback for readers who do not want email.",
      },
      {
        label: "JSON Feed",
        href: "/feed.json",
        purpose: "Machine-readable archive for feed clients and agents.",
      },
      {
        label: "Source ops",
        href: "/ops/sources",
        purpose: "Inspect registry freshness and connector readiness.",
      },
    ],
    nextActions:
      missing.length === 0
        ? [
            "Run the dry-run endpoint before Friday.",
            "Check the latest subject and preview text.",
            "Let Vercel cron send the weekly broadcast.",
          ]
        : missing.map(
            (check) =>
              `Set ${check.acceptedKeys.join(" or ")} before sends can run.`,
          ),
  };
}
