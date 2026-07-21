import os
from flask import Flask
from config import config_by_name
from app.extensions import db, migrate, jwt, cors, bcrypt

def create_app(env_name=None):
    env_name = env_name or os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[env_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    from app import models  # noqa

    from app.controllers import all_blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app