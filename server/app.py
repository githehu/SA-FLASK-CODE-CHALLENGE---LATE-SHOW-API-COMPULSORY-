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
class EpisodeList(Resource):
    # 1. GET /episodes
    def get(self):
        episodes = Episode.query.all()
        # Use to_dict from SerializerMixin
        episode_data = [episode.to_dict(rules=('-appearances',)) for episode in episodes]
        return make_response(jsonify(episode_data), 200)

class EpisodeByID(Resource):
    # 2. GET /episodes/<int:id>
    def get(self, id):
        episode = Episode.query.get(id)

        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)

        # Include nested appearances with guest details
        episode_data = episode.to_dict()
        return make_response(jsonify(episode_data), 200)

    # 3. DELETE /episodes/<int:id>
    def delete(self, id):
        episode = Episode.query.get(id)

        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)

        # Cascade delete is configured on the Appearance relationship in models.py
        db.session.delete(episode)
        db.session.commit()
        
        # Status 204 (No Content), empty response
        return make_response('', 204) 

class GuestList(Resource):
    # 4. GET /guests
    def get(self):
        guests = Guest.query.all()
        # Use to_dict from SerializerMixin
        guest_data = [guest.to_dict(rules=('-appearances',)) for guest in guests]
        return make_response(jsonify(guest_data), 200)

class AppearanceList(Resource):
    # 5. POST /appearances
    def post(self):
        data = app.json.get_json()

        try:
            # Create a new Appearance instance with incoming data
            new_appearance = Appearance(
                rating=data.get('rating'),
                episode_id=data.get('episode_id'),
                guest_id=data.get('guest_id')
            )
            
            # The @validates decorator in models.py will check the rating
            db.session.add(new_appearance)
            db.session.commit()

            # Status 201 (Created), return the new appearance with nested details
            return make_response(new_appearance.to_dict(), 201)

        except ValueError as e:
            # Handle validation errors (e.g., rating out of range)
            db.session.rollback()
            return make_response(jsonify({"errors": [str(e)]}), 400)
        
        except Exception as e:
            # Handle other potential database errors (e.g., non-existent FK)
            db.session.rollback()
            # Catching integrity errors (like foreign key violation) is complex without a specific handler, 
            # so we'll use a generic 400 for now and focus on the required rating error.
            return make_response(jsonify({"errors": ["An error occurred: Check episode_id and guest_id validity."]}), 400)

# --- Routing ---
api.add_resource(EpisodeList, '/episodes')
api.add_resource(EpisodeByID, '/episodes/<int:id>')
api.add_resource(GuestList, '/guests')
api.add_resource(AppearanceList, '/appearances')

# --- Error Handling ---
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

# Define the run configuration
if __name__ == '__main__':
    # Set a default host to make it accessible in common environments
    # Run the app on port 5555 as required
    app.run(port=5555, debug=True)