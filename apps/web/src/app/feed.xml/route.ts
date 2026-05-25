import { listBriefs } from "../../lib/briefs";
import { buildRssFeed } from "../../lib/feeds";

export const dynamic = "force-static";
export const revalidate = false;

export function GET() {
  return new Response(buildRssFeed(listBriefs()), {
    headers: {
      "Content-Type": "application/rss+xml; charset=utf-8",
    },
  });
}
