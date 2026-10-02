import { ApiError } from "./identityApi";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_GATEWAY_URL ||
  process.env.NEXT_PUBLIC_KNOWLEDGE_API_URL ||
  "http://localhost:8000";

export interface MufradMonograph {
  id: string;
  name: string;
  botanical_name: string;
  part_used: string;
  synonyms: string[];
  afal: string[];
  mizaj: { temperament: string; quality: string; hc_degree?: number; wd_degree?: number };
  organ_axes: string[];
  traditional_uses: string;
  contraindications: string;
  musleh: string;
  badal: string;
  dose: string;
  is_schedule_e1: boolean;
  modern_pharmacology: string;
}

export interface ScheduleE1Substance {
  id: string;
  canonical_name: string;
  urdu_name: string;
  botanical_name: string;
  poison_class: string;
  mandatory_mudabbar: boolean;
  mudabbar_protocol: string;
  max_single_dose_mg: number;
  max_daily_dose_mg: number;
  statutory_warning: string;
}

export interface CompoundFormulation {
  id: string;
  name: string;
  urdu_name: string;
  category: string;
  classical_indication: string;
  dose: string;
  schedule_e1_warning: boolean;
  precautions: string;
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

export interface MufradNetwork {
  mufrad: MufradMonograph;
  mizaj?: { temperament: string; quality: string; hc_degree?: number; wd_degree?: number };
  axes: Array<{ code: string; name: string; translation: string }>;
  schedule_e1_profile?: ScheduleE1Substance | null;
  correctives: Array<{ target_drug: string; musleh_name: string; classical_role: string }>;
  substitutes: Array<{ original_drug: string; substitute_name: string; classical_role: string }>;
  contained_in_compounds?: Array<{ id: string; name: string; category: string }>;
  evidence?: Array<Record<string, unknown>>;
}

export interface GraphRagResponse {
  subgraph: {
    axes: Array<Record<string, unknown>>;
    mufradat: Array<Record<string, unknown>>;
    compounds: Array<Record<string, unknown>>;
    poisons: Array<Record<string, unknown>>;
  };
  rag_context_text: string;
}

export const knowledgeApi = {
  listMonographs: (token: string, search?: string) => {
    const query = search ? `?search=${encodeURIComponent(search)}` : "";
    return request<MufradMonograph[]>(`/api/v1/pharmacopoeia/monographs${query}`, token);
  },

  listScheduleE1: (token: string) =>
    request<ScheduleE1Substance[]>("/api/v1/pharmacopoeia/schedule-e1", token),

  listMaster350Catalog: (token: string) =>
    request<Array<Record<string, unknown>>>("/api/v1/knowledge/mufradat-250/all", token),

  getMonograph350Detail: (token: string, zmfId: string) =>
    request<Record<string, unknown>>(`/api/v1/knowledge/mufradat-250/${encodeURIComponent(zmfId)}`, token),

  listCompounds: (token: string) =>
    request<CompoundFormulation[]>("/api/v1/pharmacopoeia/compounds", token),

  getMufradNetwork: (token: string, nameOrId: string) =>
    request<MufradNetwork>(`/api/v1/graph/mufrad/${encodeURIComponent(nameOrId)}/network`, token),

  getCompoundNetwork: (token: string, nameOrId: string) =>
    request<Record<string, unknown>>(`/api/v1/graph/compounds/${encodeURIComponent(nameOrId)}/network`, token),

  getCorrectives: (token: string, mufradName: string) =>
    request<Array<{ target_drug: string; musleh_name: string; classical_role: string }>>(
      `/api/v1/graph/correctives/${encodeURIComponent(mufradName)}`,
      token
    ),

  getSubstitutes: (token: string, mufradName: string, axis?: string) => {
    const query = axis ? `?axis=${encodeURIComponent(axis)}` : "";
    return request<Array<{ original_drug: string; substitute_name: string; classical_role: string }>>(
      `/api/v1/graph/substitutes/${encodeURIComponent(mufradName)}${query}`,
      token
    );
  },

  getRagContext: (
    token: string,
    payload: { organ_axis?: string; symptoms?: string[]; temperament?: string }
  ) =>
    request<GraphRagResponse>("/api/v1/graph/rag-context", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  classifyStudy: (token: string, text: string) =>
    request<EvidenceClassifyResponse>("/api/v1/evidence/classify", token, {
      method: "POST",
      body: JSON.stringify({ text }),
    }),

  gradeEvidence: (token: string, payload: GRADEScoreRequest) =>
    request<GRADEScoreResponse>("/api/v1/evidence/grade", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  hybridSearch: (token: string, payload: HybridSearchRequest) =>
    request<HybridSearchResponse>("/api/v1/knowledge/rag/hybrid-search", token, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getRagStats: (token: string) =>
    request<Record<string, unknown>>("/api/v1/knowledge/rag/stats", token),
};

export interface HybridSearchRequest {
  query: string;
  organ_axis?: string;
  temperament?: string;
  top_k?: number;
  mode?: "rrf" | "weighted";
}

export interface HybridSearchItem {
  document_id: string;
  doc_type: string;
  title: string;
  content: string;
  score: number;
  is_schedule_e1: boolean;
  metadata: Record<string, unknown>;
}

export interface HybridSearchResponse {
  query: string;
  fusion_mode: string;
  count: number;
  results: HybridSearchItem[];
}


export interface EvidenceClassifyResponse {
  predicted_level: string;
  level_name: string;
  knowledge_world: string;
  study_type: string;
  confidence: number;
  requires_peer_review: boolean;
  peer_review_status: string;
  governance_note: string;
}

export interface GRADEScoreRequest {
  starting_level: string;
  risk_of_bias?: number;
  inconsistency?: number;
  indirectness?: number;
  imprecision?: number;
  publication_bias?: number;
  large_effect_size?: number;
  dose_response_gradient?: number;
}

export interface GRADEScoreResponse {
  starting_level: string;
  baseline_score: number;
  total_downgrades: number;
  total_upgrades: number;
  net_grade_score: number;
  grade_certainty: "HIGH" | "MODERATE" | "LOW" | "VERY_LOW";
  evaluation_notes: string[];
}

