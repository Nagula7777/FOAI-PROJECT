import apiClient from './apiClient';

export const profileApi = {
  get: () => apiClient.get('/api/profile').then((r) => r.data),
  update: (data) => apiClient.put('/api/profile', data).then((r) => r.data),
  listDebts: () => apiClient.get('/api/debts').then((r) => r.data),
  createDebt: (data) => apiClient.post('/api/debts', data).then((r) => r.data),
  deleteDebt: (id) => apiClient.delete(`/api/debts/${id}`),
  listAssets: () => apiClient.get('/api/assets').then((r) => r.data),
  createAsset: (data) => apiClient.post('/api/assets', data).then((r) => r.data),
  deleteAsset: (id) => apiClient.delete(`/api/assets/${id}`),
};

export const goalApi = {
  list: () => apiClient.get('/api/goals').then((r) => r.data),
  get: (id) => apiClient.get(`/api/goals/${id}`).then((r) => r.data),
  create: (data) => apiClient.post('/api/goals', data).then((r) => r.data),
  update: (id, data) => apiClient.put(`/api/goals/${id}`, data).then((r) => r.data),
  delete: (id) => apiClient.delete(`/api/goals/${id}`),
  analysis: (id) => apiClient.get(`/api/goals/${id}/analysis`).then((r) => r.data),
};

export const aiApi = {
  analyze: () => apiClient.post('/api/ai/analyze').then((r) => r.data),
  recommendation: () => apiClient.get('/api/ai/recommendation').then((r) => r.data),
  health: () => apiClient.get('/api/financial-health').then((r) => r.data),
  emergencyFund: () => apiClient.get('/api/emergency-fund').then((r) => r.data),
  capacity: () => apiClient.get('/api/investment-capacity').then((r) => r.data),
  submitRisk: (data) => apiClient.post('/api/risk-assessment', data).then((r) => r.data),
  latestRisk: () => apiClient.get('/api/risk-assessment/latest').then((r) => r.data),
  warnings: () => apiClient.get('/api/warnings').then((r) => r.data),
};

export const portfolioApi = {
  get: () => apiClient.get('/api/portfolio').then((r) => r.data),
  rebalancing: () => apiClient.get('/api/rebalancing').then((r) => r.data),
  products: () => apiClient.get('/api/investment-products').then((r) => r.data),
  whatIf: (data) => apiClient.post('/api/simulation/what-if', data).then((r) => r.data),
  listScenarios: () => apiClient.get('/api/simulation/what-if').then((r) => r.data),
};

export const reportApi = {
  list: () => apiClient.get('/api/reports/monthly').then((r) => r.data),
  generate: () => apiClient.post('/api/reports/monthly/generate').then((r) => r.data),
  get: (id) => apiClient.get(`/api/reports/monthly/${id}`).then((r) => r.data),
  pdfUrl: (id) => `/api/reports/monthly/${id}/pdf`,
};
