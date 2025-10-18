import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Product APIs
export const productApi = {
  getAll: (status?: string, limit = 50, offset = 0) =>
    api.get('/api/products', { params: { status, limit, offset } }),

  getById: (id: number) =>
    api.get(`/api/products/${id}`),

  approve: (id: number) =>
    api.post(`/api/products/${id}/approve`),

  reject: (id: number, reason: string) =>
    api.post(`/api/products/${id}/reject`, { reason }),

  post: (id: number, platforms: string[]) =>
    api.post(`/api/products/${id}/post`, { platforms }),
};

// Trend APIs
export const trendApi = {
  scan: () =>
    api.post('/api/trends/scan'),

  getSources: () =>
    api.get('/api/trends/sources'),
};

// Analytics APIs
export const analyticsApi = {
  getDashboard: () =>
    api.get('/api/analytics/dashboard'),
};

export default api;
