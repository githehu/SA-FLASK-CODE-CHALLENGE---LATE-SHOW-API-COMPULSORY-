# server/app.py

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os

# Create Flask app
app = Flask(__name__)
# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-RESTful API
api = Api(app)

# Import models *after* db is initialized to avoid circular imports
from models import Episode, Guest, Appearance

# --- Basic Index Route ---
@app.route('/')
def index():
    return '<h1>Late Show API</h1>'

# --- Resources (API Endpoints) will be defined here in Phase 4 ---

# --- Error Handling ---
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

# Define the run configuration
if __name__ == '__main__':
    # Set a default host to make it accessible in common environments
    # Run the app on port 5555 as required
    app.run(port=5555, debug=True)