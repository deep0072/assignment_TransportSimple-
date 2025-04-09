import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  register: (userData) => api.post('/auth/users/', userData),
  login: (credentials) => api.post('/auth/users/login', credentials),
  logout: (refreshToken) => api.post('/auth/users/logout', { refresh_token: refreshToken }),
};

export const questions = {
  getAll: () => api.get('/questions/'),
  create: (questionData) => api.post('/questions/', questionData),
  getAnswers: (questionId) => api.get(`/questions/${questionId}/answers/`),
  createAnswer: (questionId, answerData) => api.post(`/questions/${questionId}/answers/`, answerData),
  likeAnswer: (answerId, questionId) => api.post(`/answers/${answerId}/like/`, { question_id: questionId }),
};

export default api;