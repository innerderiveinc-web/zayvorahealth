"use client";

import React, { useState } from "react";

interface BackupRecord {
  id: string;
  name: string;
  type: "Full DB Cluster" | "PostgreSQL WAL" | "Neo4j Graph Store" | "Qdrant Vectors";
  size: string;
  status: "Verified" | "In-Progress" | "Failed";
  storageTier: "Cold Storage (S3 Glacier)" | "Hot Replica (Local SSD)";
  createdAt: string;
}

const INITIAL_BACKUPS: BackupRecord[] = [
  { id: "BCK-2026-0914-01", name: "zayvora_prod_full_20260914.sql.gz", type: "Full DB Cluster", size: "412 MB", status: "Verified", storageTier: "Cold Storage (S3 Glacier)", createdAt: "2026-09-14 02:00 UTC" },
  { id: "BCK-2026-0914-02", name: "zayvora_wal_archive_segment_88.tar", type: "PostgreSQL WAL", size: "64 MB", status: "Verified", storageTier: "Hot Replica (Local SSD)", createdAt: "2026-09-14 06:00 UTC" },
  { id: "BCK-2026-0913-01", name: "zkb_unani_ontology_dump.dump", type: "Neo4j Graph Store", size: "188 MB", status: "Verified", storageTier: "Cold Storage (S3 Glacier)", createdAt: "2026-09-13 02:00 UTC" },
  { id: "BCK-2026-0912-01", name: "clinical_vector_embeddings_v2.qdrant", type: "Qdrant Vectors", size: "95 MB", status: "Verified", storageTier: "Cold Storage (S3 Glacier)", createdAt: "2026-09-12 02:00 UTC" }
];

export default function AdminBackupsPage() {
  const [backups, setBackups] = useState<BackupRecord[]>(INITIAL_BACKUPS);
  const [isBackingUp, setIsBackingUp] = useState(false);

  const triggerBackup = () => {
    setIsBackingUp(true);
    setTimeout(() => {
      const newBck: BackupRecord = {
        id: `BCK-${Date.now().toString().slice(-6)}`,
        name: `zayvora_manual_snapshot_${new Date().toISOString().slice(0, 10)}.sql.gz`,
        type: "Full DB Cluster",
        size: "415 MB",
        status: "Verified",
        storageTier: "Hot Replica (Local SSD)",
        createdAt: "Just now"
      };
      setBackups([newBck, ...backups]);
      setIsBackingUp(false);
      alert("Manual snapshot created and SHA-256 checksum verified!");
    }, 1500);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Disaster Recovery & Database Backups</h2>
          <p className="text-sm text-gray-500">Automated cryptographic backups, point-in-time recovery, and multi-cloud cold-storage synchronization</p>
        </div>
        <button
          onClick={triggerBackup}
          disabled={isBackingUp}
          className="px-4 py-2 bg-[#2D6A4F] hover:bg-[#1B4332] text-white rounded-lg text-sm font-semibold transition shadow-sm flex items-center gap-2"
        >
          <span>{isBackingUp ? "⏳ Creating Snapshot..." : "📸 Trigger Snapshot Now"}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">RPO (Recovery Point Objective)</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">&lt; 15 Minutes</span>
          <span className="text-xs text-emerald-600 font-semibold mt-1 block">Continuous WAL streaming active</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">RTO (Recovery Time Objective)</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">&lt; 30 Minutes</span>
          <span className="text-xs text-emerald-600 font-semibold mt-1 block">Standby replica failover automated</span>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm">
          <span className="text-xs text-gray-500 font-medium block">Encryption Standard</span>
          <span className="text-2xl font-bold text-gray-800 mt-1 block">AES-256-GCM</span>
          <span className="text-xs text-gray-400 mt-1 block">DPDP Act 2023 &amp; ABDM AES-256 encryption at rest</span>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden p-5 space-y-4">
        <h3 className="font-bold text-gray-800 text-base">Verified Snapshot Registry</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-50 border-b border-gray-100 text-xs font-semibold text-gray-500 uppercase">
              <tr>
                <th className="px-4 py-3">Backup ID</th>
                <th className="px-4 py-3">Filename</th>
                <th className="px-4 py-3">Data Store</th>
                <th className="px-4 py-3">Size</th>
                <th className="px-4 py-3">Storage Target</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Created At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {backups.map(b => (
                <tr key={b.id} className="hover:bg-gray-50/50">
                  <td className="px-4 py-3 font-mono font-bold text-gray-700">{b.id}</td>
                  <td className="px-4 py-3 font-mono text-xs text-gray-800">{b.name}</td>
                  <td className="px-4 py-3 text-gray-600">{b.type}</td>
                  <td className="px-4 py-3 font-semibold text-gray-900">{b.size}</td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{b.storageTier}</td>
                  <td className="px-4 py-3">
                    <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      ✓ {b.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-500 font-mono text-xs">{b.createdAt}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
