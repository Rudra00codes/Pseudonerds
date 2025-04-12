import axios from 'axios';
import { API_BASE_URL } from '../config';

export interface SymptomInput {
    symptoms: string[];
    language: string;
}

export interface DiagnosticResult {
    diagnosis: string;
    confidence: number;
}

export const diagnosticService = {
    submitSymptoms: async (input: SymptomInput): Promise<DiagnosticResult> => {
        const response = await axios.post(`${API_BASE_URL}/api/diagnose/`, input);
        return response.data;
    }
};