import os  # Provides access to environment variables and operating system functions.

from flask import Flask   # Imports the Flask class to create the application.

from config import config_by_name   # Imports different configuration settings (development, production).

from app.extensions import db, migrate, jwt, cors, bcrypt    # Imports initialized Flask extensions (database, migrations, JWT, CORS, password hashing).

from app import models  # Imports database models so Flask-Migrate can detect them.

import logging

def create_app(env_name=None):   # Application factory function that creates and configures the Flask app.

    # Uses the provided environment or gets FLASK_ENV from the system.
    # Defaults to "development" if none is set.
    env_name = env_name or os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)                                 # Creates a new Flask application instance.
    app.config.from_object(config_by_name[env_name])      # Loads configuration settings based on the selected environment.

    # Configure logging for production
    if env_name == "production":
        logging.basicConfig(level=logging.INFO)
        app.logger.setLevel(logging.INFO)
        app.logger.info("BreadWise Backend starting in production mode")


    db.init_app(app)                  # Initializes SQLAlchemy with the Flask app.
    migrate.init_app(app, db)         # Enables database migration support.
    jwt.init_app(app)                 # Initializes JWT authentication.
    bcrypt.init_app(app)              # Initializes password hashing with Bcrypt.
    cors.init_app(app)                # Enables Cross-Origin Resource Sharing (CORS).

    # Configure SQLAlchemy engine options for shared MySQL hosting
    # (keeps pooled connections alive and validates them before use)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
        'pool_timeout': 30,
        'pool_size': 5,
        'max_overflow': 10,
    }



    # Health check endpoint for Render
    @app.route("/api/health")
    def health():
        return {"status": "ok"}, 200

    # Blue print registration
    from app.controllers import all_blueprints    # Imports all application blueprints.
    for bp in all_blueprints:
        app.register_blueprint(bp)                 # Registers each blueprint with the Flask app.

    return app           # Returns the fully configured Flask application.