from flask import Flask
from flask_cors import CORS
from routes import api_bp
from services.user_service import init_user_service
from ai.diagnostic_model import init_diagnostic_model

app = Flask(__name__)
CORS(app)

# Register API routes
app.register_blueprint(api_bp, url_prefix='/api')

# Initialize services
init_user_service(app)
init_diagnostic_model(app)

if __name__ == '__main__':
    app.run(debug=True)

