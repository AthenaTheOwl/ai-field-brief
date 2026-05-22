import type { ReactNode } from "react";
import { SiteFooter, SiteNav } from "../../components/SiteNav";

export default function BriefsLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-white text-neutral-900 dark:bg-neutral-950 dark:text-neutral-100">
      <SiteNav />
      <main className="mx-auto max-w-3xl px-4 py-10">{children}</main>
      <SiteFooter />
    </div>
  );
}
