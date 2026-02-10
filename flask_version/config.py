"""
Configuration file for Student Marketplace Flask Application
Contains database settings, upload configuration, and app settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Secret key for session management (change in production)
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production-2024')
    
    # Database configuration
    # Option 1: MySQL
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Aditya@08')
    MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    MYSQL_DB = os.getenv('MYSQL_DB', 'student_marketplace_flask')
    
    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4'
    
    # Option 2: SQLite (for development/testing)
    # Uncomment below and comment MySQL config to use SQLite
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///student_marketplace.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300
    }
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'products')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Pagination
    PRODUCTS_PER_PAGE = 12
    
    # Image settings
    MAX_IMAGES_PER_PRODUCT = 5
    THUMBNAIL_WIDTH = 300
    THUMBNAIL_HEIGHT = 300
    
    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
