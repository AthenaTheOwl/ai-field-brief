import { NextResponse } from "next/server";

import { listBriefs } from "@/lib/briefs";
import {
  buildLatestDigestEmail,
  isAuthorizedCronRequest,
  sendDigestBroadcast,
} from "@/lib/email-digest";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const dryRun = url.searchParams.get("dry_run") === "1";
  const digest = buildLatestDigestEmail(listBriefs());

  if (dryRun) {
    return NextResponse.json({
      ok: true,
      dry_run: true,
      week: digest.week,
      subject: digest.subject,
      preview_text: digest.previewText,
    });
  }

  if (!isAuthorizedCronRequest(request, process.env)) {
    return NextResponse.json(
      { ok: false, error: "missing or invalid cron authorization" },
      { status: 401 },
    );
  }

  const result = await sendDigestBroadcast({ digest });
  return NextResponse.json({ ok: true, week: digest.week, result });
}
