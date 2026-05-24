const TRACKING_KEYS = new Set(["gclid", "fbclid", "mc_cid", "mc_eid"]);

export function canonicalizeUrl(input: string): string {
  const url = new URL(input);
  url.hash = "";
  url.hostname = url.hostname.toLowerCase();

  const kept = Array.from(url.searchParams.entries())
    .filter(([key]) => {
      const normalized = key.toLowerCase();
      return !normalized.startsWith("utm_") && !TRACKING_KEYS.has(normalized);
    })
    .sort(([left], [right]) => left.localeCompare(right));

  url.search = "";
  for (const [key, value] of kept) {
    url.searchParams.append(key, value);
  }

  if (url.pathname !== "/" && url.pathname.endsWith("/")) {
    url.pathname = url.pathname.slice(0, -1);
  }

  return url.toString();
}
