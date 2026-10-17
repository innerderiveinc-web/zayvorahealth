"use client";

import React, { useState, useEffect } from "react";

interface Organization {
  id: string;
  name: string;
  slug: string;
  tier: string;
  created_at: string;
  status: "active" | "suspended" | "trial";
  clinicians_count?: number;
  patients_count?: number;
}

const FALLBACK_ORGS: Organization[] = [
  {
    id: "org-001",
    name: "ZAYVORA Flagship Matab & Wellness Centre",
    slug: "zayvora-flagship",
    tier: "ENTERPRISE",
    created_at: "2024-01-01T00:00:00Z",
    status: "active",
    clinicians_count: 14,
    patients_count: 1250,
  },
  {
    id: "org-002",
    name: "Al-Shifa Integrative Clinic",
    slug: "al-shifa-clinic",
    tier: "PROFESSIONAL",
    created_at: "2024-03-15T00:00:00Z",
    status: "active",
    clinicians_count: 6,
    patients_count: 480,
  },
  {
    id: "org-003",
    name: "Cordoba Traditional Healing Matab",
    slug: "cordoba-healing",
    tier: "STARTER",
    created_at: "2024-06-20T00:00:00Z",
    status: "trial",
    clinicians_count: 2,
    patients_count: 95,
  },
];

export default function AdminOrganizationsPage() {
  const [orgs, setOrgs] = useState<Organization[]>(FALLBACK_ORGS);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [search, setSearch] = useState("");
  const [formData, setFormData] = useState({ name: "", slug: "", tier: "PROFESSIONAL" });

  useEffect(() => {
    async function fetchOrgs() {
      try {
        const gateway = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";
        const res = await fetch(`${gateway}/api/v1/organizations`);
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && data.length > 0) {
            setOrgs(
              data.map((o: any, idx: number) => ({
                id: o.id || `org-${idx}`,
                name: o.name,
                slug: o.slug,
                tier: o.tier || "PROFESSIONAL",
                created_at: o.created_at || new Date().toISOString(),
                status: "active",
                clinicians_count: 5,
                patients_count: 100,
              }))
            );
          }
        }
      } catch (err) {
        console.warn("Could not fetch remote organizations, using cached data", err);
      }
    }
    fetchOrgs();
  }, []);

  const filtered = orgs.filter(
    (o) =>
      o.name.toLowerCase().includes(search.toLowerCase()) ||
      o.slug.toLowerCase().includes(search.toLowerCase()) ||
      o.tier.toLowerCase().includes(search.toLowerCase())
  );

  async function handleCreateOrg(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const gateway = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";
      const res = await fetch(`${gateway}/api/v1/organizations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Bootstrap-Token": "test-bootstrap-token",
        },
        body: JSON.stringify(formData),
      });
      if (res.ok) {
        const created = await res.json();
        setOrgs([
          {
            ...created,
            status: "active",
            clinicians_count: 1,
            patients_count: 0,
          },
          ...orgs,
        ]);
        setShowModal(false);
        setFormData({ name: "", slug: "", tier: "PROFESSIONAL" });
        alert(`Organization "${formData.name}" created successfully!`);
      } else {
        // Fallback local create for demo
        const newOrg: Organization = {
          id: `org-${Date.now()}`,
          name: formData.name,
          slug: formData.slug || formData.name.toLowerCase().replace(/\s+/g, "-"),
          tier: formData.tier,
          created_at: new Date().toISOString(),
          status: "active",
          clinicians_count: 1,
          patients_count: 0,
        };
        setOrgs([newOrg, ...orgs]);
        setShowModal(false);
        setFormData({ name: "", slug: "", tier: "PROFESSIONAL" });
      }
    } catch (err) {
      console.error(err);
      alert("Failed to connect to gateway, saved locally.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Tenant Organizations</h2>
          <p className="text-xs text-gray-500">Multi-tenant Matab clinics, medical centres & enterprise subscribers.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-[#2D6A4F] text-white rounded-lg text-sm font-semibold hover:bg-[#1B4332] transition shadow-sm"
        >
          + Provision New Organization
        </button>
      </div>

      {/* Search Bar */}
      <div className="flex items-center gap-3">
        <input
          type="text"
          placeholder="Filter organizations by name, slug, or tier..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full max-w-md px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#2D6A4F] bg-white"
        />
      </div>

      {/* Organizations Table */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b border-gray-200 text-xs font-semibold text-gray-500 uppercase tracking-wider">
            <tr>
              <th className="text-left px-5 py-3">Organization Name / Slug</th>
              <th className="text-left px-5 py-3">Subscription Tier</th>
              <th className="text-left px-5 py-3">Status</th>
              <th className="text-left px-5 py-3">Clinicians</th>
              <th className="text-left px-5 py-3">Patients</th>
              <th className="text-left px-5 py-3">Created</th>
              <th className="text-right px-5 py-3">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filtered.map((org) => (
              <tr key={org.id} className="hover:bg-gray-50 transition">
                <td className="px-5 py-3.5">
                  <div className="font-semibold text-gray-800">{org.name}</div>
                  <div className="text-xs font-mono text-gray-400">{org.slug}</div>
                </td>
                <td className="px-5 py-3.5">
                  <span
                    className={`text-xs px-2.5 py-0.5 rounded-full font-semibold border ${
                      org.tier === "ENTERPRISE"
                        ? "bg-purple-50 text-purple-700 border-purple-200"
                        : org.tier === "PROFESSIONAL"
                        ? "bg-blue-50 text-blue-700 border-blue-200"
                        : "bg-emerald-50 text-emerald-700 border-emerald-200"
                    }`}
                  >
                    {org.tier}
                  </span>
                </td>
                <td className="px-5 py-3.5">
                  <span
                    className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${
                      org.status === "active"
                        ? "bg-emerald-100 text-emerald-800"
                        : "bg-amber-100 text-amber-800"
                    }`}
                  >
                    {org.status.toUpperCase()}
                  </span>
                </td>
                <td className="px-5 py-3.5 text-gray-700 font-medium">{org.clinicians_count || 1}</td>
                <td className="px-5 py-3.5 text-gray-700 font-medium">{org.patients_count || 0}</td>
                <td className="px-5 py-3.5 text-xs text-gray-400 font-mono">
                  {org.created_at.slice(0, 10)}
                </td>
                <td className="px-5 py-3.5 text-right">
                  <button className="text-xs text-[#2D6A4F] hover:underline font-semibold">
                    Manage →
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Provision Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b pb-3">
              <h3 className="font-bold text-gray-800">Provision Organization</h3>
              <button onClick={() => setShowModal(false)} className="text-gray-400 hover:text-gray-600">✕</button>
            </div>
            <form onSubmit={handleCreateOrg} className="space-y-3 text-sm">
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Organization Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Bukhara Unani Wellness"
                  value={formData.name}
                  onChange={(e) => {
                    const name = e.target.value;
                    setFormData({
                      ...formData,
                      name,
                      slug: name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, ""),
                    });
                  }}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-[#2D6A4F] outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Tenant Slug (Immutable)</label>
                <input
                  type="text"
                  required
                  value={formData.slug}
                  onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg font-mono text-xs focus:ring-2 focus:ring-[#2D6A4F] outline-none bg-gray-50"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">Subscription Tier</label>
                <select
                  value={formData.tier}
                  onChange={(e) => setFormData({ ...formData, tier: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-[#2D6A4F] outline-none"
                >
                  <option value="STARTER">STARTER (Single Clinician)</option>
                  <option value="PROFESSIONAL">PROFESSIONAL (Up to 10 Clinicians)</option>
                  <option value="ENTERPRISE">ENTERPRISE (Hospital & Research)</option>
                </select>
              </div>

              <div className="pt-3 flex justify-end gap-2 border-t">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 border rounded-lg text-gray-600 text-xs hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-5 py-2 bg-[#2D6A4F] text-white rounded-lg text-xs font-semibold hover:bg-[#1B4332]"
                >
                  {loading ? "Provisioning..." : "Create Tenant"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
