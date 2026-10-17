import { ApiError } from "./identityApi";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_GATEWAY_URL ||
  process.env.NEXT_PUBLIC_CLINICAL_API_URL ||
  "http://localhost:8000";

export interface SOAPNote {
  note_id: string;
  patient_id: string;
  session_id: string;
  created_at: string;
  detected_languages: string[];
  subjective: {
    chief_complaints: string[];
    colloquial_findings: Array<{
      colloquial_phrase: string;
      unani_pathology: string;
      organ_system: string;
    }>;
    raw_dialogue_excerpt: string;
    asbab_sittah_zarooriyyah: Record<string, string>;
  };
  objective: {
    vitals: Record<string, string>;
    nabz_examination: Record<string, string>;
    lisan_examination: Record<string, string>;
    baul_o_baraz: Record<string, string>;
  };
  assessment: {
    dominant_mizaj: string;
    secondary_mizaj: string;
    primary_unani_diagnosis: string;
    dawr_e_marad: string;
    quwa_status: string;
  };
  plan: {
    ilaj_bil_ghiza: string[];
    ilaj_bil_tadbeer: string[];
    ilaj_bil_dawa: string[];
    follow_up: string;
    statutory_notice: string;
  };
  safe_to_lock: boolean;
  status: string;
  signed_by?: string;
  signed_at?: string;
  clinician_notes?: string;
}

export interface ProcessTranscriptPayload {
  patient_id: string;
  transcript: string;
  session_id?: string;
  vitals?: Record<string, any>;
}

export interface ClinicianSignOffPayload {
  note_id: string;
  clinician_id: string;
  clinician_name: string;
  clinician_role: string;
  clinical_amendments?: Record<string, any>;
  clinician_notes?: string;
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

export const scribeApi = {
  async processTranscript(token: string, payload: ProcessTranscriptPayload): Promise<SOAPNote> {
    return request<SOAPNote>("/api/v1/scribe/process-transcript", token, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async signAndLockNote(token: string, payload: ClinicianSignOffPayload): Promise<SOAPNote> {
    return request<SOAPNote>("/api/v1/scribe/sign-and-lock", token, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  async getNote(token: string, noteId: string): Promise<SOAPNote> {
    return request<SOAPNote>(`/api/v1/scribe/notes/${noteId}`, token);
  },
};
