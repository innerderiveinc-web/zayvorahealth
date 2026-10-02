import { ApiError } from "./identityApi";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_GATEWAY_URL ||
  process.env.NEXT_PUBLIC_KNOWLEDGE_API_URL ||
  "http://localhost:8000";

export interface SearchResultItem {
  id: string;
  category: "mufradat" | "murakkabat" | "amraz" | "tadbeer" | "navigation";
  title: string;
  subtitle: string;
  badge?: string;
  route: string;
  metadata?: Record<string, any>;
}

export const DEFAULT_CLINICAL_QUICK_ACTIONS: SearchResultItem[] = [
  {
    id: "qa-new-encounter",
    category: "navigation",
    title: "Action • Start Patient Consultation",
    subtitle: "Launch active clinical encounter cockpit & Clinical Thread™",
    badge: "Consultation",
    route: "/doctor/consultation",
  },
  {
    id: "qa-find-patient",
    category: "navigation",
    title: "Action • Find Patient Chart",
    subtitle: "Search Master Patient Index (MPI) by MRN or Name",
    badge: "Patient 360",
    route: "/doctor/patients",
  },
  {
    id: "qa-opd-queue",
    category: "navigation",
    title: "Action • Open OPD Token Queue",
    subtitle: "Inspect triage queue, token progression, and waiting times",
    badge: "OPD Queue",
    route: "/doctor/queue",
  },
  {
    id: "qa-hakeem-ai",
    category: "navigation",
    title: "Action • Clinical Decision Support",
    subtitle: "Query Hakeem Sahab™ AI Copilot for classical-modern synthesis",
    badge: "Hakeem AI",
    route: "/doctor/hakeem-sahab",
  },
  {
    id: "qa-safety-rail",
    category: "navigation",
    title: "Action • Safety Firewall Check",
    subtitle: "Inspect CYP450 interactions, Mudabbar, and Tanafur rules",
    badge: "Safety Rail",
    route: "/doctor/nuskha",
  },
  {
    id: "qa-nuskha-compose",
    category: "navigation",
    title: "Action • Formulate Multi-Pillar Rx",
    subtitle: "Author Unani Nuskha prescription with Schedule E(1) Mudabbar gate",
    badge: "Nuskha",
    route: "/doctor/nuskha",
  },
  {
    id: "qa-knowledge-gov",
    category: "navigation",
    title: "Action • 12-Stage Knowledge Governance",
    subtitle: "Review pharmacognosy, classical canon, and promotion pipeline",
    badge: "Governance",
    route: "/admin/compliance",
  },
];

export const searchApi = {
  async omniSearch(query: string, limit = 20): Promise<SearchResultItem[]> {
    const trimmed = query.trim();
    if (!trimmed) {
      return DEFAULT_CLINICAL_QUICK_ACTIONS;
    }

    try {
      const res = await fetch(
        `${API_BASE_URL}/api/v1/knowledge/search/omni?q=${encodeURIComponent(trimmed)}&limit=${limit}`
      );
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          return data;
        }
      }
    } catch {
      // Graceful local fallback on network interruption
    }

    // Local fuzzy filtering of default actions and known clinical topics
    const qLower = trimmed.toLowerCase();
    const filtered = DEFAULT_CLINICAL_QUICK_ACTIONS.filter(
      (a) =>
        a.title.toLowerCase().includes(qLower) ||
        a.subtitle.toLowerCase().includes(qLower) ||
        a.badge?.toLowerCase().includes(qLower)
    );

    return filtered;
  },
};
