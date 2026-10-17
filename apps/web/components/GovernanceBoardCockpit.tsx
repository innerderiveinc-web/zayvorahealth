"use client";

import React, { useState, useEffect } from "react";
import {
  boardApi,
  type GovernanceProposal,
  type ClinicalChangeOrder,
} from "@/lib/boardApi";

interface GovernanceBoardCockpitProps {
  token: string;
}

export function GovernanceBoardCockpit({ token }: GovernanceBoardCockpitProps) {
  const [proposals, setProposals] = useState<GovernanceProposal[]>([]);
  const [changeOrders, setChangeOrders] = useState<ClinicalChangeOrder[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeActionId, setActiveActionId] = useState<string | null>(null);

  // Clinician Signer Info
  const [reviewerId, setReviewerId] = useState("TABEEB-007");
  const [reviewerName, setReviewerName] = useState("Hakim Dr. K. M. Azam");
  const [reviewerRole, setReviewerRole] = useState("SENIOR_TABEEB");
  const [comments, setComments] = useState("Reviewed against UPI Vol 1 posology standards; approved.");

  useEffect(() => {
    loadData();
  }, [token]);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [p, c] = await Promise.all([
        boardApi.getProposals(token),
        boardApi.getChangeOrders(token),
      ]);
      setProposals(p);
      setChangeOrders(c);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAttest = async (proposalId: string) => {
    setActiveActionId(proposalId);
    try {
      await boardApi.attestProposal(token, proposalId, {
        reviewer_id: reviewerId,
        reviewer_name: reviewerName,
        reviewer_role: reviewerRole,
        attestation_status: "APPROVED",
        comments,
      });
      await loadData();
    } catch (err) {
      console.error(err);
    } finally {
      setActiveActionId(null);
    }
  };

  const handlePublish = async (proposalId: string) => {
    setActiveActionId(proposalId);
    try {
      await boardApi.publishChangeOrder(token, proposalId);
      await loadData();
    } catch (err) {
      console.error(err);
    } finally {
      setActiveActionId(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="zv-panel p-5 bg-[#121712] border border-[#24302a] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xl">🏛️</span>
            <h2 className="text-base font-serif font-semibold text-[#e3c884]">
              Clinical Governance Board & Monograph Ratification
            </h2>
            <span className="px-2 py-0.5 text-[10px] font-mono rounded-full bg-[#182a1d] text-[#2ea87f] border border-[#2ea87f]/40">
              Quorum Mandatory (≥2 Senior Tabeebs)
            </span>
          </div>
          <p className="text-xs text-[#8a9490] mt-1">
            Governs official pharmacopoeial monographs, Schedule E(1) statutory limits, and posology ceilings with immutable SHA-256 seals.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 text-xs font-mono rounded bg-[#18231d] text-[#2ea87f] border border-[#2ea87f]/40">
            21 CFR Part 11 + AYUSH Compliant
          </span>
        </div>
      </div>

      {/* Reviewer Role Bar */}
      <div className="zv-panel p-4 bg-[#141b15] flex flex-wrap items-center justify-between gap-4 text-xs">
        <div className="flex items-center gap-3">
          <span className="text-[#8a9490]">Active Board Signatory:</span>
          <span className="font-semibold text-[#ece8dd]">{reviewerName}</span>
          <span className="px-2 py-0.5 rounded text-[10px] bg-[#223528] text-[#2ea87f] font-mono">
            {reviewerRole}
          </span>
          <span className="text-[#8a9490]">({reviewerId})</span>
        </div>
        <div className="text-[11px] text-[#8a9490]">
          Quorum Rule: Minimum 2 independent clinical specialists required to seal changes.
        </div>
      </div>

      {/* Proposals Section */}
      <div className="space-y-4">
        <h3 className="text-sm font-serif font-semibold text-[#e3c884] uppercase tracking-wider flex items-center gap-2">
          <span>📝</span> Pending Monograph & Posology Proposals ({proposals.length})
        </h3>

        <div className="space-y-4">
          {proposals.map((prop) => (
            <div
              key={prop.proposal_id}
              className="zv-panel p-5 bg-[#121712] border border-[#24302a] space-y-3"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#24302a] pb-3">
                <div>
                  <span className="px-2 py-0.5 text-[10px] font-mono rounded bg-[#1f2821] text-[#e3c884] border border-[#e3c884]/30 mr-2">
                    {prop.proposal_id}
                  </span>
                  <span className="text-sm font-semibold text-[#ece8dd]">{prop.target_entity_name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-[#1a2b1f] text-[#2ea87f]">
                    {prop.change_type}
                  </span>
                  <span
                    className={`px-2 py-0.5 text-xs font-semibold rounded ${
                      prop.status === "PUBLISHED"
                        ? "bg-[#182a1d] text-[#2ea87f]"
                        : prop.quorum_reached
                        ? "bg-[#332815] text-[#e3c884]"
                        : "bg-[#252422] text-[#8a9490]"
                    }`}
                  >
                    {prop.status}
                  </span>
                </div>
              </div>

              <p className="text-xs text-[#ece8dd] leading-relaxed">
                <strong className="text-[#8a9490]">Clinical Justification:</strong> {prop.justification}
              </p>

              <div className="text-xs text-[#8a9490] flex flex-wrap items-center gap-4">
                <span>Proposed By: <strong className="text-[#ece8dd]">{prop.proposed_by}</strong></span>
                <span>Date: {new Date(prop.created_at).toLocaleDateString()}</span>
                <span>
                  Quorum Status:{" "}
                  <strong className={prop.quorum_reached ? "text-[#2ea87f]" : "text-[#e06c75]"}>
                    {prop.attestations.length} / {prop.required_quorum_count} Attestations
                  </strong>
                </span>
              </div>

              {/* Attestation Signatures List */}
              {prop.attestations.length > 0 && (
                <div className="p-3 bg-[#0e1410] rounded border border-[#1e2922] space-y-1.5 text-xs">
                  <span className="text-[11px] text-[#8a9490] block font-semibold">
                    Attesting Specialists:
                  </span>
                  {prop.attestations.map((att, idx) => (
                    <div key={idx} className="flex items-center justify-between text-[#ece8dd]">
                      <div className="flex items-center gap-2">
                        <span className="text-[#2ea87f]">✓</span>
                        <span>{att.reviewer_name}</span>
                        <span className="text-[10px] text-[#8a9490] font-mono">({att.reviewer_role})</span>
                      </div>
                      <span className="text-[10px] text-[#8a9490]">
                        {new Date(att.timestamp_utc).toLocaleString()}
                      </span>
                    </div>
                  ))}
                </div>
              )}

              {/* Actions */}
              <div className="flex items-center gap-3 pt-2">
                {!prop.quorum_reached && (
                  <button
                    onClick={() => handleAttest(prop.proposal_id)}
                    disabled={activeActionId === prop.proposal_id}
                    className="zv-btn-primary py-1.5 px-4 text-xs font-semibold cursor-pointer"
                  >
                    {activeActionId === prop.proposal_id ? "Attesting..." : "✍️ Attest as Senior Tabeeb"}
                  </button>
                )}

                {prop.quorum_reached && prop.status !== "PUBLISHED" && (
                  <button
                    onClick={() => handlePublish(prop.proposal_id)}
                    disabled={activeActionId === prop.proposal_id}
                    className="py-1.5 px-4 text-xs font-semibold rounded bg-[#332815] text-[#e3c884] hover:bg-[#47391e] border border-[#e3c884]/40 transition cursor-pointer"
                  >
                    {activeActionId === prop.proposal_id
                      ? "Publishing..."
                      : "🔒 Publish Cryptographic Change Order"}
                  </button>
                )}

                {prop.status === "PUBLISHED" && (
                  <span className="text-xs text-[#2ea87f] font-semibold flex items-center gap-1.5">
                    <span>✓</span> Published & Ratified into ZKB 2.0
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Published Clinical Change Orders (Audit Trail) */}
      <div className="space-y-4">
        <h3 className="text-sm font-serif font-semibold text-[#e3c884] uppercase tracking-wider flex items-center gap-2">
          <span>📜</span> Cryptographically Sealed Change Orders ({changeOrders.length})
        </h3>

        <div className="space-y-3">
          {changeOrders.map((co) => (
            <div
              key={co.order_id}
              className="zv-panel p-4 bg-[#111712] border border-[#2ea87f]/30 space-y-2 text-xs"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-[#e3c884] font-bold">{co.order_id}</span>
                  <span className="font-medium text-[#ece8dd]">{co.target_entity}</span>
                </div>
                <span className="text-[11px] text-[#8a9490]">
                  Published: {new Date(co.published_at_utc).toLocaleString()}
                </span>
              </div>

              <div className="font-mono text-[11px] text-[#8a9490] break-all bg-[#0a0e0b] p-2 rounded border border-[#1a231d]">
                <strong className="text-[#2ea87f]">SHA-256 Seal:</strong> {co.cryptographic_seal_sha256}
              </div>

              <div className="text-[11px] text-[#8a9490]">
                Signatories: <strong className="text-[#ece8dd]">{co.attesting_signatories.join(", ")}</strong>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
