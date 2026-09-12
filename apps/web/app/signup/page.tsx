"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { identityApi, ApiError } from "@/lib/identityApi";
import { saveSession } from "@/lib/session";

function slugify(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

export default function SignupPage() {
  const router = useRouter();
  const [clinicName, setClinicName] = useState("");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    const slug = slugify(clinicName);
    try {
      await identityApi.createOrganization({ name: clinicName, slug, tier: "clinic" });
      const session = await identityApi.signup({
        email,
        full_name: fullName,
        password,
        organization_slug: slug,
        role_name: "Owner",
      });
      saveSession(session);
      router.push("/dashboard");
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.status === 409) setError("A clinic with this name is already registered.");
        else if (err.status === 422) setError(err.message || "Please check your details and try again.");
        else setError(err.message);
      } else {
        setError("Could not reach the identity service. Is it running?");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex-1 flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <h1 className="zv-brand-title text-2xl mb-1">ZAYVORA</h1>
          <p className="text-sm" style={{ color: "var(--muted)" }}>
            Register Your Clinic
          </p>
        </div>

        <form onSubmit={handleSubmit} className="zv-panel p-6 space-y-4">
          <div>
            <label className="zv-label" htmlFor="clinicName">
              Clinic name
            </label>
            <input
              id="clinicName"
              className="zv-input"
              type="text"
              placeholder="e.g. Ashraf Unani Clinic"
              value={clinicName}
              onChange={(e) => setClinicName(e.target.value)}
              required
            />
            {clinicName && (
              <p className="text-xs mt-1" style={{ color: "var(--muted)" }}>
                Clinic ID: {slugify(clinicName) || "—"}
              </p>
            )}
          </div>
          <div>
            <label className="zv-label" htmlFor="fullName">
              Your full name
            </label>
            <input
              id="fullName"
              className="zv-input"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
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
              Password (min 12 characters)
            </label>
            <input
              id="password"
              className="zv-input"
              type="password"
              minLength={12}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className="zv-error">{error}</p>}

          <button type="submit" className="zv-btn-primary w-full" disabled={loading}>
            {loading ? "Creating clinic..." : "Create Clinic & Sign In"}
          </button>

          <p className="text-center text-sm" style={{ color: "var(--muted)" }}>
            Already registered?{" "}
            <Link href="/" className="underline" style={{ color: "var(--gold-soft)" }}>
              Sign in
            </Link>
          </p>
        </form>
      </div>
    </main>
  );
}
