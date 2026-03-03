// src/services/api.js
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// ── helpers ──────────────────────────────────────────────────────────────────
const getToken = () => localStorage.getItem("token");

async function request(path, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };
  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

// ── Auth ─────────────────────────────────────────────────────────────────────
export const login = (username, password) =>
  request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });

// ── Sales ────────────────────────────────────────────────────────────────────
export const getSales = (statusFilter) => {
  const q = statusFilter ? `?status=${statusFilter}` : "";
  return request(`/sales${q}`);
};

// ── Predict ──────────────────────────────────────────────────────────────────
export const predict = (jumlah_penjualan, harga, diskon) =>
  request("/predict", {
    method: "POST",
    body: JSON.stringify({ jumlah_penjualan, harga, diskon }),
  });
