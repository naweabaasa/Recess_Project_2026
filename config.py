import os 
from datetime import timedelta   


BASE_DIR = os.path.abspath(os.path.dirname(__file__))     


class Config:     
     """Base config shared by every environment."""     
     SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-prod")

     SQLALCHEMY_DATABASE_URI = os.environ.get(         
          "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"    
      )     
     SQLALCHEMY_TRACK_MODIFICATIONS = False       
     
     
     JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-me-jwt-secret")     
     JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)     
     JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)     
     JWT_TOKEN_LOCATION = ["headers"]       
     
     
     UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")     
     MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB uploads       
     
     
     # comma separated list of allowed origins for the React site + admin dashboard     
     CORS_ORIGINS = os.environ.get(         
          "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"     
     ).split(",")     
     
     
     class DevelopmentConfig(Config):     
          
          DEBUG = True     
     
     
     
     class ProductionConfig(Config):     
          DEBUG = False     
          
     
     class TestingConfig(Config):     
          TESTING = True     
          SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"     
          
          
     
     config_by_name = {     
          "development": DevelopmentConfig,     
          "production": ProductionConfig,     
          "testing": TestingConfig, }   