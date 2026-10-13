import apiClient from './apiClient';

export async function register({ email, password, full_name }) {
  const { data } = await apiClient.post('/api/auth/register', {
    email,
    password,
    full_name,
  });
  return data;
}

export async function login({ email, password }) {
  const { data } = await apiClient.post('/api/auth/login', { email, password });
  return data;
}

export async function getCurrentUser() {
  const { data } = await apiClient.get('/api/auth/me');
  return data;
}

export function saveSession({ access_token, user }) {
  localStorage.setItem('access_token', access_token);
  localStorage.setItem('user', JSON.stringify(user));
}

export function clearSession() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
}

export function getStoredUser() {
  const raw = localStorage.getItem('user');
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function getStoredToken() {
  return localStorage.getItem('access_token');
}
