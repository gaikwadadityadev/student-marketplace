
+"""
Configuration file for Student Marketplace Flask Application
Production-hardened with fixed SECRET_KEY and proper env var loading
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _mysql_uri() -> str:
        """
            Construct MySQL database URI from environment variables.
                Supports both MYSQL_* (Render convention) and MYSQLHOST etc. (Railway convention).
                    """
        from urllib.parse import quote_plus

    # Try Render-style first, then Railway-style
        user     = os.getenv('MYSQL_USER')     or os.getenv('MYSQLUSER', 'root')
        password = os.getenv('MYSQL_PASSWORD') or os.getenv('MYSQLPASSWORD', '')
        host     = os.getenv('MYSQL_HOST')     or os.getenv('MYSQLHOST', '127.0.0.1')
        port     = os.getenv('MYSQL_PORT')     or os.getenv('MYSQLPORT', '3306')
        database = os.getenv('MYSQL_DB')       or os.getenv('MYSQLDATABASE', 'student_marketplace')

    return (
                f'mysql+pymysql://{user}:{quote_plus(str(password))}'
                f'@{host}:{port}/{database}?charset=utf8mb4'
    )


def _get_db_uri() -> str:
        db_url = os.getenv('DATABASE_URL')
        mysql_host = os.getenv('MYSQL_HOST') or os.getenv('MYSQLHOST')

    if db_url and not any(p in db_url.lower() for p in ['your_', 'placeholder']):
                if db_url.startswith('postgres://'):
                                db_url = db_url.replace('postgres://', 'postgresql://', 1)
                            if db_url.startswith('postgresql://') and 'sslmode=' not in db_url:
                                            if '?' in db_url:
                                                                db_url += '&sslmode=require'
                            else:
                db_url += '?sslmode=require'
        return db_url
elif mysql_host and not any(p in mysql_host.lower() for p in ['your_', 'placeholder']):
        return _mysql_uri()
else:
        db_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'student_marketplace.db'))
        # SQLAlchemy requires forward slashes even on Windows for sqlite absolute paths
        db_path_posix = db_path.replace('\\', '/')
        return f'sqlite:///{db_path_posix}'


class Config:
        """Application configuration class - production-hardened"""

    SQLALCHEMY_DATABASE_URI = _get_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS    = {
                'pool_pre_ping': True,
                'pool_recycle': 300,
                'pool_timeout': 30,
                'pool_size': 5,
                'max_overflow': 10,
    }

    # ==================== SECRET KEYS ====================
    # CRITICAL: Must be a FIXED value in production.
    # secrets.token_hex(32) rotates on every restart -> sessions break.
    SECRET_KEY = os.getenv(
                'SECRET_KEY',
                'StudentMarketplace-SuperSecret-2024-FixedKey-DoNotChange'
    )
    WTF_CSRF_SECRET_KEY = os.getenv(
                'WTF_CSRF_SECRET_KEY',
                'StudentMarketplace-CSRF-2024-FixedKey'
    )

    # ==================== CSRF ====================
    WTF_CSRF_ENABLED    = True
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_SSL_STRICT = False   # Keep False - form tokens handled separately
    WTF_CSRF_METHODS    = ['POST', 'PUT', 'PATCH', 'DELETE']

    # ==================== SESSION ====================
    SESSION_COOKIE_SECURE   = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME     = 'student_marketplace_session'
    PERMANENT_SESSION_LIFETIME   = timedelta(hours=24)
    SESSION_REFRESH_EACH_REQUEST = True

    # ==================== FILE UPLOADS ====================
    UPLOAD_FOLDER       = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads'
    )
    MAX_CONTENT_LENGTH  = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    ALLOWED_EXTENSIONS  = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # ==================== RATE LIMITING ====================
    RATELIMIT_ENABLED     = os.getenv('RATELIMIT_ENABLED', 'True') == 'True'
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_STRATEGY    = 'fixed-window'
    RATELIMIT_DEFAULT     = '200 per hour'
    RATELIMIT_HEADERS_ENABLED = True

    # ==================== CORS ====================
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

    # ==================== SECURITY HEADERS ====================
    TALISMAN_ENABLED    = False   # Disabled - Render handles HTTPS termination
    TALISMAN_FORCE_HTTPS = False

    # ==================== ENVIRONMENT ====================
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG     = os.getenv('FLASK_DEBUG', 'False') == 'True'

    # ==================== INPUT SANITIZATION ====================
    BLEACH_ALLOWED_TAGS       = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
    BLEACH_ALLOWED_ATTRIBUTES = {}

    # ==================== PASSWORD POLICY ====================
    MIN_PASSWORD_LENGTH       = 6
    REQUIRE_PASSWORD_COMPLEXITY = True

    # ==================== LOGIN SECURITY ====================
    MAX_LOGIN_ATTEMPTS    = 10
    LOGIN_ATTEMPT_TIMEOUT = 900
