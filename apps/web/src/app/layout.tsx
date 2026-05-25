import type { Metadata } from "next";
import type { ReactNode } from "react";

import { ClerkProvider } from "@clerk/nextjs";

import { SITE_URL } from "../lib/feeds";
import "../styles/globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: "ai-field-brief",
  description: "Multi-tenant AI field-brief product (phase 1 scaffold)",
  alternates: {
    types: {
      "application/rss+xml": "/feed.xml",
      "application/atom+xml": "/atom.xml",
      "application/feed+json": "/feed.json",
    },
  },
};

interface RootLayoutProps {
  children: ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
