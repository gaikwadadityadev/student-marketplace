"""
Enhanced Security Configuration for Student Marketplace
Implements CSRF protection, rate limiting, and security headers
"""
import os
from datetime import timedelta

class SecurityConfig:
    """Security-focused configuration"""
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF token
    WTF_CSRF_SSL_STRICT = False  # Set to True in production with HTTPS
    
    # Session Security
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Rate Limiting Configuration
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_DEFAULT = "200 per hour"
    
    # Security Headers (Content Security Policy)
    TALISMAN_CONFIG = {
        'force_https': False,  # Set to True in production
        'strict_transport_security': True,
        'strict_transport_security_max_age': 31536000,
        'content_security_policy': {
            'default-src': "'self'",
            'script-src': [
                "'self'",
                "'unsafe-inline'",  # Needed for inline scripts
                "https://cdn.jsdelivr.net",
                "https://code.jquery.com",
                "https://stackpath.bootstrapcdn.com",
                "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0"
            ],
            'style-src': [
                "'self'",
                "'unsafe-inline'",  # Needed for inline styles
                "https://fonts.googleapis.com",
                "https://cdn.jsdelivr.net",
                "https://stackpath.bootstrapcdn.com"
            ],
            'font-src': [
                "'self'",
                "https://fonts.gstatic.com",
                "https://cdn.jsdelivr.net"
            ],
            'img-src': [
                "'self'",
                "data:",
                "https:"
            ],
            'connect-src': "'self'"
        },
        'content_security_policy_nonce_in': ['script-src'],
        'feature_policy': {
            'geolocation': "'none'",
            'microphone': "'none'",
            'camera': "'none'"
        }
    }
    
    # File Upload Security
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Password Policy
    MIN_PASSWORD_LENGTH = 8
    REQUIRE_PASSWORD_COMPLEXITY = True
    
    # Login Security
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_ATTEMPT_TIMEOUT = 900  # 15 minutes in seconds
    
    # Input Sanitization
    BLEACH_ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
    BLEACH_ALLOWED_ATTRIBUTES = {}
