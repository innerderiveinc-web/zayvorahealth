import AsyncStorage from '@react-native-async-storage/async-storage';
import { apiPost, setAuthToken } from './api.service';

const TOKEN_KEY = 'zayvora_access_token';
const REFRESH_KEY = 'zayvora_refresh_token';

export async function login(email: string, password: string): Promise<{ access_token: string; refresh_token: string }> {
  const data = await apiPost<{ access_token: string; refresh_token: string }>(
    '/api/identity/auth/login', { email, password }
  );
  await AsyncStorage.setItem(TOKEN_KEY, data.access_token);
  await AsyncStorage.setItem(REFRESH_KEY, data.refresh_token);
  setAuthToken(data.access_token);
  return data;
}

export async function register(payload: { email: string; password: string; name: string; role?: string }) {
  return apiPost('/api/identity/auth/register', payload);
}

export async function logout() {
  await AsyncStorage.multiRemove([TOKEN_KEY, REFRESH_KEY]);
  setAuthToken(null);
}

export async function getStoredToken(): Promise<string | null> {
  const token = await AsyncStorage.getItem(TOKEN_KEY);
  if (token) setAuthToken(token);
  return token;
}

export async function refreshToken(): Promise<string | null> {
  const refresh = await AsyncStorage.getItem(REFRESH_KEY);
  if (!refresh) return null;
  try {
    const data = await apiPost<{ access_token: string; refresh_token: string }>(
      '/api/identity/auth/refresh', { refresh_token: refresh }
    );
    await AsyncStorage.setItem(TOKEN_KEY, data.access_token);
    await AsyncStorage.setItem(REFRESH_KEY, data.refresh_token);
    setAuthToken(data.access_token);
    return data.access_token;
  } catch {
    await logout();
    return null;
  }
}
