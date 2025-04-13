from flask import Blueprint, request, jsonify
from ai.diagnostic_model import get_model

api_bp = Blueprint('api', __name__)

@api_bp.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400
        
        # Get diagnosis from model
        model = get_model()
        results = model.diagnose(symptoms)
        
        return jsonify(results)
    
    except Exception as e:
        print(f"Error in diagnosis: {e}")
        return jsonify({"error": "Failed to process diagnosis"}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200