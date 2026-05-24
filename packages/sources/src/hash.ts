import { createHash } from "node:crypto";

export interface ContentHashInput {
  readonly title: string;
  readonly canonicalUrl: string;
  readonly body?: string | null;
}

export function contentHash(input: ContentHashInput): string {
  return createHash("sha256")
    .update(`${input.title}\n${input.canonicalUrl}\n${input.body ?? ""}`, "utf8")
    .digest("hex");
}
