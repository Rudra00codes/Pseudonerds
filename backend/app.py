from flask import Flask, request, jsonify
from flask_cors import CORS
from ai.diagnostic_model import DiagnosticModel

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400
        
        # TODO: Initialize and use the ML model here
        # For now, return mock data
        mock_result = {
            "diagnosis": "Common Cold",
            "confidence": 0.85,
            "severity": "LOW",
            "recommendations": [
                "Rest well",
                "Stay hydrated",
                "Take over-the-counter cold medicine"
            ]
        }
        
        return jsonify(mock_result)
    
    except Exception as e:
        print(f"Error in diagnosis: {e}")
        return jsonify({"error": "Failed to process diagnosis"}), 500

if __name__ == '__main__':
    app.run(debug=True)