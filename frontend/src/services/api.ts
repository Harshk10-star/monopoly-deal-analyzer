import axios from 'axios';

// Create axios instance
export const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Game analysis API methods
export const gameAnalysisApi = {
  analyze: (gameState: any, strategy: string) =>
    api.post('/api/v1/analysis/analyze', { gameState, strategy }),
  
  simulate: (gameState: any, strategy: string, numSimulations: number) =>
    api.post('/api/v1/analysis/simulate', { gameState, strategy, numSimulations }),
  
  getHistory: (limit: number = 10) =>
    api.get(`/api/v1/analysis/history?limit=${limit}`),
};

// Payment API methods
export const paymentApi = {
  createCheckout: (paymentType: string, quantity?: number) =>
    api.post('/api/v1/payments/create-checkout', { payment_type: paymentType, quantity }),
  
  getCredits: () =>
    api.get('/api/v1/payments/credits'),
};

// User API methods
export const userApi = {
  getProfile: () =>
    api.get('/api/v1/users/profile'),
  
  updateProfile: (userData: any) =>
    api.put('/api/v1/users/profile', userData),
  
  getStats: () =>
    api.get('/api/v1/users/stats'),
  
  deleteAccount: () =>
    api.delete('/api/v1/users/account'),
};

// Auth API methods
export const authApi = {
  login: (email: string, password: string) =>
    api.post('/api/v1/auth/login', { email, password }),
  
  register: (email: string, password: string) =>
    api.post('/api/v1/auth/register', { email, password }),
  
  refresh: () =>
    api.post('/api/v1/auth/refresh'),
};



