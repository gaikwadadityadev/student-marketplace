"""
Configuration file for Student Marketplace Flask Application
Enhanced with comprehensive security settings
"""
import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _mysql_uri() -> str:
    """
    Construct MySQL database URI from environment variables
    Uses PyMySQL driver for MySQL connectivity
    """
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', 'root')
    host = os.getenv('MYSQL_HOST', '127.0.0.1')
    port = os.getenv('MYSQL_PORT', '3306')
    database = os.getenv('MYSQL_DB', 'student_marketplace')
    # URL-encode special chars in password
    from urllib.parse import quote_plus
    return f'mysql+pymysql://{user}:{quote_plus(password)}@{host}:{port}/{database}?charset=utf8mb4'


class Config:
    """Application configuration class with enhanced security"""
    
    # ==================== DATABASE CONFIGURATION ====================
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', _mysql_uri())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # ==================== SECRET KEYS ====================
    # Generate secure secret key: python -c "import secrets; print(secrets.token_hex(32))"
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', secrets.token_hex(32))
    
    # ==================== CSRF PROTECTION ====================
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No expiration for CSRF tokens
    WTF_CSRF_SSL_STRICT = os.getenv('FLASK_ENV') == 'production'
    WTF_CSRF_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']
    
    # ==================== SESSION SECURITY ====================
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    SESSION_COOKIE_NAME = 'student_marketplace_session'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_REFRESH_EACH_REQUEST = True
    
    # ==================== RATE LIMITING ====================
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True') == 'True'
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = '200 per hour'
    RATELIMIT_HEADERS_ENABLED = True
    
    # ==================== FILE UPLOAD CONFIGURATION ====================
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # ==================== SECURITY HEADERS ====================
    # Enable security headers
    TALISMAN_ENABLED = os.getenv('FLASK_ENV') != 'development'
    TALISMAN_FORCE_HTTPS = os.getenv('FLASK_ENV') == 'production'
    
    # Content Security Policy
    CONTENT_SECURITY_POLICY = {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            "'unsafe-inline'",  # Required for inline scripts
            'https://cdn.jsdelivr.net',
            'https://code.jquery.com',
            'https://stackpath.bootstrapcdn.com',
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",  # Required for inline styles
            'https://fonts.googleapis.com',
            'https://cdn.jsdelivr.net',
            'https://stackpath.bootstrapcdn.com',
        ],
        'font-src': [
            "'self'",
            'https://fonts.gstatic.com',
            'https://cdn.jsdelivr.net',
        ],
        'img-src': [
            "'self'",
            'data:',
            'https:',
        ],
        'connect-src': ["'self'"],
    }
    
    # ==================== CORS CONFIGURATION ====================
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # ==================== PASSWORD POLICY ====================
    MIN_PASSWORD_LENGTH = 8
    REQUIRE_PASSWORD_COMPLEXITY = True
    
    # ==================== LOGIN SECURITY ====================
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_ATTEMPT_TIMEOUT = 900  # 15 minutes in seconds
    
    # ==================== INPUT SANITIZATION ====================
    BLEACH_ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
    BLEACH_ALLOWED_ATTRIBUTES = {}
    
    # ==================== ENVIRONMENT ====================
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
