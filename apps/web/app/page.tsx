"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { identityApi, ApiError } from "@/lib/identityApi";
import { saveSession } from "@/lib/session";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [organizationSlug, setOrganizationSlug] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const session = await identityApi.login({ email, password, organization_slug: organizationSlug });
      saveSession(session);
      router.push("/dashboard");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.status === 429 ? "Too many attempts. Please wait and try again." : "Invalid credentials.");
      } else {
        setError("Could not reach the identity service. Is it running?");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex-1 flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <h1 className="zv-brand-title text-2xl mb-1">ZAYVORA</h1>
          <p className="text-sm" style={{ color: "var(--muted)" }}>
            Health Operating System — Clinician Sign In
          </p>
        </div>

        <form onSubmit={handleSubmit} className="zv-panel p-6 space-y-4">
          <div>
            <label className="zv-label" htmlFor="organizationSlug">
              Clinic ID
            </label>
            <input
              id="organizationSlug"
              className="zv-input"
              type="text"
              placeholder="your-clinic-slug"
              value={organizationSlug}
              onChange={(e) => setOrganizationSlug(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="zv-label" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              className="zv-input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="zv-label" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              className="zv-input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className="zv-error">{error}</p>}

          <button type="submit" className="zv-btn-primary w-full" disabled={loading}>
            {loading ? "Signing in..." : "Sign In"}
          </button>

          <p className="text-center text-sm" style={{ color: "var(--muted)" }}>
            New clinic?{" "}
            <Link href="/signup" className="underline" style={{ color: "var(--gold-soft)" }}>
              Register
            </Link>
          </p>
        </form>
      </div>
    </main>
  );
}
