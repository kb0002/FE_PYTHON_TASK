from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    CORS(app)  # Enable Cross-Origin Resource Sharing

    # Register blueprints or routes if modularizing
    from app import routes
   
