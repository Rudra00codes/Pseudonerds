export const config = {
    apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
    supportedLanguages: [
        { code: 'en', name: 'English' },
        { code: 'hi', name: 'Hindi' },
        { code: 'bn', name: 'Bengali' },
        { code: 'te', name: 'Telugu' },
        { code: 'ta', name: 'Tamil' }
    ],
    maxSymptoms: 10,
    offlineStorageKey: 'diagnostic_cache',
    modelVersion: '1.0.0'
};