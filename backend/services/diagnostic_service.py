from typing import List, Dict, Any
import os
import json
import numpy as np
import tensorflow as tf

class DiagnosticService:
    def __init__(self):
        # Define model paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_dir, 'ai/models/diagnostic_model.tflite')
        self.symptom_mapping_path = os.path.join(base_dir, 'ai/models/symptom_mapping.json')
        self.condition_mapping_path = os.path.join(base_dir, 'ai/models/condition_mapping.json')
        
        # Initialize model and mappings
        self.interpreter = None
        self.symptom_mapping = {}
        self.conditions = []
        
        # Load model and mappings
        self.load_model()
        self.load_mappings()
    
    def load_model(self):
        """Load the TensorFlow Lite model"""
        try:
            self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.interpreter = None
    
    def load_mappings(self):
        """Load symptom and condition mappings"""
        try:
            with open(self.symptom_mapping_path, 'r') as f:
                self.symptom_mapping = json.load(f)
            
            with open(self.condition_mapping_path, 'r') as f:
                self.conditions = json.load(f)
            
            print("Mappings loaded successfully")
        except Exception as e:
            print(f"Error loading mappings: {e}")
    
    def process_symptoms(self, symptoms: List[str], language: str = "en") -> Dict[str, Any]:
        """Process symptoms and return diagnosis"""
        try:
            # Preprocess symptoms
            input_data = self.preprocess_symptoms(symptoms)
            
            # If model is available, use it for inference
            if self.interpreter:
                # Reshape input data to match model's expected shape
                input_data = np.expand_dims(input_data, axis=0).astype(np.float32)
                
                # Set input tensor
                self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
                
                # Run inference
                self.interpreter.invoke()
                
                # Get output tensor
                output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
                
                # Get top prediction
                top_index = np.argmax(output_data[0])
                confidence = float(output_data[0][top_index])
                
                diagnosis = self.conditions[top_index]
                severity = self._determine_severity(diagnosis, symptoms)
                
                return {
                    "diagnosis": diagnosis,
                    "confidence": confidence,
                    "severity": severity,
                    "recommendations": self._get_recommendations(diagnosis)
                }
            else:
                # Fallback to rule-based approach
                return self.rule_based_diagnosis(symptoms)
        except Exception as e:
            print(f"Error in process_symptoms: {e}")
            return {"diagnosis": "Unable to process symptoms", "confidence": 0.0, "severity": "LOW"}
    
    def preprocess_symptoms(self, symptoms: List[str]) -> np.ndarray:
        """Convert symptoms to model input format"""
        # Create a one-hot encoded vector
        input_vector = np.zeros(50, dtype=np.float32)
        
        for symptom in symptoms:
            symptom = symptom.lower()
            if symptom in self.symptom_mapping:
                input_vector[self.symptom_mapping[symptom]] = 1.0
        
        return input_vector
    
    def rule_based_diagnosis(self, symptoms: List[str]) -> Dict[str, Any]:
        """Fallback rule-based diagnostic approach"""
        symptoms_lower = [s.lower() for s in symptoms]
        
        # Simple rule-based logic
        if "fever" in symptoms_lower and "cough" in symptoms_lower:
            if "shortness of breath" in symptoms_lower:
                return {
                    "diagnosis": "Possible Pneumonia",
                    "confidence": 0.75,
                    "severity": "HIGH",
                    "recommendations": ["Seek medical attention", "Rest", "Stay hydrated"]
                }
            else:
                return {
                    "diagnosis": "Common Cold or Influenza",
                    "confidence": 0.85,
                    "severity": "MEDIUM",
                    "recommendations": ["Rest", "Fluids", "Over-the-counter medication"]
                }
        
        if "headache" in symptoms_lower and "nausea" in symptoms_lower:
            return {
                "diagnosis": "Possible Migraine",
                "confidence": 0.70,
                "severity": "MEDIUM",
                "recommendations": ["Rest in dark room", "Stay hydrated", "Pain relievers"]
            }
        
        # Default response
        return {
            "diagnosis": "Unspecified Condition",
            "confidence": 0.50,
            "severity": "LOW",
            "recommendations": ["Monitor symptoms", "Consult with healthcare provider if symptoms persist"]
        }
    
    def _determine_severity(self, condition: str, symptoms: List[str]) -> str:
        """Determine severity based on condition and symptoms"""
        high_risk_symptoms = ["shortness of breath", "chest pain", "confusion", "severe pain"]
        
        # Check for high-risk symptoms
        for symptom in symptoms:
            if symptom.lower() in high_risk_symptoms:
                return "HIGH"
        
        # Condition-based severity
        high_severity_conditions = ["Pneumonia", "Asthma"]
        medium_severity_conditions = ["Influenza", "Hypertension", "Type 2 Diabetes"]
        
        if any(cond in condition for cond in high_severity_conditions):
            return "HIGH"
        elif any(cond in condition for cond in medium_severity_conditions):
            return "MEDIUM"
        
        return "LOW"
    
    def _get_recommendations(self, diagnosis: str) -> List[str]:
        """Get recommendations based on diagnosis"""
        recommendations = {
            "Common Cold": ["Rest", "Stay hydrated", "Over-the-counter cold medication if needed"],
            "Influenza": ["Rest", "Fluids", "Fever reducers", "Consult doctor if symptoms worsen"],
            "Hypertension": ["Reduce salt intake", "Regular exercise", "Medication as prescribed"],
            "Type 2 Diabetes": ["Monitor blood sugar", "Follow prescribed diet", "Regular exercise"],
            "Migraine": ["Rest in dark room", "Stay hydrated", "Pain relievers"],
            "Gastroenteritis": ["Stay hydrated", "BRAT diet", "Rest"],
            "Urinary Tract Infection": ["Increase fluid intake", "Consult doctor for antibiotics"],
            "Asthma": ["Use prescribed inhaler", "Avoid triggers", "Seek medical help if breathing worsens"],
            "Allergic Rhinitis": ["Avoid allergens", "Antihistamines", "Nasal sprays"],
            "Anxiety Disorder": ["Deep breathing exercises", "Regular physical activity", "Consider counseling"]
        }
        
        if diagnosis in recommendations:
            return recommendations[diagnosis]
        
        return ["Monitor symptoms", "Consult with healthcare provider if symptoms persist"]