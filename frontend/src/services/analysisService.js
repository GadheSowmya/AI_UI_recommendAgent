import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const analysisService = {
  // Health check
  healthCheck: () => apiClient.get('/health'),

  // Screenshot analysis
  analyzeScreenshot: (imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    return apiClient.post('/analyze/screenshot', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  // Code analysis
  analyzeCode: (htmlCode, cssCode = '', jsCode = '') => {
    return apiClient.post('/analyze/code', {
      html: htmlCode,
      css: cssCode,
      js: jsCode,
    });
  },

  // Hybrid analysis (image + code)
  analyzeHybrid: (imageFile, htmlCode, cssCode = '') => {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('html', htmlCode);
    if (cssCode) formData.append('css', cssCode);
    return apiClient.post('/analyze/hybrid', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  // Get analysis history
  getHistory: (limit = 10) => {
    return apiClient.get(`/history?limit=${limit}`);
  },

  // Get specific recommendations
  getRecommendations: (analysisId) => {
    return apiClient.get(`/recommendations/${analysisId}`);
  },

  // Export report
  exportReport: (analysisIndex = -1, format = 'json') => {
    return apiClient.post('/export-report', {
      analysis_index: analysisIndex,
      format: format,
    });
  },

  // Get all UX rules
  getRules: () => {
    return apiClient.get('/rules');
  },
};

export default apiClient;
