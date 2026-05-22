import Link from "next/link";

export function SiteNav() {
  return (
    <header className="border-b border-neutral-200 dark:border-neutral-800">
      <nav className="mx-auto flex max-w-3xl items-center justify-between px-4 py-4">
        <Link href="/" className="text-base font-medium tracking-tight">
          ai-field-brief
        </Link>
        <ul className="flex gap-6 text-sm text-neutral-600 dark:text-neutral-300">
          <li>
            <Link href="/briefs" className="hover:underline">
              briefs
            </Link>
          </li>
          <li>
            <a
              href="https://github.com/AthenaTheOwl/ai-field-brief"
              className="hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              github
            </a>
          </li>
        </ul>
      </nav>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="mt-16 border-t border-neutral-200 dark:border-neutral-800">
      <div className="mx-auto max-w-3xl px-4 py-6 text-sm text-neutral-500">
        weekly AI digest with concrete moves. content CC BY 4.0 ·
        code Apache-2.0 ·
        {" "}
        <a
          href="https://github.com/AthenaTheOwl/ai-field-brief"
          className="hover:underline"
        >
          source
        </a>
      </div>
    </footer>
  );
}
