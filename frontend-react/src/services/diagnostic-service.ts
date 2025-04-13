import { Symptom, DiagnosticResult } from '@/lib/types';
import { config } from '@/lib/config';
import * as tf from '@tensorflow/tfjs';

export class DiagnosticService {
    private static instance: DiagnosticService;
    private modelLoaded: boolean = false;
    private model: tf.LayersModel | null = null;

    private constructor() {}

    static getInstance(): DiagnosticService {
        if (!DiagnosticService.instance) {
            DiagnosticService.instance = new DiagnosticService();
        }
        return DiagnosticService.instance;
    }

    async initialize(): Promise<void> {
        try {
            await this.loadModel();
            this.modelLoaded = true;
        } catch (error) {
            console.error('Failed to initialize diagnostic service:', error);
            throw new Error('Model initialization failed');
        }
    }

    async processSymptoms(symptoms: Symptom[]): Promise<DiagnosticResult> {
        if (!this.modelLoaded || !this.model) {
            throw new Error('Diagnostic model not initialized');
        }

        try {
            const processedSymptoms = this.preprocessSymptoms(symptoms);
            const diagnosis = await this.runInference(processedSymptoms);
            
            return {
                ...diagnosis,
                timestamp: new Date().toISOString(),
                symptoms,
                requiredActions: this.generateActions(diagnosis.severity),
                specialistReferral: this.checkReferralNeed(diagnosis)
            };
        } catch (error) {
            console.error('Error processing symptoms:', error);
            throw new Error('Symptom processing failed');
        }
    }

    private async loadModel(): Promise<void> {
        try {
            this.model = await tf.loadLayersModel('/models/diagnostic_model.json');
            await this.model.summary();
        } catch (error) {
            console.error('Model loading failed:', error);
            throw new Error('Failed to load the diagnostic model');
        }
    }

    private preprocessSymptoms(symptoms: Symptom[]): Float32Array {
        // Convert symptoms to model input format
        const inputSize = 100; // Adjust based on your model
        const input = new Float32Array(inputSize).fill(0);
        
        symptoms.forEach(symptom => {
            const severityScore = this.getSeverityScore(symptom.severity);
            // Map symptom to input vector (implement based on your model)
        });

        return input;
    }

    private async runInference(input: Float32Array): Promise<Partial<DiagnosticResult>> {
        if (!this.model) throw new Error('Model not loaded');

        const tensorInput = tf.tensor2d([Array.from(input)]);
        const prediction = await this.model.predict(tensorInput) as tf.Tensor;
        const results = await prediction.array();
        tensorInput.dispose();
        prediction.dispose();

        return this.interpretResults(results[0]);
    }

    private getSeverityScore(severity: string): number {
        const scores = { 'mild': 0.3, 'moderate': 0.6, 'severe': 1.0 };
        return scores[severity as keyof typeof scores] || 0.3;
    }

    private interpretResults(results: number[]): Partial<DiagnosticResult> {
        // Implement based on your model's output format
        return {
            diagnosis: 'Sample diagnosis',
            confidence: results[0],
            severity: results[1] > 0.7 ? 'high' : results[1] > 0.3 ? 'medium' : 'low'
        };
    }

    private generateActions(severity: string): { immediate: string[], followUp: string[] } {
        const actions = {
            low: {
                immediate: ['Rest', 'Stay hydrated'],
                followUp: ['Monitor symptoms']
            },
            medium: {
                immediate: ['Rest', 'Stay hydrated', 'Take prescribed medication'],
                followUp: ['Schedule follow-up in 48 hours']
            },
            high: {
                immediate: ['Seek immediate medical attention', 'Take prescribed medication'],
                followUp: ['Urgent medical review required']
            }
        };
        return actions[severity as keyof typeof actions] || actions.low;
    }

    private checkReferralNeed(diagnosis: Partial<DiagnosticResult>): { required: boolean, urgency: 'routine' | 'urgent' | 'emergency' } {
        if (diagnosis.severity === 'high') {
            return { required: true, urgency: 'emergency' };
        }
        return { required: false, urgency: 'routine' };
    }
}