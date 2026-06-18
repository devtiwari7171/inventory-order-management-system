import api from '../api/axios';

export const customerService = {
  list: ({ q = '', skip = 0, limit = 50 } = {}) =>
    api.get('/customers/', { params: { q, skip, limit } }).then((r) => r.data),

  get: (id) => api.get(`/customers/${id}`).then((r) => r.data),

  create: (payload) => api.post('/customers/', payload).then((r) => r.data),

  update: (id, payload) => api.put(`/customers/${id}`, payload).then((r) => r.data),

  remove: (id) => api.delete(`/customers/${id}`).then((r) => r.data),
};
