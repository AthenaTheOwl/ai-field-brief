import { listBriefs } from "../../lib/briefs";
import { buildAtomFeed } from "../../lib/feeds";

export const dynamic = "force-static";
export const revalidate = false;

export function GET() {
  return new Response(buildAtomFeed(listBriefs()), {
    headers: {
      "Content-Type": "application/atom+xml; charset=utf-8",
    },
  });
}
