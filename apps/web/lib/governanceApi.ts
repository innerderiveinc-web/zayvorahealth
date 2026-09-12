import { ApiError } from "./identityApi";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_GATEWAY_URL ||
  process.env.NEXT_PUBLIC_CLINICAL_API_URL ||
  "http://localhost:8000";

export interface AuditVerificationOut {
  is_valid: boolean;
  total_blocks: number;
  genesis_hash: string;
  latest_block_hash: string;
  tampered_block_index: number | null;
  verification_message: string;
}

export interface Part11SignatureOut {
  signature_id: string;
  signer_name: string;
  signer_id: string;
  signer_role: string;
  timestamp_utc: string;
  signature_meaning: string;
  document_content_hash: string;
  cryptographic_seal: string;
}

export interface RegulatoryBundleOut {
  bundle_id: string;
  resource_id: string;
  regulatory_standard: string;
  export_timestamp_utc: string;
  chain_integrity: {
    is_valid: boolean;
    total_blocks: number;
    latest_block_hash: string;
    certificate: string;
  };
  provenance_blocks: Array<{
    index: number;
    timestamp_utc: string;
    actor_id: string;
    action: string;
    diff_hash: string;
    block_hash: string;
  }>;
  registered_signatures: Array<{
    signature_id: string;
    signer_name: string;
    signer_role: string;
    timestamp_utc: string;
    meaning: string;
    seal: string;
  }>;
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

export const governanceApi = {
  async verifyChain(token: string): Promise<AuditVerificationOut> {
    return request<AuditVerificationOut>("/api/v1/governance/audit/verify", token);
  },

  async signDocument(
    token: string,
    payload: {
      signer_id: string;
      signer_name: string;
      signer_role: string;
      document_payload: Record<string, any>;
      signature_meaning?: string;
    }
  ): Promise<Part11SignatureOut> {
    return request<Part11SignatureOut>("/api/v1/governance/signatures/sign", token, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async exportBundle(token: string, resourceId: string): Promise<RegulatoryBundleOut> {
    return request<RegulatoryBundleOut>(`/api/v1/governance/regulatory-bundle/${resourceId}`, token);
  },
};
