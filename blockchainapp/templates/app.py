

# Import necessary libraries
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base # Assuming this is where DeclarativeBase comes from
from werkzeug.middleware.proxy_fix import ProxyFix # Correct import for ProxyFix
from flask_cors import CORS # For CORS
# Set up logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file (for local development)
# This line should be at the very top of your application file,
# before you try to access any environment variables.
from dotenv import load_dotenv
load_dotenv()

# Define Base for SQLAlchemy declarative models
# Assuming DeclarativeBase is from sqlalchemy.ext.declarative
# If it's a custom Base, ensure it's defined or imported correctly.
Base = declarative_base() # Or if you had a custom Base class, keep that.

# Create database instance
db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)

# Configure app.secret_key securely
app.secret_key = os.getenv("SESSION_SECRET") # Now directly using the env variable
if not app.secret_key:
    raise ValueError("SESSION_SECRET environment variable is not set. Please set a strong, random secret key.")

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set. Please set your PostgreSQL connection string.")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url # Using the env variable here
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database with app
db.init_app(app)

# Enable CORS (review this for production as discussed previously)
# For production, consider restricting origins:
# CORS(app, origins=["https://yourfrontend.com"])
CORS(app) 

# Configure the app
app.config['JSON_SORT_KEYS'] = False

# Register blueprints
# Make sure your routes.py defines main_bp
from routes import main_bp
app.register_blueprint(main_bp)

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # WARNING: debug=True and host='0.0.0.0' are NOT for production.
    # Use a production WSGI server like Gunicorn or uWSGI for deployment.
    app.run(host='0.0.0.0', port=5000, debug=True)