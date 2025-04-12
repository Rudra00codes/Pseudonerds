"use client"

import React, { useState, useEffect } from 'react';
import { Box, TextField, Button, FormControl, InputLabel, Select, MenuItem, Chip, Alert, CircularProgress } from '@mui/material';
import { DiagnosticService } from '@/services/diagnostic-service';
interface Symptom {
  id: string;
  name: string;
  severity: string;
}

interface SymptomFormProps {
  onDiagnosisReceived: (diagnosis: any) => void;
  language: string;
}

const COMMON_SYMPTOMS = [
  { id: '1', name: 'Fever', severity: 'moderate' },
  { id: '2', name: 'Cough', severity: 'mild' },
  { id: '3', name: 'Headache', severity: 'moderate' },
  { id: '4', name: 'Fatigue', severity: 'mild' },
  { id: '5', name: 'Body Pain', severity: 'moderate' }
];

export default function SymptomForm({ onDiagnosisReceived, language }: SymptomFormProps) {
  const [selectedSymptoms, setSelectedSymptoms] = useState<Symptom[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const diagnosticService = DiagnosticService.getInstance();

  useEffect(() => {
    const initializeService = async () => {
      try {
        await diagnosticService.initialize();
      } catch (err) {
        setError('Failed to initialize diagnostic service');
      }
    };
    initializeService();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const diagnosis = await diagnosticService.processSymptoms(selectedSymptoms);
      onDiagnosisReceived(diagnosis);
    } catch (err) {
      setError('Failed to process symptoms. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ p: 3 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      <Box sx={{ mb: 3 }}>
        {COMMON_SYMPTOMS.map((symptom) => (
          <Chip
            key={symptom.id}
            label={symptom.name}
            onClick={() => {
              if (!selectedSymptoms.find(s => s.id === symptom.id)) {
                setSelectedSymptoms([...selectedSymptoms, symptom]);
              }
            }}
            sx={{ m: 0.5 }}
            color={selectedSymptoms.find(s => s.id === symptom.id) ? "primary" : "default"}
          />
        ))}
      </Box>

      {selectedSymptoms.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <h3>Selected Symptoms:</h3>
          {selectedSymptoms.map((symptom) => (
            <Chip
              key={symptom.id}
              label={symptom.name}
              onDelete={() => setSelectedSymptoms(selectedSymptoms.filter(s => s.id !== symptom.id))}
              color="primary"
              sx={{ m: 0.5 }}
            />
          ))}
        </Box>
      )}

      <Button
        type="submit"
        variant="contained"
        color="primary"
        disabled={loading || selectedSymptoms.length === 0}
        sx={{ mt: 2 }}
      >
        {loading ? <CircularProgress size={24} /> : 'Get Diagnosis'}
      </Button>
    </Box>
  );
}