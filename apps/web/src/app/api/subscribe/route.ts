import { NextResponse } from "next/server";

import {
  EmailConfigError,
  ResendRequestError,
  subscribeToDigest,
} from "@/lib/email-digest";

export const dynamic = "force-dynamic";

function htmlResponse(message: string, status = 200): Response {
  return new Response(
    `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>ai-field-brief subscription</title>
  </head>
  <body style="font-family:Arial,sans-serif;line-height:1.5;max-width:42rem;margin:3rem auto;padding:0 1rem;">
    <h1>ai-field-brief</h1>
    <p>${message}</p>
    <p><a href="/">Back to the brief</a></p>
  </body>
</html>`,
    {
      status,
      headers: { "content-type": "text/html; charset=utf-8" },
    },
  );
}

function wantsHtml(request: Request): boolean {
  const contentType = request.headers.get("content-type") ?? "";
  return contentType.includes("application/x-www-form-urlencoded");
}

async function readEmail(request: Request): Promise<string> {
  const contentType = request.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) {
    const body = (await request.json()) as { email?: unknown };
    return typeof body.email === "string" ? body.email : "";
  }
  const form = await request.formData();
  const value = form.get("email");
  return typeof value === "string" ? value : "";
}

export async function POST(request: Request) {
  const html = wantsHtml(request);

  try {
    const email = await readEmail(request);
    await subscribeToDigest({ email });

    if (html) {
      return htmlResponse("You're on the weekly digest list.");
    }

    return NextResponse.json({ ok: true });
  } catch (error) {
    const status =
      error instanceof EmailConfigError
        ? 503
        : error instanceof ResendRequestError
          ? error.status
          : 400;
    const message =
      error instanceof Error ? error.message : "Subscription failed.";

    if (html) {
      return htmlResponse(message, status);
    }

    return NextResponse.json({ ok: false, error: message }, { status });
  }
}
