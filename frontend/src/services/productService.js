import api from '../api/axios';

export const productService = {
  list: ({ q = '', skip = 0, limit = 50 } = {}) =>
    api.get('/products/', { params: { q, skip, limit } }).then((r) => r.data),

  get: (id) => api.get(`/products/${id}`).then((r) => r.data),

  create: (payload) => api.post('/products/', payload).then((r) => r.data),

  update: (id, payload) => api.put(`/products/${id}`, payload).then((r) => r.data),

  remove: (id) => api.delete(`/products/${id}`).then((r) => r.data),
};
