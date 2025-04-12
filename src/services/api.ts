import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

export const diagnosticService = {
    submitSymptoms: async (symptoms: string[], language: string) => {
        return api.post('/api/diagnose', { symptoms, language });
    }
};