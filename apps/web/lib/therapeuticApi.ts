import { ApiError } from "./identityApi";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_GATEWAY_URL ||
  process.env.NEXT_PUBLIC_THERAPEUTIC_API_URL ||
  "http://localhost:8000";

export interface NuskhaIngredientInput {
  name: string;
  mufrad_id?: string;
  afal?: string;
  miqdaar?: string;
  musleh?: string;
  badal?: string;
  is_mudabbar?: boolean;
  mudabbar_process?: string;
  dose_mg?: number;
  mizaj_temperament?: string;
  mizaj_degree_hc?: number;
  mizaj_degree_wd?: number;
}

export interface PatientSafetyContext {
  age?: number;
  pregnancy_status?: "pregnant" | "not_pregnant" | "unknown" | "not_applicable";
  lactation_status?: "yes" | "no";
  allergies?: string[];
  current_medications?: string[];
  comorbidities?: string[];
  chief_complaint?: string;
}

export interface NuskhaCompileRequest {
  target_organ_axes: string[];
  therapeutic_objective: string;
  patient_safety_context: PatientSafetyContext;
  ingredients: NuskhaIngredientInput[];
}

export interface CompiledIngredient {
  name: string;
  classical_role: string;
  target_axis_alignment: string;
  prescribed_dose_mg: number;
  clinically_adjusted_dose_mg: number;
  posology_adjustments: string[];
  musleh: string;
  badal: string;
  is_mudabbar?: boolean;
  mudabbar_process: string;
}

export interface NuskhaCompileResponse {
  status: string;
  juz_e_azam: string | null;
  target_organ_axes: string[];
  therapeutic_objective: string;
  is_formulation_balanced: boolean;
  missing_musleh_alerts: string[];
  substitute_suggestions: Array<{ for_ingredient: string; classical_badal: string; reason: string }>;
  compiled_ingredients: CompiledIngredient[];
}

export interface NuskhaDraftOut {
  id: string;
  patient_id: string;
  encounter_id: string;
  mizaj_context: Record<string, unknown>;
  asbab: string;
  tashkhis: string;
  organ_axis_context: string[];
  usool_e_ilaj: string;
  therapeutic_objective: string;
  ingredients: NuskhaIngredientInput[];
  dosage_form: string;
  dose: string;
  timing: string;
  duration: string;
  parhez: string;
  safety_verdict: "SAFE_TO_CONSIDER" | "CAUTION" | "MODIFY" | "DO_NOT_RECOMMEND" | "REFER";
  safety_reasons: string[];
  status: "draft" | "approved" | "rejected";
  reviewed_by_user_id?: string;
  reviewed_at?: string;
  rejection_reason?: string;
  safety_override_justification?: string;
  created_at: string;
}

export interface TadbeerPlanCreatePayload {
  patient_id: string;
  encounter_id: string;
  patient_safety_context?: PatientSafetyContext;
  name: string;
  category: "regimen" | "rest" | "physical_activity" | "massage" | "bathing" | "other";
  indication?: string;
  method?: string;
  frequency?: string;
  duration?: string;
  contraindications?: string;
  practitioner_requirements?: string;
}

export interface TadbeerPlanOut {
  id: string;
  patient_id: string;
  encounter_id: string;
  name: string;
  category: string;
  indication: string;
  method: string;
  frequency: string;
  duration: string;
  contraindications: string;
  practitioner_requirements: string;
  safety_verdict: string;
  safety_reasons: string[];
  status: string;
  created_at: string;
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

export const therapeuticApi = {
  compileNuskha: (token: string, payload: NuskhaCompileRequest) =>
    request<NuskhaCompileResponse>("/api/v1/nuskha-drafts/compile", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  createNuskhaDraft: (token: string, payload: Record<string, unknown>) =>
    request<NuskhaDraftOut>("/api/v1/nuskha-drafts", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  listDraftsForPatient: (token: string, patientId: string) =>
    request<NuskhaDraftOut[]>(`/api/v1/nuskha-drafts/by-patient/${patientId}`, token),

  approveDraft: (token: string, draftId: string, safetyOverrideJustification = "") =>
    request<NuskhaDraftOut>(`/api/v1/nuskha-drafts/${draftId}/approve`, token, {
      method: "POST",
      body: JSON.stringify({ safety_override_justification: safetyOverrideJustification }),
    }),

  rejectDraft: (token: string, draftId: string, reason: string) =>
    request<NuskhaDraftOut>(`/api/v1/nuskha-drafts/${draftId}/reject`, token, {
      method: "POST",
      body: JSON.stringify({ rejection_reason: reason }),
    }),

  createTadbeerPlan: (token: string, payload: TadbeerPlanCreatePayload) =>
    request<TadbeerPlanOut>("/api/v1/tadbeer-plans", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  listTadbeerPlansForPatient: (token: string, patientId: string) =>
    request<TadbeerPlanOut[]>(`/api/v1/tadbeer-plans/by-patient/${patientId}`, token),

  createCarePlan: (token: string, payload: CarePlanCreatePayload) =>
    request<UnifiedCarePlanOut>("/api/v1/care-plans", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  listCarePlansForPatient: (token: string, patientId: string) =>
    request<UnifiedCarePlanOut[]>(`/api/v1/care-plans/patient/${patientId}`, token),

  getCarePlan: (token: string, planId: string) =>
    request<UnifiedCarePlanOut>(`/api/v1/care-plans/${planId}`, token),

  signCarePlan: (token: string, planId: string, registrationNumber: string) =>
    request<UnifiedCarePlanOut>(`/api/v1/care-plans/${planId}/sign`, token, {
      method: "POST",
      body: JSON.stringify({
        clinician_registration_number: registrationNumber,
        statutory_affirmation: true,
      }),
    }),

  evaluatePharmacovigilance: (token: string, payload: ADRReportPayload) =>
    request<WHOUMCResultOut>("/api/v1/care-plans/pharmacovigilance/evaluate", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  createInventoryBatch: (token: string, payload: InventoryBatchCreatePayload) =>
    request<InventoryBatchOut>("/api/v1/dispensary/batches", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  listInventoryBatches: (token: string, medicationName?: string) => {
    const query = medicationName ? `?medication_name=${encodeURIComponent(medicationName)}` : "";
    return request<InventoryBatchOut[]>(`/api/v1/dispensary/batches${query}`, token);
  },

  dispensePrescription: (token: string, payload: DispenseRequestPayload) =>
    request<DispenseRecordOut[]>("/api/v1/dispensary/dispense", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  recallBatch: (token: string, batchId: string, payload: { reason: string; recall_class?: string }) =>
    request<BatchRecallOut>(`/api/v1/dispensary/batches/${batchId}/recall`, token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};

export interface InventoryBatchCreatePayload {
  medication_name: string;
  formulation_type?: string;
  batch_number: string;
  manufacturer?: string;
  manufacturing_date: string;
  expiry_date: string;
  initial_quantity: number;
  unit?: string;
  is_schedule_e1?: boolean;
  mudabbar_certified?: boolean;
  mudabbar_certificate_number?: string;
}

export interface InventoryBatchOut {
  id: string;
  organization_id: string;
  medication_name: string;
  formulation_type: string;
  batch_number: string;
  manufacturer: string;
  manufacturing_date: string;
  expiry_date: string;
  initial_quantity: number;
  available_quantity: number;
  unit: string;
  is_schedule_e1: boolean;
  mudabbar_certified: boolean;
  mudabbar_certificate_number?: string | null;
  qc_release_status: string;
  created_at: string;
}

export interface DispenseRequestPayload {
  prescription_id: string;
  patient_id: string;
  medication_name: string;
  quantity_requested: number;
  is_schedule_e1?: boolean;
  pharmacist_license_number: string;
  patient_counseling_notes?: string;
}

export interface DispenseRecordOut {
  id: string;
  organization_id: string;
  prescription_id: string;
  patient_id: string;
  batch_id: string;
  batch_number: string;
  quantity_dispensed: number;
  dispensed_by_pharmacist_id: string;
  pharmacist_license_number: string;
  patient_counseling_notes: string;
  mudabbar_verified_at_dispense: boolean;
  dispensed_at: string;
}

export interface BatchRecallOut {
  batch_number: string;
  medication_name: string;
  previous_status: string;
  new_status: string;
  recall_class: string;
  reason: string;
  recalled_by_user_id: string;
  recalled_at: string;
  action_required: string;
}


export interface AsbabSittah {
  hawa_muheet: string;
  makool_mashroob: string;
  harkat_sukoon_badani: string;
  harkat_sukoon_nafsani: string;
  naum_yaqzah: string;
  istifragh_ihtibas: string;
}

export interface UnifiedCarePlanOut {
  id: string;
  patient_id: string;
  encounter_id: string;
  created_by_user_id: string;
  title: string;
  horizon: "acute" | "stabilization" | "maintenance";
  duration_days: number;
  mizaj_context: Record<string, unknown>;
  usool_e_ilaj: string;
  primary_indication: string;
  ilaj_bid_dawa: Array<Record<string, unknown>>;
  ilaj_bit_tadbeer: Array<Record<string, unknown>>;
  ilaj_bil_ghiza: Record<string, unknown>;
  asbab_sittah: AsbabSittah;
  review_milestones: Array<Record<string, unknown>>;
  prognosis_notes: string;
  safe_to_lock: boolean;
  signed_by_clinician_id?: string | null;
  clinician_registration_number: string;
  signed_at?: string | null;
  status: "draft" | "active" | "completed" | "discontinued";
  created_at: string;
  updated_at: string;
}

export interface CarePlanCreatePayload {
  patient_id: string;
  encounter_id: string;
  title: string;
  horizon?: "acute" | "stabilization" | "maintenance";
  duration_days?: number;
  mizaj_context?: Record<string, unknown>;
  usool_e_ilaj?: string;
  primary_indication?: string;
  ilaj_bid_dawa?: Array<Record<string, unknown>>;
  ilaj_bit_tadbeer?: Array<Record<string, unknown>>;
  ilaj_bil_ghiza?: Record<string, unknown>;
  asbab_sittah?: Partial<AsbabSittah>;
  review_milestones?: Array<Record<string, unknown>>;
  prognosis_notes?: string;
}

export interface ADRReportPayload {
  patient_id: string;
  suspected_agent: string;
  batch_number?: string;
  adverse_reaction_description: string;
  latency_hours?: number;
  dechallenge_performed?: boolean;
  dechallenge_outcome?: "improved" | "no_change" | "worsened" | "unknown";
  rechallenge_performed?: boolean;
  rechallenge_outcome?: "positive" | "negative" | "not_applicable";
  concomitant_drugs?: string[];
  alternative_etiologies_considered?: string[];
  is_schedule_e1_substance?: boolean;
  verified_mudabbar_protocol_followed?: boolean;
}

export interface WHOUMCResultOut {
  causality_category: string;
  causality_score: number;
  rationale: string;
  statutory_warning?: string | null;
  regulatory_action_required: boolean;
  recommendations: string[];
}

