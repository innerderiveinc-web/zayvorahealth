import { ApiError } from "./identityApi";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_GATEWAY_URL ||
  process.env.NEXT_PUBLIC_CLINICAL_API_URL ||
  "http://localhost:8000";

export interface DoseSlot {
  slot_name: "MORNING" | "NOON" | "EVENING" | "BEDTIME";
  scheduled_time: string;
  items: Array<{
    item_type: "dawa" | "tadbeer" | "ghiza";
    item_id: string;
    display_name: string;
    dosage_and_form: string;
    anupan_vehicle: string;
    instructions: string;
    adherence_status: "PENDING" | "TAKEN" | "MISSED" | "SKIPPED";
  }>;
}

export interface TodaySchedule {
  patient_id: string;
  schedule_date: string;
  slots: DoseSlot[];
  overall_7d_adherence_pct: number;
  dietary_guidelines: string[];
}

export interface PortalMessage {
  message_id: string;
  patient_id: string;
  sender_type: "PATIENT" | "CLINICIAN" | "SYSTEM";
  timestamp_utc: string;
  message_body: string;
  triage_status: "ROUTINE" | "ELEVATED" | "EMERGENCY_REDIRECT";
  requires_immediate_action: boolean;
}

export interface VoiceSynthesizeResponse {
  patient_id: string;
  language: string;
  language_name: string;
  script_text: string;
  transliteration: string;
  audio_format: string;
  audio_data_uri: string;
  audio_duration_seconds: number;
  clinical_verification_hash: string;
  safety_note: string;
  bhashini_pipeline?: {
    source_language: string;
    target_language: string;
    engine: string;
    voice_gender: string;
    status: string;
  };
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

export const portalApi = {
  async getTodaySchedule(token: string, patientId: string): Promise<TodaySchedule> {
    try {
      return await request<TodaySchedule>(`/api/v1/patient-portal/${patientId}/today`, token);
    } catch (err) {
      if (process.env.NEXT_PUBLIC_DEMO_MODE === "true") {
        return getFallbackTodaySchedule(patientId);
      }
      throw err;
    }
  },

  async logAdherence(
    token: string,
    payload: {
      patient_id: string;
      item_type: string;
      item_id: string;
      timing_slot: string;
      status: "TAKEN" | "MISSED" | "SKIPPED";
      reason?: string;
    }
  ): Promise<{ recorded: boolean; compliance_pct: number }> {
    try {
      return await request<{ recorded: boolean; compliance_pct: number }>(
        "/api/v1/patient-portal/adherence",
        token,
        {
          method: "POST",
          body: JSON.stringify(payload),
        }
      );
    } catch (err) {
      if (process.env.NEXT_PUBLIC_DEMO_MODE === "true") {
        return { recorded: true, compliance_pct: 92.5 };
      }
      throw err;
    }
  },

  async getMessages(token: string, patientId: string): Promise<PortalMessage[]> {
    try {
      return await request<PortalMessage[]>(`/api/v1/patient-portal/${patientId}/messages`, token);
    } catch (err) {
      if (process.env.NEXT_PUBLIC_DEMO_MODE === "true") {
        return getFallbackMessages(patientId);
      }
      throw err;
    }
  },

  async sendMessage(
    token: string,
    payload: {
      patient_id: string;
      sender_type: "PATIENT" | "CLINICIAN";
      message_body: string;
    }
  ): Promise<PortalMessage> {
    try {
      return await request<PortalMessage>("/api/v1/patient-portal/messages/send", token, {
        method: "POST",
        body: JSON.stringify(payload),
      });
    } catch (err) {
      if (process.env.NEXT_PUBLIC_DEMO_MODE === "true") {
        const isEmergency =
          payload.message_body.toLowerCase().includes("chest pain") ||
          payload.message_body.toLowerCase().includes("severe");
        return {
          message_id: "msg-" + Date.now(),
          patient_id: payload.patient_id,
          sender_type: payload.sender_type,
          timestamp_utc: new Date().toISOString(),
          message_body: payload.message_body,
          triage_status: isEmergency ? "EMERGENCY_REDIRECT" : "ROUTINE",
          requires_immediate_action: isEmergency,
        };
      }
      throw err;
    }
  },

  async synthesizeMedicationVoice(
    token: string,
    payload: {
      patient_id: string;
      medication_name?: string;
      dosage_display?: string;
      timing_slot?: string;
      intake_vehicle?: string;
      language?: string;
      dose_id?: string;
    }
  ): Promise<VoiceSynthesizeResponse> {
    try {
      return await request<VoiceSynthesizeResponse>(
        "/api/v1/patient-portal/voice/synthesize",
        token,
        {
          method: "POST",
          body: JSON.stringify(payload),
        }
      );
    } catch (err) {
      if (process.env.NEXT_PUBLIC_DEMO_MODE === "true") {
        return {
          patient_id: payload.patient_id,
          language: payload.language || "ur",
          language_name: "Urdu (Roman Transliteration)",
          script_text: `Mohtaram Mareez! Aap ki tajweez kardah dawa ${payload.medication_name || "Jawarish"} nahar munh lein.`,
          transliteration: `Dear Patient! Please take ${payload.medication_name || "medication"} as prescribed.`,
          audio_format: "audio/wav;codec=pcm_16",
          audio_data_uri: "data:audio/wav;base64,UklGRjIAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",
          audio_duration_seconds: 1.5,
          clinical_verification_hash: "mock-hash-4592",
          safety_note: "Verified clinical voice instruction.",
          bhashini_pipeline: {
            source_language: "en",
            target_language: payload.language || "ur",
            engine: "Bhashini-Indic-TTS-v2",
            voice_gender: "female",
            status: "SYNTHESIZED_SUCCESS",
          },
        };
      }
      throw err;
    }
  },
};

function getFallbackTodaySchedule(patientId: string): TodaySchedule {
  return {
    patient_id: patientId,
    schedule_date: new Date().toISOString().split("T")[0],
    overall_7d_adherence_pct: 94.2,
    slots: [
      {
        slot_name: "MORNING",
        scheduled_time: "07:30 AM",
        items: [
          {
            item_type: "dawa",
            item_id: "med-001",
            display_name: "Majun Suranjan (Mudabbar)",
            dosage_and_form: "5 grams (Majun paste)",
            anupan_vehicle: "Aab-e-Badiyan (Fennel hydrosol) 50 mL lukewarm",
            instructions: "Take 30 minutes before breakfast; avoid cold water.",
            adherence_status: "TAKEN",
          },
          {
            item_type: "ghiza",
            item_id: "ghiza-001",
            display_name: "Harira-e-Badam with saffron",
            dosage_and_form: "1 warm bowl",
            anupan_vehicle: "Warm skimmed milk",
            instructions: "Nourishing breakfast to fortify Hararat-e-Ghariziyyah.",
            adherence_status: "TAKEN",
          },
        ],
      },
      {
        slot_name: "NOON",
        scheduled_time: "01:30 PM",
        items: [
          {
            item_type: "dawa",
            item_id: "med-002",
            display_name: "Sharbat Buzuri Motadil",
            dosage_and_form: "20 mL syrup",
            anupan_vehicle: "Diluted with 100 mL lukewarm water",
            instructions: "Diuretic & hepatic cooler; drink after light meal.",
            adherence_status: "PENDING",
          },
        ],
      },
      {
        slot_name: "EVENING",
        scheduled_time: "06:00 PM",
        items: [
          {
            item_type: "tadbeer",
            item_id: "tadb-001",
            display_name: "Dalak-e-Layyin (Gentle Effleurage)",
            dosage_and_form: "20 minutes session",
            anupan_vehicle: "Roghan-e-Surkh (Warm herbal oil)",
            instructions: "Apply along lumbosacral region and lower limbs.",
            adherence_status: "PENDING",
          },
        ],
      },
      {
        slot_name: "BEDTIME",
        scheduled_time: "10:00 PM",
        items: [
          {
            item_type: "dawa",
            item_id: "med-003",
            display_name: "Itrifal Ustukhuddus",
            dosage_and_form: "6 grams",
            anupan_vehicle: "100 mL warm water",
            instructions: "Tanqiya-e-Dimagh; take immediately prior to sleep.",
            adherence_status: "PENDING",
          },
        ],
      },
    ],
    dietary_guidelines: [
      "Strictly avoid Laham-e-Baqar (Beef) and stale legumes.",
      "Incorporate Zanjabeel and Pudina into noon broth.",
      "Maintain hydration with Aab-e-Anar or lukewarm water.",
    ],
  };
}

function getFallbackMessages(patientId: string): PortalMessage[] {
  return [
    {
      message_id: "msg-001",
      patient_id: patientId,
      sender_type: "CLINICIAN",
      timestamp_utc: new Date(Date.now() - 3600 * 1000 * 4).toISOString(),
      message_body:
        "Salam. Please remember to take Majun Suranjan with lukewarm Aab-e-Badiyan rather than cold water to optimize stomach absorption.",
      triage_status: "ROUTINE",
      requires_immediate_action: false,
    },
    {
      message_id: "msg-002",
      patient_id: patientId,
      sender_type: "PATIENT",
      timestamp_utc: new Date(Date.now() - 3600 * 1000 * 2).toISOString(),
      message_body:
        "Thank you, Doctor. The morning joint stiffness has significantly decreased after 3 days of Dalak-e-Layyin.",
      triage_status: "ROUTINE",
      requires_immediate_action: false,
    },
  ];
}
