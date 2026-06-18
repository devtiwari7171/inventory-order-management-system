import api from '../api/axios';

export const dashboardService = {
  stats: () => api.get('/dashboard/').then((r) => r.data),
};
