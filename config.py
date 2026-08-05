import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "change-me"
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "bread_wise_db")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "change-me-jwt"
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



