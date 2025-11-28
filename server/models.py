# server/models.py

from app import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# --- Model Definitions ---

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    # Relationship: has many Guests through Appearances (many-to-many)
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
    guests = association_proxy('appearances', 'guest')

    # Serialization rules: Prevent infinite recursion
    serialize_rules = ('-appearances.episode', '-guests.appearances')

    def __repr__(self):
        return f'<Episode {self.id}: {self.number} ({self.date})>'

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    # Relationship: has many Episodes through Appearances (many-to-many)
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')
    episodes = association_proxy('appearances', 'episode')

    # Serialization rules: Prevent infinite recursion
    serialize_rules = ('-appearances.guest', '-episodes.appearances')

    def __repr__(self):
        return f'<Guest {self.id}: {self.name}>'

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    # Foreign Keys
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))

    # Relationships: belongs to Episode AND Guest
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')

    # Serialization rules: Nest related objects
    # Include nested episode and guest for POST response. Exclude appearance to avoid recursion.
    serialize_rules = ('-episode.appearances', '-guest.appearances')

    # Validation: Rating must be between 1 and 5
    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5 (inclusive).")
        return rating

    def __repr__(self):
        return f'<Appearance {self.id} (Rating: {self.rating})>'