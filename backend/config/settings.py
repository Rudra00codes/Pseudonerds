import os
from dotenv import load_dotenv

load_dotenv()

# Base settings
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# API Keys
BHASHINI_API_KEY = os.getenv('BHASHINI_API_KEY')
BHASHINI_API_URL = os.getenv('BHASHINI_API_URL')
ABDM_API_KEY = os.getenv('ABDM_API_KEY')
ABDM_API_URL = os.getenv('ABDM_API_URL')

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3'),
    }
}

# Offline storage configuration
OFFLINE_STORAGE = {
    'MODEL_PATH': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ai/models/diagnostic_model.tflite'),
    'CACHE_DIR': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache/'),
}

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
    'models',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]