import axios from 'axios';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const apiClient = axios.create({
  baseURL: apiBaseUrl,
});

export const analyzeResume = (formData) => apiClient.post('/analyze/', formData);
export const createAdvice = (payload) => apiClient.post('/advice/', payload);
export const createInterviewQuestions = (payload) => apiClient.post('/interview/', payload);
export const generateReport = (payload) => apiClient.post('/report/', payload, { responseType: 'blob' });
export const tailorResume = (payload) => apiClient.post('/tailor-resume/', payload);

export default apiClient;
