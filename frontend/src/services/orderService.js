import api from '../api/axios';

export const orderService = {
  list: ({ skip = 0, limit = 50 } = {}) =>
    api.get('/orders/', { params: { skip, limit } }).then((r) => r.data),

  get: (id) => api.get(`/orders/${id}`).then((r) => r.data),

  create: (payload) => api.post('/orders/', payload).then((r) => r.data),

  remove: (id) => api.delete(`/orders/${id}`).then((r) => r.data),
};
