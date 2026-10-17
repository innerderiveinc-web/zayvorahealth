import { ApiError } from "./identityApi";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_GATEWAY_URL ||
  process.env.NEXT_PUBLIC_AI_API_URL ||
  "http://localhost:8000";

export interface HakeemConsultRequest {
  patient_id: string;
  chief_complaint: string;
  organ_axis?: string;
}

export interface HakeemConsultOut {
  id: string;
  patient_id: string;
  chief_complaint: string;
  organ_axis: string;
  candidate_mufradat: Array<Record<string, unknown>>;
  raw_response: string;
  parsed_sections: Record<string, string>;
  is_valid: boolean;
  missing_sections: string[];
  reviewed_by_clinician: boolean;
  converted_to_nuskha_draft_id: string | null;
  created_at: string;
}

export interface MarkReviewedPayload {
  converted_to_nuskha_draft_id?: string;
}

export interface HakeemRefineRequest {
  consultation_id: string;
  clinician_feedback: string;
}

export interface HakeemRefineOut {
  consultation_id: string;
  valid: boolean;
  missing_sections: string[];
  raw_response: string;
  sections: Record<string, string>;
  clinician_feedback_applied: string;
  zape_personalization: Record<string, unknown>;
  requires_clinician_review: boolean;
}

export interface ZAPEPersonalizeRequest {
  patient_context: Record<string, unknown>;
  candidate_drugs?: Array<Record<string, unknown>>;
  season?: string;
}

export interface ZAPEPersonalizeResponse {
  posology: {
    posology_scaling_factor: number;
    category: string;
    formula_applied: string;
    warnings: string[];
  };
  temperament_modulation: {
    temperament: string;
    constitutional_modulations: string[];
    musleh_recommendations: string[];
    contraindicated_classes: string[];
  };
  seasonal_modulation: {
    season_identified: string;
    seasonal_guidance: string;
    seasonal_caution: string;
  };
  overall_summary: string;
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

export const hakeemApi = {
  consult: (token: string, payload: HakeemConsultRequest) =>
    request<HakeemConsultOut>("/api/v1/hakeem/consult", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getConsultation: (token: string, consultationId: string) =>
    request<HakeemConsultOut>(`/api/v1/hakeem/consultations/${consultationId}`, token),

  listConsultationsForPatient: (token: string, patientId: string) =>
    request<HakeemConsultOut[]>(`/api/v1/hakeem/consultations/by-patient/${patientId}`, token),

  markReviewed: (token: string, consultationId: string, payload: MarkReviewedPayload = {}) =>
    request<HakeemConsultOut>(`/api/v1/hakeem/consultations/${consultationId}/mark-reviewed`, token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  refineConsultation: (token: string, payload: HakeemRefineRequest) =>
    request<HakeemRefineOut>("/api/v1/hakeem/refine", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  personalize: (token: string, payload: ZAPEPersonalizeRequest) =>
    request<ZAPEPersonalizeResponse>("/api/v1/hakeem/personalize", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};

