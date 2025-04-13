"use client"

import React from 'react';
import { Box, Paper, Typography, Chip, Divider, Button } from '@mui/material';
interface DiagnosticResult {
  diagnosis: string;
  confidence: number;
  severity: string;
  requiredActions: {
    immediate: string[];
    followUp: string[];
  };
  specialistReferral?: {
    required: boolean;
    urgency: string;
  };
}
import { Warning, CheckCircle, Error } from '@mui/icons-material';

interface DiagnosisResultProps {
  result: DiagnosticResult;
  onClose: () => void;
}

const severityColors = {
  low: { color: 'success', icon: CheckCircle },
  medium: { color: 'warning', icon: Warning },
  high: { color: 'error', icon: Error }
};

export default function DiagnosisResult({ result, onClose }: DiagnosisResultProps) {
  const severityInfo = severityColors[result.severity as keyof typeof severityColors];
  const SeverityIcon = severityInfo.icon;

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <SeverityIcon color={severityInfo.color as any} sx={{ mr: 1 }} />
        <Typography variant="h5" component="h2">
          Diagnostic Results
        </Typography>
      </Box>

      <Divider sx={{ my: 2 }} />

      <Typography variant="h6" gutterBottom>
        {result.diagnosis}
      </Typography>

      <Box sx={{ my: 2 }}>
        <Chip
          label={`Confidence: ${(result.confidence * 100).toFixed(1)}%`}
          color="primary"
          sx={{ mr: 1 }}
        />
        <Chip
          label={`Severity: ${result.severity.toUpperCase()}`}
          color={severityInfo.color as any}
        />
      </Box>

      <Box sx={{ my: 3 }}>
        <Typography variant="h6" gutterBottom>Immediate Actions:</Typography>
        {result.requiredActions.immediate.map((action, index) => (
          <Typography key={index} sx={{ ml: 2 }}>• {action}</Typography>
        ))}
      </Box>

      <Box sx={{ my: 3 }}>
        <Typography variant="h6" gutterBottom>Follow-up Actions:</Typography>
        {result.requiredActions.followUp.map((action, index) => (
          <Typography key={index} sx={{ ml: 2 }}>• {action}</Typography>
        ))}
      </Box>

      {result.specialistReferral?.required && (
        <Box sx={{ my: 3, p: 2, bgcolor: 'error.light', borderRadius: 1 }}>
          <Typography variant="h6" color="error.dark">
            Specialist Referral Required - {result.specialistReferral.urgency.toUpperCase()}
          </Typography>
        </Box>
      )}

      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
        <Button variant="outlined" onClick={onClose}>
          New Diagnosis
        </Button>
        <Button variant="contained" color="primary">
          Schedule Teleconsultation
        </Button>
      </Box>
    </Paper>
  );
}