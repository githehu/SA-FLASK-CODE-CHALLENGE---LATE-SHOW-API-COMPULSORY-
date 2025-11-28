# server/testing/conftest.py

import pytest
from app import app, db
from models import Episode, Guest, Appearance

@pytest.fixture(scope='session')
def _app():
    # Set up the test configuration
    app.config['TESTING'] = True
    # Use a separate in-memory SQLite database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        # Initialize database and create tables
        db.create_all()
        yield app
        # Teardown: close and drop tables
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(_app):
    return _app.test_client()

@pytest.fixture
def session(db_session):
    return db_session

@pytest.fixture(autouse=True)
def setup_data(_app):
    # This fixture runs before every test to ensure a clean dataset
    with _app.app_context():
        # 1. Clear database
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()
        db.session.commit()

        # 2. Create sample data for testing
        e1 = Episode(date="1/1/2000", number=101)
        e2 = Episode(date="1/2/2000", number=102)
        
        g1 = Guest(name="Test Guest 1", occupation="Actor")
        g2 = Guest(name="Test Guest 2", occupation="Musician")

        db.session.add_all([e1, e2, g1, g2])
        db.session.commit()
        
        # Appearance data
        a1 = Appearance(episode=e1, guest=g1, rating=5)
        a2 = Appearance(episode=e1, guest=g2, rating=1)
        a3 = Appearance(episode=e2, guest=g1, rating=3)

        db.session.add_all([a1, a2, a3])
        db.session.commit()

        # Provide access to the created objects for tests
        yield {
            'e1': e1, 'e2': e2,
            'g1': g1, 'g2': g2,
            'a1': a1, 'a2': a2, 'a3': a3
        }

@pytest.fixture
def db_session(_app):
    # Provides a database session object
    with _app.app_context():
        yield db.session