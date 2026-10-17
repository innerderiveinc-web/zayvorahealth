"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { Suspense } from "react";

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const tokenFromUrl = searchParams.get("token") || "";
  
  const [token, setToken] = useState(tokenFromUrl);
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleReset(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters long.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://localhost:8088/api/v1/auth/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, new_password: password })
      });
      if (!response.ok) {
        throw new Error("Failed to reset password.");
      }
      router.push("/login?message=Password+reset+successful");
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <PublicWebsiteShell>
      <div className="min-h-[75vh] flex items-center justify-center py-16 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Create New Password
            </h1>
            <p className="mt-2 text-xs text-[#94A3B8]">
              Enter the reset token received via email and choose a strong, unique password.
            </p>
          </div>

          <div className="rounded-3xl bg-[#0D1527] border border-[#1E293B] p-8 shadow-2xl space-y-6">
            {success ? (
              <div className="text-center space-y-4">
                <div className="w-12 h-12 rounded-full bg-[#10B981]/20 border border-[#10B981] flex items-center justify-center mx-auto text-xl text-[#34D399]">
                  ✓
                </div>
                <h3 className="text-lg font-bold text-white">Password Updated</h3>
                <p className="text-xs text-[#94A3B8]">
                  Your credentials have been securely updated. You may now sign in with your new password.
                </p>
                <div className="pt-4">
                  <Link
                    href="/login"
                    className="block w-full py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#0F766E] text-white text-xs font-bold transition"
                  >
                    Proceed to Login →
                  </Link>
                </div>
              </div>
            ) : (
              <form onSubmit={handleReset} className="space-y-4">
                {error && (
                  <div className="p-3 rounded-xl bg-red-950/60 border border-red-800 text-red-200 text-xs">
                    {error}
                  </div>
                )}

                <div>
                  <label className="block text-xs font-semibold text-[#CBD5E1] mb-1">
                    Reset Token
                  </label>
                  <input
                    type="text"
                    required
                    value={token}
                    onChange={e => setToken(e.target.value)}
                    placeholder="e.g. TOK-98214"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#0A0F1D] border border-[#334155] text-white text-sm focus:outline-none focus:border-[#0D9488]"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-[#CBD5E1] mb-1">
                    New Password
                  </label>
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    placeholder="Min 8 characters"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#0A0F1D] border border-[#334155] text-white text-sm focus:outline-none focus:border-[#0D9488]"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-[#CBD5E1] mb-1">
                    Confirm New Password
                  </label>
                  <input
                    type="password"
                    required
                    value={confirmPassword}
                    onChange={e => setConfirmPassword(e.target.value)}
                    placeholder="Repeat password"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#0A0F1D] border border-[#334155] text-white text-sm focus:outline-none focus:border-[#0D9488]"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 rounded-xl bg-gradient-to-r from-[#0D9488] to-[#2D6A4F] text-white font-bold text-sm shadow-md hover:brightness-110 transition disabled:opacity-50 mt-2"
                >
                  {loading ? "Updating..." : "Update Password →"}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ResetPasswordForm />
    </Suspense>
  );
}
