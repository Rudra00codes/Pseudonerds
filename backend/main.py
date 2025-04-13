from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import the diagnostic service
try:
    from services.diagnostic_service import DiagnosticService
    diagnostic_service = DiagnosticService()
    model_available = True
except Exception as e:
    print(f"Warning: Could not load diagnostic service: {e}")
    model_available = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Add a secret key for JWT
CORS(app)  # Enable CORS for all routes

# Try to initialize user service
try:
    from services.user_service import init_user_service
    init_user_service(app)
    user_service_available = True
    print("User service initialized successfully")
except ImportError as e:
    print(f"Warning: Could not import user service: {e}")
    user_service_available = False
except Exception as e:
    print(f"Warning: Could not initialize user service: {e}")
    user_service_available = False

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok", 
        "model_available": model_available,
        "user_service_available": user_service_available
    })

@app.route('/api/diagnose/test', methods=['POST'])
def diagnose_test():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        language = data.get('language', 'en')
        
        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400
        
        if model_available:
            # Use the diagnostic service if available
            result = diagnostic_service.process_symptoms(symptoms, language)
            return jsonify(result)
        else:
            # Fallback response if model is not available
            return jsonify({
                "diagnosis": "Test Diagnosis (Model Unavailable)",
                "confidence": 0.85,
                "severity": "MEDIUM",
                "recommendations": ["This is a test response", "The actual model is not available"]
            })
    
    except Exception as e:
        print(f"Error in diagnosis: {e}")
        return jsonify({"error": "Failed to process diagnosis"}), 500

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)