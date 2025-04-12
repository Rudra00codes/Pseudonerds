import tensorflow as tf
import numpy as np
import json
import os
from typing import Dict, List, Optional

class DiagnosticModel:
    def __init__(self, model_path: str = "models/diagnostic_model.tflite"):
        self.model_path = model_path
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.symptom_mapping = self._load_symptom_mapping()

    def _load_symptom_mapping(self) -> Dict:
        mapping_path = os.path.join(os.path.dirname(__file__), "models/symptom_mapping.json")
        try:
            with open(mapping_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def initialize(self) -> bool:
        try:
            self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            return True
        except Exception as e:
            print(f"Model initialization failed: {str(e)}")
            return False

    def process_symptoms(self, symptoms: List[Dict]) -> Dict:
        if not self.interpreter:
            raise RuntimeError("Model not initialized")

        try:
            processed_input = self._preprocess_symptoms(symptoms)
            self.interpreter.set_tensor(self.input_details[0]['index'], processed_input)
            self.interpreter.invoke()
            
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            return self._postprocess_output(output_data)
        except Exception as e:
            raise RuntimeError(f"Inference failed: {str(e)}")

    def _preprocess_symptoms(self, symptoms: List[Dict]) -> np.ndarray:
        input_size = self.input_details[0]['shape'][1]
        input_data = np.zeros((1, input_size), dtype=np.float32)
        
        for symptom in symptoms:
            if symptom['id'] in self.symptom_mapping:
                index = self.symptom_mapping[symptom['id']]
                severity = self._normalize_severity(symptom.get('severity', 'moderate'))
                input_data[0, index] = severity
                
        return input_data

    def _normalize_severity(self, severity: str) -> float:
        severity_map = {
            'mild': 0.3,
            'moderate': 0.6,
            'severe': 1.0
        }
        return severity_map.get(severity.lower(), 0.6)

    def _postprocess_output(self, output_data: np.ndarray) -> Dict:
        confidence = float(np.max(output_data))
        diagnosis_index = int(np.argmax(output_data))
        
        return {
            'diagnosis': self._get_diagnosis_label(diagnosis_index),
            'confidence': confidence,
            'severity': self._determine_severity(confidence),
            'recommendations': self._get_recommendations(diagnosis_index, confidence)
        }

    def _get_diagnosis_label(self, index: int) -> str:
        # TODO: Implement mapping from model output index to diagnosis label
        return f"Diagnosis_{index}"

    def _determine_severity(self, confidence: float) -> str:
        if confidence > 0.8:
            return 'high'
        elif confidence > 0.5:
            return 'medium'
        return 'low'

    def _get_recommendations(self, diagnosis_index: int, confidence: float) -> List[str]:
        # TODO: Implement recommendation logic based on diagnosis and confidence
        return ["Consult a healthcare professional", "Monitor symptoms"]

diagnostic_model = DiagnosticModel()
