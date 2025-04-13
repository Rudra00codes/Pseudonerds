import numpy as np
import tensorflow as tf
import json
import os
import sys

# Define paths directly instead of using Django settings
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai', 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'diagnostic_model.tflite')

def create_placeholder_model():
    """Create a simple model for symptom-based diagnostics"""
    # Input: Symptom features (50 possible symptoms as one-hot encoded)
    inputs = tf.keras.Input(shape=(50,), name="symptoms")
    
    # Simple neural network
    x = tf.keras.layers.Dense(32, activation="relu")(inputs)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(16, activation="relu")(x)
    
    # Output: Probability distribution over 10 common conditions
    outputs = tf.keras.layers.Dense(10, activation="softmax", name="diagnosis")(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    return model

def create_mappings():
    """Create symptom and condition mappings"""
    symptoms = [
        "fever", "cough", "headache", "fatigue", "sore throat",
        "runny nose", "body aches", "chills", "nausea", "vomiting",
        "diarrhea", "shortness of breath", "chest pain", "dizziness", "rash",
        "joint pain", "back pain", "abdominal pain", "loss of appetite", "weight loss",
        "increased thirst", "frequent urination", "blurred vision", "numbness", "tingling",
        "swelling", "itching", "sneezing", "wheezing", "congestion",
        "ear pain", "eye pain", "vision changes", "hearing changes", "difficulty swallowing",
        "hoarseness", "muscle weakness", "confusion", "memory problems", "anxiety",
        "depression", "insomnia", "excessive sweating", "dry mouth", "excessive hunger",
        "blood in stool", "blood in urine", "irregular heartbeat", "fainting", "seizures"
    ]
    
    conditions = [
        "Common Cold",
        "Influenza",
        "Hypertension",
        "Type 2 Diabetes",
        "Migraine",
        "Gastroenteritis",
        "Urinary Tract Infection",
        "Asthma",
        "Allergic Rhinitis",
        "Anxiety Disorder"
    ]
    
    symptom_mapping = {symptom: i for i, symptom in enumerate(symptoms)}
    
    return symptom_mapping, conditions

def main():
    # Create model directory if it doesn't exist
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Create and save the model
    print("Creating model...")
    model = create_placeholder_model()
    model.summary()
    
    # Convert to TFLite
    print("Converting to TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    # Save the TFLite model
    with open(MODEL_PATH, 'wb') as f:
        f.write(tflite_model)
    print(f"TFLite model saved to {MODEL_PATH}")
    
    # Create and save mappings
    print("Creating mappings...")
    symptom_mapping, conditions = create_mappings()
    
    symptom_path = os.path.join(MODEL_DIR, 'symptom_mapping.json')
    condition_path = os.path.join(MODEL_DIR, 'condition_mapping.json')
    
    with open(symptom_path, 'w') as f:
        json.dump(symptom_mapping, f, indent=2)
    print(f"Symptom mapping saved to {symptom_path}")
    
    with open(condition_path, 'w') as f:
        json.dump(conditions, f, indent=2)
    print(f"Condition mapping saved to {condition_path}")
    
    print("Model setup complete!")

if __name__ == "__main__":
    main()