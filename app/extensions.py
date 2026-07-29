from flask_sqlalchemy import SQLAlchemy     # Import SQLAlchemy for database management.
from flask_migrate import Migrate           # Import Flask-Migrate for handling database migrations.
from flask_jwt_extended import JWTManager   # Import JWTManager for creating and managing JSON Web Tokens.
from flask_cors import CORS                 # Import CORS to allow communication between frontend and backend.
from flask_bcrypt import Bcrypt             # Import Bcrypt for password hashing and security.
 
db = SQLAlchemy()
# Create database instance.
# Used to interact with the database using SQLAlchemy.

migrate = Migrate()
# Create migration instance.
# Helps update database structure without losing data.

jwt = JWTManager()
# Create JWT manager.
# Handles user authentication tokens.

cors = CORS()
# Create CORS instance.
# Allows requests from different domains (frontend to backend).

bcrypt = Bcrypt()
# Create password encryption tool.
# Used to securely hash user passwords.