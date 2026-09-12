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

export const searchApi = {
  async omniSearch(query: string, limit = 20): Promise<SearchResultItem[]> {
    const res = await fetch(
      `${API_BASE_URL}/api/v1/knowledge/search/omni?q=${encodeURIComponent(query)}&limit=${limit}`
    );
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
    return res.json();
  },
};
