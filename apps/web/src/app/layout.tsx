import type { Metadata } from "next";
import type { ReactNode } from "react";

import { ClerkProvider } from "@clerk/nextjs";

import { hasLiveClerkConfig } from "../lib/env";
import { SITE_URL } from "../lib/feeds";
import "../styles/globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: "ai-field-brief",
  description: "A weekly AI systems brief built from source evidence and concrete actions.",
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
  const document = (
    <html lang="en">
      <body>{children}</body>
    </html>
  );

  return hasLiveClerkConfig(process.env) ? (
    <ClerkProvider>{document}</ClerkProvider>
  ) : (
    document
  );
}
