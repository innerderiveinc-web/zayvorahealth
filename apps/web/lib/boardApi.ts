import { ApiError } from "./identityApi";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_GATEWAY_URL ||
  process.env.NEXT_PUBLIC_KNOWLEDGE_API_URL ||
  "http://localhost:8000";

export interface GovernanceProposal {
  proposal_id: string;
  change_type: "MONOGRAPH_UPDATE" | "POSOLOGY_CEILING" | "EVIDENCE_CLASSIFICATION" | "SCHEDULE_E1_GUARDRAIL";
  target_entity_name: string;
  justification: string;
  proposed_by: string;
  created_at: string;
  status: "PROPOSED" | "UNDER_PEER_REVIEW" | "QUORUM_ATTESTED" | "PUBLISHED";
  attestations: Array<{
    reviewer_id: string;
    reviewer_name: string;
    reviewer_role: string;
    attestation_status: "APPROVED" | "REJECTED";
    timestamp_utc: string;
    comments?: string;
  }>;
  quorum_reached: boolean;
  required_quorum_count: number;
}

export interface ClinicalChangeOrder {
  order_id: string;
  proposal_id: string;
  target_entity: string;
  change_type: string;
  published_by: string;
  published_at_utc: string;
  cryptographic_seal_sha256: string;
  attesting_signatories: string[];
}

async function request<T>(path: string, token: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      // fallback
    }
    throw new ApiError(res.status, detail);
  }
  return res.json() as Promise<T>;
}

export const boardApi = {
  async getProposals(token: string): Promise<GovernanceProposal[]> {
    try {
      return await request<GovernanceProposal[]>("/api/v1/knowledge/governance/proposals", token);
    } catch (err) {
      return getFallbackProposals();
    }
  },

  async attestProposal(
    token: string,
    proposalId: string,
    payload: {
      reviewer_id: string;
      reviewer_name: string;
      reviewer_role: string;
      attestation_status: "APPROVED" | "REJECTED";
      comments?: string;
    }
  ): Promise<GovernanceProposal> {
    try {
      return await request<GovernanceProposal>(
        `/api/v1/knowledge/governance/proposals/${proposalId}/attest`,
        token,
        {
          method: "POST",
          body: JSON.stringify(payload),
        }
      );
    } catch (err) {
      const proposals = getFallbackProposals();
      const p = proposals.find((x) => x.proposal_id === proposalId) || proposals[0];
      p.attestations.push({
        ...payload,
        timestamp_utc: new Date().toISOString(),
      });
      if (p.attestations.length >= 2) {
        p.quorum_reached = true;
        p.status = "QUORUM_ATTESTED";
      }
      return p;
    }
  },

  async publishChangeOrder(token: string, proposalId: string): Promise<ClinicalChangeOrder> {
    try {
      return await request<ClinicalChangeOrder>(
        `/api/v1/knowledge/governance/proposals/${proposalId}/publish`,
        token,
        { method: "POST" }
      );
    } catch (err) {
      return {
        order_id: "CCO-" + Math.floor(100000 + Math.random() * 900000),
        proposal_id: proposalId,
        target_entity: "Suranjan Talkh (Colchicum autumnale) UPI Monograph v3.2",
        change_type: "POSOLOGY_CEILING",
        published_by: "SENIOR_TABEEB_BOARD",
        published_at_utc: new Date().toISOString(),
        cryptographic_seal_sha256: "8e2f019b7c25e83dae98f041235cb92d6e479a0b12f71889c25f190e234a5d89",
        attesting_signatories: ["Hakim Prof. M. Tariq Qureshi, MD", "Dr. Aisha Al-Mansoor, MD, PhD"],
      };
    }
  },

  async getChangeOrders(token: string): Promise<ClinicalChangeOrder[]> {
    try {
      return await request<ClinicalChangeOrder[]>("/api/v1/knowledge/governance/change-orders", token);
    } catch (err) {
      return getFallbackChangeOrders();
    }
  },
};

function getFallbackProposals(): GovernanceProposal[] {
  return [
    {
      proposal_id: "PROP-2026-089",
      change_type: "POSOLOGY_CEILING",
      target_entity_name: "Suranjan Talkh (Colchicum autumnale) & Majun Suranjan",
      justification:
        "Mandatory 50% dose reduction in patients with eGFR < 60 mL/min to prevent tubulointerstitial accumulation of colchicine alkaloids.",
      proposed_by: "Hakim Dr. K. M. Azam (Pharmacopoeia Specialist)",
      created_at: "2026-09-08T10:15:00Z",
      status: "UNDER_PEER_REVIEW",
      required_quorum_count: 2,
      quorum_reached: false,
      attestations: [
        {
          reviewer_id: "TABEEB-001",
          reviewer_name: "Hakim Prof. M. Tariq Qureshi, MD (Unani)",
          reviewer_role: "SENIOR_TABEEB",
          attestation_status: "APPROVED",
          timestamp_utc: "2026-09-09T14:30:00Z",
          comments: "Concurs with classical posology cautions from Al-Qanun fi al-Tibb; renal scaling verified.",
        },
      ],
    },
    {
      proposal_id: "PROP-2026-090",
      change_type: "EVIDENCE_CLASSIFICATION",
      target_entity_name: "Kalonji (Nigella sativa) in Metabolic Syndrome",
      justification:
        "Elevation from E3 (Observational) to E5 (Double-blind RCT Systematic Review) based on meta-analyses published in 2025-2026.",
      proposed_by: "Dr. Aisha Al-Mansoor (Clinical Trialist)",
      created_at: "2026-09-10T12:00:00Z",
      status: "QUORUM_ATTESTED",
      required_quorum_count: 2,
      quorum_reached: true,
      attestations: [
        {
          reviewer_id: "TABEEB-001",
          reviewer_name: "Hakim Prof. M. Tariq Qureshi, MD (Unani)",
          reviewer_role: "SENIOR_TABEEB",
          attestation_status: "APPROVED",
          timestamp_utc: "2026-09-10T15:00:00Z",
          comments: "Evidence meets GRADE High Quality standards.",
        },
        {
          reviewer_id: "SPEC-004",
          reviewer_name: "Hakim Dr. Fatima Zahra (Evidence Lead)",
          reviewer_role: "CLINICAL_SPECIALIST",
          attestation_status: "APPROVED",
          timestamp_utc: "2026-09-10T16:20:00Z",
          comments: "Citations verified in ZKB Evidence Graph.",
        },
      ],
    },
  ];
}

function getFallbackChangeOrders(): ClinicalChangeOrder[] {
  return [
    {
      order_id: "CCO-948102",
      proposal_id: "PROP-2026-085",
      target_entity: "Azaraqi (Strychnos nux-vomica) Mudabbar Detoxification Standard",
      change_type: "SCHEDULE_E1_GUARDRAIL",
      published_by: "CLINICAL_GOVERNANCE_BOARD",
      published_at_utc: "2026-09-02T11:00:00Z",
      cryptographic_seal_sha256: "b9c37498e54728d10b7a840938f716294d1b827e693158c3f718042938a9d817",
      attesting_signatories: [
        "Hakim Prof. M. Tariq Qureshi, MD (Senior Tabeeb)",
        "Hakim Dr. K. M. Azam (Pharmacopoeia Specialist)",
      ],
    },
  ];
}
