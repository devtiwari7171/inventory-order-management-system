/**
 * Centralized Axios instance with:
 *  - Base URL from VITE_API_URL or relative (for Vite proxy)
 *  - Request interceptor (timing)
 *  - Response interceptor that normalizes errors so they always carry a .detail message
 */
import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

// Response interceptor: normalize errors for the UI
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Build a user-friendly message
    const detail =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      error?.message ||
      'Unexpected error';
    const normalized = new Error(
      typeof detail === 'string' ? detail : JSON.stringify(detail)
    );
    normalized.status = error?.response?.status;
    normalized.original = error;
    return Promise.reject(normalized);
  }
);

export default api;
