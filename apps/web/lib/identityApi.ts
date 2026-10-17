const IDENTITY_API_URL =
  process.env.NEXT_PUBLIC_GATEWAY_URL ||
  process.env.NEXT_PUBLIC_IDENTITY_API_URL ||
  "http://localhost:8000";

export interface OrganizationOut {
  id: string;
  name: string;
  slug: string;
  tier: string;
  is_active: boolean;
  created_at: string;
}

export interface UserOut {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  mfa_enabled: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in_seconds: number;
  user: UserOut;
  organization: OrganizationOut;
  roles: string[];
  permissions: string[];
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${IDENTITY_API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      // ignore — fall back to statusText
    }
    throw new ApiError(res.status, detail);
  }
  return res.json() as Promise<T>;
}

export const identityApi = {
  signup: (payload: {
    email: string;
    full_name: string;
    password: string;
    organization_slug: string;
    role_name: string;
  }) => request<TokenResponse>("/api/v1/auth/signup", { method: "POST", body: JSON.stringify(payload) }),

  login: (payload: { email: string; password: string; organization_slug: string }) =>
    request<TokenResponse>("/api/v1/auth/login", { method: "POST", body: JSON.stringify(payload) }),

  session: (token: string) =>
    request<{ userId: string; organizationId: string; roles: string[]; permissions: string[] }>(
      "/api/v1/auth/session",
      { headers: { Authorization: `Bearer ${token}` } }
    ),

  logout: (token: string) =>
    request<{ detail: string }>("/api/v1/auth/logout", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    }),

  createOrganization: (payload: { name: string; slug: string; tier?: string }) =>
    request<OrganizationOut>("/api/v1/organizations", { method: "POST", body: JSON.stringify(payload) }),
};
