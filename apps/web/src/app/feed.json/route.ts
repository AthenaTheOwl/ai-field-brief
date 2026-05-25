import { listBriefs } from "../../lib/briefs";
import { buildJsonFeed } from "../../lib/feeds";

export const dynamic = "force-static";
export const revalidate = false;

export function GET() {
  return new Response(buildJsonFeed(listBriefs()), {
    headers: {
      "Content-Type": "application/feed+json; charset=utf-8",
    },
  });
}
