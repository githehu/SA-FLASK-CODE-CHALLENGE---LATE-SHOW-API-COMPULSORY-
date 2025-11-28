# server/testing/models_test.py

import pytest
from app import db # Need db for session and commit
from models import Episode, Guest, Appearance


# --- Relationship Tests ---
def test_episode_relationships(setup_data):
    e1 = setup_data['e1']
    g1 = setup_data['g1']
    a1 = setup_data['a1']
    
    # Test episode.appearances
    assert len(e1.appearances) == 2
    assert a1 in e1.appearances
    
    # Test episode.guests (association proxy)
    assert g1 in e1.guests

def test_guest_relationships(setup_data):
    g1 = setup_data['g1']
    e1 = setup_data['e1']
    a1 = setup_data['a1']

    # Test guest.appearances
    assert len(g1.appearances) == 2
    assert a1 in g1.appearances

    # Test guest.episodes (association proxy)
    assert e1 in g1.episodes

def test_appearance_relationships(setup_data):
    a1 = setup_data['a1']
    e1 = setup_data['e1']
    g1 = setup_data['g1']
    
    # Test appearance.episode
    assert a1.episode is e1
    
    # Test appearance.guest
    assert a1.guest is g1

# --- Validation Test ---
def test_appearance_rating_validation(db_session):
    # Test valid rating
    valid_appearance = Appearance(rating=3, episode_id=1, guest_id=1)
    db_session.add(valid_appearance)
    db_session.commit() # Should succeed

    # Test rating too low (below 1)
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        invalid_low = Appearance(rating=0, episode_id=1, guest_id=1)
        db_session.add(invalid_low)
        db_session.commit()
    db_session.rollback()

    # Test rating too high (above 5)
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        invalid_high = Appearance(rating=6, episode_id=1, guest_id=1)
        db_session.add(invalid_high)
        db_session.commit()
    db_session.rollback()

# --- Cascade Delete Test ---
def test_episode_cascade_delete(db_session, setup_data):
    e1_id = setup_data['e1'].id
    a1_id = setup_data['a1'].id
    
    # Before delete, check the objects exist
    assert Episode.query.get(e1_id) is not None
    assert Appearance.query.get(a1_id) is not None

    # Delete the episode
    episode_to_delete = Episode.query.get(e1_id)
    db_session.delete(episode_to_delete)
    db_session.commit()

    # Check if episode is deleted
    assert Episode.query.get(e1_id) is None
    
    # Check if the associated appearance is *cascaded* deleted
    assert Appearance.query.get(a1_id) is None