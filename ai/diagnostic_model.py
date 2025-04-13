import os
import json
import numpy as np
import tensorflow as tf

class DiagnosticModel:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), 'models/diagnostic_model.tflite')
        self.symptom_mapping_path = os.path.join(os.path.dirname(__file__), 'models/symptom_mapping.json')
        self.condition_mapping_path = os.path.join(os.path.dirname(__file__), 'models/condition_mapping.json')
        
        # Load the TFLite model
        self.interpreter = None
        self.load_model()
        
        # Load mappings
        self.load_mappings()
    
    def load_model(self):
        """Load the TFLite model"""
        try:
            self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback to rule-based inference if model fails to load
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
            self.symptom_mapping = {}
            self.conditions = []
    
    def preprocess_symptoms(self, symptoms):
        """Convert symptom text to model input format"""
        # Create a one-hot encoded vector
        input_vector = np.zeros(50, dtype=np.float32)
        
        for symptom in symptoms:
            symptom = symptom.lower()
            if symptom in self.symptom_mapping:
                input_vector[self.symptom_mapping[symptom]] = 1.0
        
        return input_vector
    
    def diagnose(self, symptoms):
        """Perform diagnosis based on symptoms"""
        # Preprocess symptoms
        input_data = self.preprocess_symptoms(symptoms)
        
        # If model is available, use it
        if self.interpreter:
            try:
                # Reshape input data to match model's expected shape
                input_data = np.expand_dims(input_data, axis=0).astype(np.float32)
                
                # Set input tensor
                self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
                
                # Run inference
                self.interpreter.invoke()
                
                # Get output tensor
                output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
                
                # Get top 3 predictions
                top_indices = np.argsort(output_data[0])[-3:][::-1]
                top_probs = output_data[0][top_indices]
                
                results = []
                for i, idx in enumerate(top_indices):
                    results.append({
                        "diagnosis": self.conditions[idx],
                        "confidence": float(top_probs[i]),
                        "severity": self._determine_severity(self.conditions[idx], symptoms)
                    })
                
                return results
            except Exception as e:
                print(f"Error during model inference: {e}")
                # Fall back to rule-based approach
                return self.rule_based_diagnosis(symptoms)
        else:
            # Use rule-based approach if model isn't available
            return self.rule_based_diagnosis(symptoms)
    
    def rule_based_diagnosis(self, symptoms):
        """Fallback rule-based diagnostic approach"""
        symptoms_lower = [s.lower() for s in symptoms]
        
        # Simple rule-based logic (for demonstration)
        if "fever" in symptoms_lower and "cough" in symptoms_lower:
            if "shortness of breath" in symptoms_lower:
                return [{
                    "diagnosis": "Possible Pneumonia",
                    "confidence": 0.75,
                    "severity": "high",
                    "recommendations": ["Seek medical attention", "Rest", "Stay hydrated"]
                }]
            else:
                return [{
                    "diagnosis": "Common Cold or Influenza",
                    "confidence": 0.85,
                    "severity": "medium",
                    "recommendations": ["Rest", "Fluids", "Over-the-counter medication"]
                }]
        
        if "headache" in symptoms_lower and "nausea" in symptoms_lower:
            return [{
                "diagnosis": "Possible Migraine",
                "confidence": 0.70,
                "severity": "medium",
                "recommendations": ["Rest in dark room", "Stay hydrated", "Pain relievers"]
            }]
        
        # Default response if no rules match
        return [{
            "diagnosis": "Unspecified Condition",
            "confidence": 0.50,
            "severity": "low",
            "recommendations": ["Monitor symptoms", "Consult with healthcare provider if symptoms persist"]
        }]
    
    def _determine_severity(self, condition, symptoms):
        """Determine severity based on condition and symptoms"""
        high_risk_symptoms = ["shortness of breath", "chest pain", "confusion", "severe pain"]
        
        # Check for high-risk symptoms
        for symptom in symptoms:
            if symptom.lower() in high_risk_symptoms:
                return "high"
        
        # Condition-based severity
        high_severity_conditions = ["Pneumonia", "Asthma"]
        medium_severity_conditions = ["Influenza", "Hypertension", "Type 2 Diabetes"]
        
        if any(cond in condition for cond in high_severity_conditions):
            return "high"
        elif any(cond in condition for cond in medium_severity_conditions):
            return "medium"
        
        return "low"

# Singleton instance
_model_instance = None

def init_diagnostic_model(app):
    """Initialize the diagnostic model and attach it to the Flask app"""
    global _model_instance
    _model_instance = DiagnosticModel()
    app.config['DIAGNOSTIC_MODEL'] = _model_instance
    return _model_instance

def get_model():
    """Get the singleton instance of the diagnostic model"""
    global _model_instance
    if _model_instance is None:
        _model_instance = DiagnosticModel()
    return _model_instance
