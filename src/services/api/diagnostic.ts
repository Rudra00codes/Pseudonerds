import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export interface SymptomRequest {
  symptoms: string[];
  language: string;
  patientId?: string;
}

export interface DiagnosticResponse {
  diagnosis: string;
  confidence: number;
  recommendations?: string[];
  severity?: 'low' | 'medium' | 'high';
}

export const diagnosticService = {
  submitSymptoms: async (data: SymptomRequest): Promise<DiagnosticResponse> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/diagnose`, data);
      return response.data;
    } catch (error) {
      console.error('Diagnostic API Error:', error);
      throw new Error('Failed to process symptoms');
    }
  },

  getHistory: async (patientId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/diagnose/history/${patientId}`);
      return response.data;
    } catch (error) {
      console.error('History API Error:', error);
      throw new Error('Failed to fetch diagnostic history');
    }
  }
};