from flask import Flask
from flask_cors import CORS
import os

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
    
    # Enable CORS
    CORS(app)
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register routes
    from app.routes import main
    app.register_blueprint(main)
    
    return app