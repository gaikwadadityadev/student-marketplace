"""
Security Utilities for Student Marketplace
Provides input sanitization, validation, and security helpers
"""
import re
import bleach
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta

class SecurityUtils:
    """Security utility functions"""
    
    # Login attempt tracking (in-memory, should use Redis in production)
    login_attempts = {}
    
    @staticmethod
    def sanitize_html(text):
        """Sanitize HTML input to prevent XSS attacks"""
        if not text:
            return text
        # Allow only safe tags
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
        return bleach.clean(text, tags=allowed_tags, strip=True)
    
    @staticmethod
    def sanitize_input(text):
        """Sanitize general text input"""
        if not text:
            return text
        # Remove all HTML tags
        return bleach.clean(text, tags=[], strip=True)
    
    @staticmethod
    def validate_email_format(email):
        """Validate email format"""
        try:
            valid = validate_email(email, check_deliverability=False)
            return True, valid.email
        except EmailNotValidError as e:
            return False, str(e)
    
    @staticmethod
    def validate_password_strength(password):
        """
        Validate password strength
        Returns: (is_valid, error_message, strength_score)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long", 0
        
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        
        # Complexity checks
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if re.search(r'[0-9]', password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        if re.search(r'[^a-zA-Z0-9]', password):
            score += 1
        else:
            feedback.append("Add special characters")
        
        # Determine if password meets minimum requirements
        if score < 3:
            return False, f"Password too weak. {', '.join(feedback)}", score
        
        return True, "Password is strong", score
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        if not phone:
            return True  # Phone is optional
        
        # Remove common separators
        clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
        
        # Check if it's a valid phone number (10-15 digits)
        if re.match(r'^\d{10,15}$', clean_phone):
            return True
        return False
    
    @staticmethod
    def validate_username(username):
        """Validate username format"""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(username) > 30:
            return False, "Username must be less than 30 characters"
        
        # Allow only alphanumeric and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, "Valid username"
    
    @staticmethod
    def check_login_attempts(identifier):
        """
        Check if login attempts have exceeded limit
        Args:
            identifier: IP address or username
        Returns:
            (is_allowed, attempts_left, wait_time)
        """
        now = datetime.now()
        
        if identifier not in SecurityUtils.login_attempts:
            return True, 5, 0
        
        attempt_data = SecurityUtils.login_attempts[identifier]
        attempts = attempt_data['count']
        last_attempt = attempt_data['timestamp']
        
        # Reset if timeout has passed
        if (now - last_attempt).total_seconds() > 900:  # 15 minutes
            del SecurityUtils.login_attempts[identifier]
            return True, 5, 0
        
        # Check if locked out
        if attempts >= 5:
            wait_time = 900 - int((now - last_attempt).total_seconds())
            return False, 0, wait_time
        
        return True, 5 - attempts, 0
    
    @staticmethod
    def record_login_attempt(identifier, success=False):
        """
        Record a login attempt
        Args:
            identifier: IP address or username
            success: Whether the login was successful
        """
        now = datetime.now()
        
        if success:
            # Clear attempts on successful login
            if identifier in SecurityUtils.login_attempts:
                del SecurityUtils.login_attempts[identifier]
        else:
            # Increment failed attempts
            if identifier not in SecurityUtils.login_attempts:
                SecurityUtils.login_attempts[identifier] = {
                    'count': 1,
                    'timestamp': now
                }
            else:
                SecurityUtils.login_attempts[identifier]['count'] += 1
                SecurityUtils.login_attempts[identifier]['timestamp'] = now
    
    @staticmethod
    def validate_file_upload(filename, file_size=None, max_size=16*1024*1024):
        """
        Validate file upload
        Args:
            filename: Name of the file
            file_size: Size of file in bytes
            max_size: Maximum allowed size
        Returns:
            (is_valid, error_message)
        """
        if not filename:
            return False, "No file provided"
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if '.' not in filename:
            return False, "File must have an extension"
        
        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in allowed_extensions:
            return False, f"File type .{ext} not allowed. Allowed: {', '.join(allowed_extensions)}"
        
        # Check file size if provided
        if file_size and file_size > max_size:
            max_mb = max_size / (1024 * 1024)
            return False, f"File too large. Maximum size: {max_mb}MB"
        
        return True, "File is valid"
    
    @staticmethod
    def get_client_ip(request):
        """Get the client's real IP address"""
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        return request.remote_addr or 'unknown'
