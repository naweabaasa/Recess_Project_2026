import os from flask 
import Flask, jsonify from config 
import config_by_name from app.extensions 
import db, migrate, jwt, cors, bcrypt     



def create_app(env_name: str = None) -> Flask:     
    """Application factory. Keeps startup grouped and testable,     
    call create_app('testing') to get an isolated app for pytest."""     
    env_name = env_name or os.environ.get("FLASK_ENV", "development")       
    
    app = Flask(__name__)     
    app.config.from_object(config_by_name[env_name])       
    
    
    # ---- extensions ----     
db.init_app(app)     
migrate.init_app(app, db)     
jwt.init_app(app)     
bcrypt.init_app(app)     
cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})       



# ---- models must be imported before blueprints/migrations touch db ----     
from app import models  # noqa: F401       


# ---- blueprints, grouped under /api/* ----     
from app.controllers import all_blueprints     
for bp in all_blueprints:         
    app.register_blueprint(bp)       
    
    
# ---- error handlers ----     
@app.errorhandler(404)     
def not_found(e):         
    return jsonify({"error": "Resource not found"}), 404       

@app.errorhandler(500)     
def server_error(e):         
    return jsonify({"error": "Internal server error"}), 500       

@jwt.unauthorized_loader     
def missing_token(reason): 
     return jsonify({"error": "Missing or invalid authorization token"}), 401


@jwt.expired_token_loader     
def expired_token(header, payload):         
    return jsonify({"error": "Token has expired"}), 401       


@app.route("/")     
def index():         
    return jsonify({"message": "API is running"}), 200       


return app 