from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os
from dotenv import load_dotenv

from services.auth_service import AuthService
from services.diagnostic_service import DiagnosticService
from services.bhashini_service import BhashiniService
from services.abdm_service import ABDMService
from models.database import db

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
jwt = JWTManager(app)
db.init_app(app)

# Initialize services
auth_service = AuthService()
diagnostic_service = DiagnosticService()
bhashini_service = BhashiniService()
abdm_service = ABDMService()

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if auth_service.verify_credentials(data.get('username'), data.get('password')):
        access_token = create_access_token(identity=data.get('username'))
        return jsonify({'token': access_token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/diagnose', methods=['POST'])
@jwt_required()
def diagnose():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Translate symptoms if language is specified
        if 'language' in data:
            translated_symptoms = bhashini_service.translate_text(
                data['symptoms'],
                source_lang=data['language'],
                target_lang='en'
            )
        else:
            translated_symptoms = data['symptoms']
        
        # Get diagnosis
        diagnosis = diagnostic_service.process_symptoms(translated_symptoms)
        
        # Store diagnosis in user's health record
        abdm_service.store_diagnosis(user_id, diagnosis)
        
        return jsonify(diagnosis), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/health-records', methods=['GET'])
@jwt_required()
def get_health_records():
    try:
        user_id = get_jwt_identity()
        records = abdm_service.get_health_records(user_id)
        return jsonify(records), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/translate', methods=['POST'])
@jwt_required()
def translate():
    try:
        data = request.get_json()
        translated_text = bhashini_service.translate_text(
            data['text'],
            source_lang=data['source_lang'],
            target_lang=data['target_lang']
        )
        return jsonify({'translated_text': translated_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)