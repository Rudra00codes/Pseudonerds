export interface Symptom {
    id: string;
    name: string;
    severity: 'mild' | 'moderate' | 'severe';
    duration?: string;
    description?: string;
    localizedNames?: Record<string, string>;
}

export interface DiagnosticResult {
    diagnosis: string;
    confidence: number;
    recommendations?: string[];
    severity: 'low' | 'medium' | 'high';
    timestamp: string;
    symptoms: Symptom[];
    requiredActions: {
        immediate: string[];
        followUp: string[];
    };
    specialistReferral?: {
        required: boolean;
        speciality?: string;
        urgency: 'routine' | 'urgent' | 'emergency';
    };
}

export interface ApiError {
    code: string;
    message: string;
    details?: unknown;
}

export interface UserPreferences {
    language: string;
    theme: 'light' | 'dark' | 'system';
    notifications: boolean;
    accessibilitySettings: {
        fontSize: 'normal' | 'large' | 'extra-large';
        highContrast: boolean;
        screenReader: boolean;
    };
    offlineMode: boolean;
}

export interface TeleconsultationSession {
    id: string;
    patientId: string;
    doctorId?: string;
    status: 'scheduled' | 'in-progress' | 'completed' | 'cancelled';
    scheduledTime: string;
    diagnosis?: DiagnosticResult;
    notes?: string;
}