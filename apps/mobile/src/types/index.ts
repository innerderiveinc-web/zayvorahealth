export type Role = "patient" | "doctor";

export type Language = "en" | "ur" | "hi";

export interface PatientProfile {
  mrn: string;
  name: string;
  age: number;
  gender: string;
  mizaj: "Damawi (Sanguine)" | "Safrawi (Choleric)" | "Balghami (Phlegmatic)" | "Sawdawi (Melancholic)";
  dominantOrganAxis: "Qalb-Dimagh" | "Kabid-Mida" | "Kulyah-Masana";
  activeConditions: string[];
}

export interface PrescriptionItem {
  id: string;
  formulation: string;
  dosage: string;
  frequency: string;
  duration: string;
  anupan: string;
  audioGuideAvailable: boolean;
  audioPosologyText: {
    en: string;
    ur: string;
    hi: string;
  };
}

export interface AsbabSittahLog {
  date: string;
  hawa_air: "fresh_mountain" | "moderate_ventilated" | "congested_polluted";
  makul_food: "balanced_prescribed" | "excess_spicy" | "excess_phlegmatic";
  harakat_movement: number; // minutes
  nawm_sleep: number; // hours
  istifragh_retention: "normal_evacuation" | "constipated" | "diarrhea";
  nafsaniyah_psychic: "calm_focused" | "moderate_stress" | "acute_anxiety";
}
