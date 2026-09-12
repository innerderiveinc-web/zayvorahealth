import { ApiError } from "./identityApi";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_GATEWAY_URL ||
  process.env.NEXT_PUBLIC_CLINICAL_API_URL ||
  "http://localhost:8000";

export interface PatientRecord {
  id: string;
  organization_id: string;
  mrn: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  phone: string;
  email: string;
  pregnancy_status: "pregnant" | "not_pregnant" | "unknown" | "not_applicable";
  comorbidities: string[];
  created_at: string;
}

export interface PatientCreatePayload {
  mrn: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  phone?: string;
  email?: string;
  pregnancy_status?: "pregnant" | "not_pregnant" | "unknown" | "not_applicable";
  comorbidities?: string[];
}

export interface TimelineEvent {
  event_type: "encounter" | "clinical_note" | "prescription" | "appointment";
  id: string;
  timestamp: string;
  summary: string;
  details: Record<string, unknown>;
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

export interface MizajAssessmentRecord {
  id: string;
  patient_id: string;
  encounter_id: string | null;
  assessed_by_user_id: string;
  primary_temperament: "Damwi" | "Safrawi" | "Balghami" | "Saudawi" | "Motadil";
  secondary_temperament: string;
  distribution_percentages: { Damwi: number; Safrawi: number; Balghami: number; Saudawi: number };
  su_e_mizaj: string;
  dyscrasia_degree: number;
  raw_scores: Record<string, number>;
  answers_json: Record<string, string>;
  created_at: string;
}

export interface DifferentialDiagnosis {
  score: number;
  unani_disease: string;
  urdu_name: string;
  icd11_code: string;
  icd11_title: string;
  snomed_concept_id: string;
  organ_axis: string;
  classical_asbab: string;
  usool_e_ilaj: string;
  red_flags: string[];
}

export const clinicalApi = {
  listPatients: (token: string) => request<PatientRecord[]>("/api/v1/patients", token),

  getPatient: (token: string, patientId: string) =>
    request<PatientRecord>(`/api/v1/patients/${patientId}`, token),

  createPatient: (token: string, payload: PatientCreatePayload) =>
    request<PatientRecord>("/api/v1/patients", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getTimeline: (token: string, patientId: string) =>
    request<TimelineEvent[]>(`/api/v1/patients/${patientId}/timeline`, token),

  createMizajAssessment: (
    token: string,
    patientId: string,
    answers: Record<string, string>,
    encounterId?: string
  ) =>
    request<MizajAssessmentRecord>(`/api/v1/patients/${patientId}/mizaj-assessment`, token, {
      method: "POST",
      body: JSON.stringify({ answers, encounter_id: encounterId }),
    }),

  getLatestMizajAssessment: (token: string, patientId: string) =>
    request<MizajAssessmentRecord>(`/api/v1/patients/${patientId}/mizaj-assessment/latest`, token),

  getDifferentialDiagnoses: (
    token: string,
    payload: { chief_complaint: string; organ_axis?: string; dominant_mizaj?: string }
  ) =>
    request<DifferentialDiagnosis[]>("/api/v1/diagnostics/differential", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  analyzeOrganAxis: (
    token: string,
    payload: {
      complaint: string;
      associated_symptoms?: string[];
      duration_days?: number;
      symptom_acuity?: "mild" | "moderate" | "severe";
      inflammatory_signs?: boolean;
      temperament_context?: Record<string, unknown>;
    }
  ) =>

    request<OrganAxisAnalysisResponse>("/api/v1/diagnostics/organ-axis/analyze", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getDigitalTwin: (token: string, patientId: string) =>
    request<DigitalTwinState>(`/api/v1/patients/${patientId}/digital-twin`, token),

  simulateDigitalTwinTrajectory: (
    token: string,
    patientId: string,
    payload: { dominant_humor?: string; treatment_modalities?: string[]; weeks?: number }
  ) =>
    request<DigitalTwinSimulationResponse>(`/api/v1/patients/${patientId}/digital-twin/simulate`, token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getDigitalTwinTrajectory: (token: string, patientId: string) =>
    request<DigitalTwinTrajectoryResponse>(`/api/v1/patients/${patientId}/digital-twin/trajectory`, token),
};

export interface DigitalTwinState {
  patient_id: string;
  timestamp: string;
  mizaj_state: {
    primary_temperament: string;
    heat_cold_deviation: number;
    wet_dry_deviation: number;
    drift_magnitude: number;
    clinical_status: string;
  };
  organ_axis_integrity: Record<string, number>;
  quwa_faculties: {
    quwwat_tabi_iyyah: number;
    quwwat_hayawaniyyah: number;
    quwwat_nafsaniyyah: number;
    tabiat_homeostatic_reserve: number;
  };
  overall_vitality_index: number;
  safe_to_lock: boolean;
}

export interface DigitalTwinSimulationResponse {
  simulation_metadata: {
    dominant_humor: string;
    concoction_protocol: { days: number; phase: string };
    active_modalities: string[];
    horizon_weeks: number;
    homeostatic_synergy_rate: number;
  };
  projected_milestones: Array<{
    week: number;
    projected_mean_organ_integrity: number;
    nujz_milestone_achieved: boolean;
    phase_description: string;
  }>;
  is_predictive_advisory: boolean;
  safe_to_lock: boolean;
}

export interface DigitalTwinTrajectoryResponse {
  trajectory_available: boolean;
  baseline_magnitude?: number;
  latest_magnitude?: number;
  net_drift_delta?: number;
  clinical_trend: string;
  evaluations_count?: number;
}


export interface OrganAxisInfo {
  id: string;
  name: string;
  governing_power?: string;
  primary_organ?: string;
  description?: string;
}

export interface ReflexArcInfo {
  id: string;
  name: string;
  primary_axis: string;
  reflex_axis: string;
  classical_mechanism: string;
  trigger_keywords: string[];
  clinical_presentation: string;
}

export interface OrganAxisAnalysisResponse {
  complaint: string;
  organ_axes: {
    primary_axis: OrganAxisInfo;
    secondary_axis?: OrganAxisInfo | null;
    reflex_sympathy_identified: boolean;
    detected_reflex_arcs: ReflexArcInfo[];
  };
  asbab_e_arbaa: {
    sabab_fail: string;
    sabab_maddi: string;
    sabab_suri: string;
    sabab_tamami: string;
  };
  dawr_e_marad: {
    stage: string;
    stage_code: string;
    clinical_state: string;
    usool_e_ilaj: string;
    therapeutic_priorities: string[];
  };
}

