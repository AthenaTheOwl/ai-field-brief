import type { Metadata } from "next";
import type { ReactNode } from "react";

import { ClerkProvider } from "@clerk/nextjs";

import "../styles/globals.css";

export const metadata: Metadata = {
  title: "ai-field-brief",
  description: "Multi-tenant AI field-brief product (phase 1 scaffold)",
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
