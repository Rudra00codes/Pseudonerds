import sys
import os
import numpy as np

# Add the parent directory to the path so we can import the services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.diagnostic_service import DiagnosticService

def test_model_loading():
    """Test that the model loads correctly"""
    model = DiagnosticService()
    
    # Check if model and mappings were loaded
    assert hasattr(model, 'interpreter'), "Model interpreter not found"
    assert model.interpreter is not None, "Model failed to load"
    assert hasattr(model, 'symptom_mapping'), "Symptom mapping not found"
    assert hasattr(model, 'conditions'), "Condition mapping not found"
    print("✓ Model loading test passed")

def test_symptom_preprocessing():
    """Test symptom preprocessing"""
    model = DiagnosticService()
    symptoms = ["fever", "cough", "headache"]
    input_vector = model.preprocess_symptoms(symptoms)
    
    # Check that the vector has the right shape
    assert input_vector.shape == (50,), f"Expected shape (50,), got {input_vector.shape}"
    
    # Check that the right indices are set to 1
    for symptom in symptoms:
        if symptom in model.symptom_mapping:
            assert input_vector[model.symptom_mapping[symptom]] == 1.0, f"Expected 1.0 for {symptom}"
    
    # Count the number of 1s (should equal the number of valid symptoms)
    valid_symptoms = [s for s in symptoms if s in model.symptom_mapping]
    assert sum(input_vector) == len(valid_symptoms), f"Expected {len(valid_symptoms)} symptoms, got {sum(input_vector)}"
    
    print("✓ Symptom preprocessing test passed")

def test_diagnosis():
    """Test the diagnosis functionality"""
    model = DiagnosticService()
    
    # Test with common cold symptoms
    cold_symptoms = ["fever", "cough", "runny nose", "sore throat"]
    cold_results = model.process_symptoms(cold_symptoms)
    assert isinstance(cold_results, dict), "Result should be a dictionary"
    assert "diagnosis" in cold_results, "Result should contain a diagnosis"
    assert "confidence" in cold_results, "Result should contain a confidence score"
    assert "severity" in cold_results, "Result should contain a severity level"
    print(f"Cold symptoms diagnosis: {cold_results['diagnosis']} (confidence: {cold_results['confidence']:.2f})")
    
    # Test with diabetes symptoms
    diabetes_symptoms = ["increased thirst", "frequent urination", "weight loss", "fatigue"]
    diabetes_results = model.process_symptoms(diabetes_symptoms)
    assert isinstance(diabetes_results, dict), "Result should be a dictionary"
    assert "diagnosis" in diabetes_results, "Result should contain a diagnosis"
    print(f"Diabetes symptoms diagnosis: {diabetes_results['diagnosis']} (confidence: {diabetes_results['confidence']:.2f})")
    
    # Test with unknown symptoms
    unknown_symptoms = ["unknown_symptom1", "unknown_symptom2"]
    unknown_results = model.process_symptoms(unknown_symptoms)
    assert isinstance(unknown_results, dict), "Result should be a dictionary"
    assert "diagnosis" in unknown_results, "Result should contain a diagnosis"
    print(f"Unknown symptoms diagnosis: {unknown_results['diagnosis']} (confidence: {unknown_results['confidence']:.2f})")
    
    print("✓ Diagnosis test passed")

def test_severity_determination():
    """Test severity determination"""
    model = DiagnosticService()
    
    # Test high severity
    high_severity = model._determine_severity("Pneumonia", ["shortness of breath", "fever"])
    assert high_severity == "HIGH", f"Expected 'HIGH', got '{high_severity}'"
    
    # Test medium severity
    medium_severity = model._determine_severity("Influenza", ["fever", "cough"])
    assert medium_severity == "MEDIUM", f"Expected 'MEDIUM', got '{medium_severity}'"
    
    # Test low severity
    low_severity = model._determine_severity("Common Cold", ["runny nose"])
    assert low_severity == "LOW", f"Expected 'LOW', got '{low_severity}'"
    
    print("✓ Severity determination test passed")

if __name__ == "__main__":
    print("Running diagnostic model tests...")
    test_model_loading()
    test_symptom_preprocessing()
    test_diagnosis()
    test_severity_determination()
    print("All tests passed!")