import { Platform } from 'react-native';

// Use 10.0.2.2 for Android emulator (maps to host localhost), else localhost
const BASE_URL = Platform.OS === 'android'
  ? 'http://10.0.2.2:8000'
  : 'http://localhost:8000';

let _authToken: string | null = null;

export function setAuthToken(token: string | null) {
  _authToken = token;
}

export async function apiGet<T = unknown>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(_authToken ? { Authorization: `Bearer ${_authToken}` } : {}),
    },
  });
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return res.json();
}

export async function apiPost<T = unknown>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(_authToken ? { Authorization: `Bearer ${_authToken}` } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail || `POST ${path} failed: ${res.status}`);
  }
  return res.json();
}
