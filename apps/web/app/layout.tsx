import type { Metadata } from "next";
import "./globals.css";
import { ErrorBoundary } from "@/components/ErrorBoundary";

export const metadata: Metadata = {
  title: "ZAYVORA Health OS",
  description: "AI-Native Integrative Healthcare Operating System",
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
