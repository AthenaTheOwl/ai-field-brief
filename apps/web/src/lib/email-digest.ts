import type { BriefRecord } from "./briefs";
import { getBriefSummary, SITE_URL } from "./feeds";

const RESEND_API_BASE = "https://api.resend.com";

export interface DigestEmail {
  week: string;
  subject: string;
  previewText: string;
  html: string;
  text: string;
}

export interface EmailConfig {
  apiKey: string;
  segmentId: string;
  from: string;
}

export class EmailConfigError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "EmailConfigError";
  }
}

export class ResendRequestError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ResendRequestError";
    this.status = status;
  }
}

type FetchLike = typeof fetch;

function normalizeEmail(value: string): string {
  return value.trim().toLowerCase();
}

export function validateSubscriberEmail(value: string): string {
  const email = normalizeEmail(value);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    throw new Error("Enter a valid email address.");
  }
  return email;
}

export function readEmailConfig(
  env: Record<string, string | undefined>,
): EmailConfig {
  const apiKey = env.RESEND_API_KEY?.trim();
  const segmentId =
    env.RESEND_SEGMENT_ID?.trim() ?? env.RESEND_AUDIENCE_ID?.trim();
  const from =
    env.DIGEST_FROM_EMAIL?.trim() ?? env.RESEND_FROM_ADDRESS?.trim();

  const missing = [
    ["RESEND_API_KEY", apiKey],
    ["RESEND_SEGMENT_ID", segmentId],
    ["DIGEST_FROM_EMAIL", from],
  ]
    .filter(([, value]) => !value)
    .map(([name]) => name);

  if (missing.length > 0) {
    throw new EmailConfigError(
      `email digest is not configured; missing ${missing.join(", ")}`,
    );
  }

  return {
    apiKey: apiKey as string,
    segmentId: segmentId as string,
    from: from as string,
  };
}

function briefUrl(week: string): string {
  return `${SITE_URL}/briefs/${week}`;
}

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export function buildLatestDigestEmail(briefs: BriefRecord[]): DigestEmail {
  const latest = briefs[0];
  if (!latest) {
    throw new Error("no briefs available for digest email");
  }

  const summary = getBriefSummary(latest);
  const url = briefUrl(latest.week);
  const sourceCount =
    latest.meta?.sources_reviewed?.filter((source) => source.status === "ok")
      .length ?? 0;
  const itemCount =
    latest.meta?.sources_reviewed?.reduce(
      (sum, source) => sum + (source.items_included ?? 0),
      0,
    ) ?? 0;
  const sourceLine =
    sourceCount > 0
      ? `${sourceCount} sources swept, ${itemCount} items included.`
      : "Read the brief.";

  const subject = `ai-field-brief ${latest.week}: ${latest.title}`;
  const previewText = `${latest.title} - ${summary}`;
  const html = `<!doctype html>
<html>
  <body style="font-family:Arial,sans-serif;line-height:1.5;color:#171717;">
    <p style="font-size:12px;letter-spacing:0;text-transform:uppercase;color:#737373;">${escapeHtml(latest.week)}</p>
    <h1 style="font-size:24px;line-height:1.2;margin:0 0 16px;">${escapeHtml(latest.title)}</h1>
    <p>${escapeHtml(summary)}</p>
    <p>${escapeHtml(sourceLine)}</p>
    <p><a href="${escapeHtml(url)}">Read the brief</a></p>
    <hr style="border:none;border-top:1px solid #e5e5e5;margin:24px 0;" />
    <p style="font-size:12px;color:#737373;">
      You are receiving this because you subscribed to ai-field-brief.
      <a href="{{{RESEND_UNSUBSCRIBE_URL}}}">Unsubscribe</a>.
    </p>
  </body>
</html>`;

  const text = [
    `${latest.week}: ${latest.title}`,
    "",
    summary,
    "",
    sourceLine,
    "",
    `Read: ${url}`,
    "",
    "Unsubscribe: {{{RESEND_UNSUBSCRIBE_URL}}}",
  ].join("\n");

  return { week: latest.week, subject, previewText, html, text };
}

async function parseResendError(response: Response): Promise<string> {
  const text = await response.text();
  if (!text) {
    return `Resend returned HTTP ${response.status}`;
  }
  try {
    const body = JSON.parse(text) as { message?: string; error?: string };
    return body.message ?? body.error ?? text;
  } catch {
    return text;
  }
}

async function resendPost(
  path: string,
  payload: unknown,
  config: EmailConfig,
  fetchImpl: FetchLike,
): Promise<unknown> {
  const response = await fetchImpl(`${RESEND_API_BASE}${path}`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${config.apiKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new ResendRequestError(
      response.status,
      await parseResendError(response),
    );
  }

  return response.json();
}

export async function subscribeToDigest({
  email,
  env = process.env,
  fetchImpl = fetch,
}: {
  email: string;
  env?: Record<string, string | undefined>;
  fetchImpl?: FetchLike;
}): Promise<unknown> {
  const config = readEmailConfig(env);
  const normalizedEmail = validateSubscriberEmail(email);

  return resendPost(
    "/contacts",
    {
      email: normalizedEmail,
      unsubscribed: false,
      segments: [{ id: config.segmentId }],
      properties: {
        source: "ai-field-brief",
      },
    },
    config,
    fetchImpl,
  );
}

export async function sendDigestBroadcast({
  digest,
  env = process.env,
  fetchImpl = fetch,
}: {
  digest: DigestEmail;
  env?: Record<string, string | undefined>;
  fetchImpl?: FetchLike;
}): Promise<unknown> {
  const config = readEmailConfig(env);

  return resendPost(
    "/broadcasts",
    {
      segmentId: config.segmentId,
      from: config.from,
      subject: digest.subject,
      previewText: digest.previewText,
      html: digest.html,
      text: digest.text,
      name: `ai-field-brief ${digest.week}`,
      send: true,
    },
    config,
    fetchImpl,
  );
}

export function isAuthorizedCronRequest(
  request: Request,
  env: Record<string, string | undefined>,
): boolean {
  const secret = env.CRON_SECRET?.trim();
  if (!secret) {
    return false;
  }
  return request.headers.get("authorization") === `Bearer ${secret}`;
}
