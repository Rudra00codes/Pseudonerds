from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token

bcrypt = Bcrypt()
jwt = JWTManager()

def init_user_service(app):
    bcrypt.init_app(app)
    jwt.init_app(app)

def authenticate_user(username, password):
    # This is a placeholder. In a real application, you would check against a database
    if username == "test" and password == "password":
        return True
    return False

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password)

def create_token(user_id):
    return create_access_token(identity=user_id)

