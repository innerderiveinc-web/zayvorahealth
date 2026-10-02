import type { Metadata } from "next";
import "./globals.css";
import { ErrorBoundary } from "@/components/ErrorBoundary";

export const metadata: Metadata = {
  title: "ZAYVORA Health OS™ — Ancient Wisdom. Modern Science. Intelligent Care.",
  description: "ZAYVORA Health OS™ is the digital healthcare operating system for ZAYVORA Health™ — integrating classical Unani medicine with modern biomedical intelligence, powered by Hakeem Sahab AI™.",
  manifest: "/manifest.json",
  themeColor: "#2D6A4F",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col">
        <ErrorBoundary>{children}</ErrorBoundary>
      </body>
    </html>
  );
}
