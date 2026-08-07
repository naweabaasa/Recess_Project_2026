import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SECRET_KEY is used by Flask to sign cookies and sessions.
    # NEVER use a simple string like "change-me" in production!
    # os.environ.get() tries to read from environment variables first.
    # If not found, os.urandom(32).hex() generates a random 64-character string.
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32).hex()
    
    # Database connection settings
    # These read from environment variables, with defaults for local development
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "bread_wise_db")
    
    # This creates the full database connection URL
    # Format: mysql+pymysql://username:password@host/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    
    # Disable tracking modifications to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT_SECRET_KEY is used to sign authentication tokens.
    # This should be different from SECRET_KEY for better security.
    # Again, NEVER use "change-me-jwt" in production!
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or os.urandom(32).hex()
    
    # JWT Token Expiration Settings
    # How long before access tokens expire and users need to login again
    # timedelta(hours=1) means tokens expire after 1 hour
    # This prevents old tokens from being used forever (security!)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Refresh tokens last longer - used to get new access tokens without logging in again
    # timedelta(days=30) means refresh tokens last for 30 days
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Folder where uploaded files will be stored
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": Config,
}



