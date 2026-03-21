// ============================================================
// api.js — Single source of truth for ALL backend API calls
// Every page imports from here. Never call fetch() directly.
// ============================================================

const BASE = 'http://localhost:8000/api';

function getToken()        { return localStorage.getItem('access_token'); }
function getRefreshToken() { return localStorage.getItem('refresh_token'); }

async function refreshAccessToken() {
  const res = await fetch(`${BASE}/auth/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh: getRefreshToken() }),
  });
  if (!res.ok) {
    localStorage.clear();
    window.location.href = '/frontend/pages/login.html';
    throw new Error('Session expired. Please log in again.');
  }
  const data = await res.json();
  localStorage.setItem('access_token', data.access);
  return data.access;
}

async function request(method, path, body = null, isMultipart = false) {
  const makeRequest = async (token) => {
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (!isMultipart && body) headers['Content-Type'] = 'application/json';

    const opts = { method, headers };
    if (body) opts.body = isMultipart ? body : JSON.stringify(body);

    const res = await fetch(`${BASE}${path}`, opts);

    if (res.status === 401) {
      const newToken = await refreshAccessToken();
      return makeRequest(newToken);
    }

    if (!res.ok) {
      let errData = {};
      try { errData = await res.json(); } catch {}
      const msg = errData.error || errData.detail ||
                  Object.values(errData).flat().join(' ') ||
                  `HTTP ${res.status}`;
      throw new Error(msg);
    }

    if (res.status === 204) return null;
    return res.json();
  };

  return makeRequest(getToken());
}

// ── Helper: decode JWT payload ───────────────────────────────
export function getTokenPayload() {
  const token = getToken();
  if (!token) return null;
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch { return null; }
}

export function getCurrentRole() {
  const p = getTokenPayload();
  return p ? p.role : null;
}

export function getCurrentUserId() {
  const p = getTokenPayload();
  return p ? p.user_id : null;
}

export function isLoggedIn() { return !!getToken(); }

// ── API surface ──────────────────────────────────────────────
export const api = {

  auth: {
    login:   (login_id, password) =>
      request('POST', '/auth/login/', { login_id, password }),
    signup:  (data) => request('POST', '/auth/signup/', data),
    refresh: (refresh) => request('POST', '/auth/refresh/', { refresh }),
    users:   () => request('GET', '/auth/users/'),
  },

  products: {
    list:     (search = '', status_filter = '') =>
      request('GET', `/products/?search=${encodeURIComponent(search)}&status=${status_filter}`),
    get:      (id) => request('GET', `/products/${id}/`),
    create:   (formData) => request('POST', '/products/', formData, true),
    versions: (id) => request('GET', `/products/${id}/versions/`),
  },

  boms: {
    list:   (search = '') =>
      request('GET', `/boms/?search=${encodeURIComponent(search)}`),
    get:    (id) => request('GET', `/boms/${id}/`),
    create: (data) => request('POST', '/boms/', data),
  },

  ecos: {
    list:      () => request('GET', '/ecos/'),
    get:       (id) => request('GET', `/ecos/${id}/`),
    create:    (data) => request('POST', '/ecos/', data),
    update:    (id, data) => request('PATCH', `/ecos/${id}/`, data),
    start:     (id) => request('POST', `/ecos/${id}/start/`),
    validate:  (id) => request('PATCH', `/ecos/${id}/stage/next/`),
    approve:   (id) => request('POST', `/ecos/${id}/approve/`),
    reject:    (id, reason) => request('POST', `/ecos/${id}/reject/`, { reason }),
    diff:      (id) => request('GET', `/ecos/${id}/diff/`),
    addChange: (id, data) => request('POST', `/ecos/${id}/changes/`, data),
  },

  settings: {
    stages: {
      list:   () => request('GET', '/settings/stages/'),
      create: (data) => request('POST', '/settings/stages/', data),
      update: (id, data) => request('PUT', `/settings/stages/${id}/`, data),
      delete: (id) => request('DELETE', `/settings/stages/${id}/`),
    },
    approvals: {
      list:   () => request('GET', '/settings/approvals/'),
      create: (data) => request('POST', '/settings/approvals/', data),
      update: (id, data) => request('PUT', `/settings/approvals/${id}/`, data),
      delete: (id) => request('DELETE', `/settings/approvals/${id}/`),
    },
  },

  reports: {
    ecos:            () => request('GET', '/reports/ecos/'),
    productVersions: () => request('GET', '/reports/product-versions/'),
    bomHistory:      () => request('GET', '/reports/bom-history/'),
    archived:        () => request('GET', '/reports/archived/'),
  },

  audit: {
    get: (entityType, entityId) =>
      request('GET', `/audit/${entityType}/${entityId}/`),
  },
};
