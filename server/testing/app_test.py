# server/testing/app_test.py

import pytest

# --- GET /episodes ---
def test_get_episodes_success(client, setup_data):
    response = client.get('/episodes')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    # Check structure (no appearances should be nested here)
    assert 'appearances' not in data[0]
    assert data[0]['number'] == setup_data['e1'].number

# --- GET /episodes/<int:id> ---
def test_get_episode_by_id_success(client, setup_data):
    e1_id = setup_data['e1'].id
    response = client.get(f'/episodes/{e1_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == e1_id
    # Check nested appearances
    assert 'appearances' in data
    assert len(data['appearances']) == 2
    # Check nested guest details
    assert 'guest' in data['appearances'][0]
    assert 'name' in data['appearances'][0]['guest']

def test_get_episode_by_id_not_found(client):
    response = client.get('/episodes/999') # Use a non-existent ID
    assert response.status_code == 404
    assert response.get_json() == {"error": "Episode not found"}

# --- DELETE /episodes/<int:id> ---
def test_delete_episode_success(client, setup_data):
    e2_id = setup_data['e2'].id
    response = client.delete(f'/episodes/{e2_id}')
    assert response.status_code == 204
    assert response.data == b'' # No content expected
    
    # Verify episode is actually deleted
    verify_response = client.get(f'/episodes/{e2_id}')
    assert verify_response.status_code == 404

def test_delete_episode_not_found(client):
    response = client.delete('/episodes/999')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Episode not found"}

# --- GET /guests ---
def test_get_guests_success(client, setup_data):
    response = client.get('/guests')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['name'] == setup_data['g1'].name
    assert 'appearances' not in data[0]

# --- POST /appearances ---
def test_post_appearance_success(client, setup_data):
    post_data = {
        "rating": 5, 
        "episode_id": setup_data['e2'].id, # Episode 2
        "guest_id": setup_data['g2'].id    # Guest 2
    }
    response = client.post('/appearances', json=post_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['rating'] == 5
    assert data['episode_id'] == post_data['episode_id']
    assert data['guest_id'] == post_data['guest_id']
    # Check nested episode/guest details are included for a successful POST
    assert 'episode' in data
    assert 'guest' in data
    assert data['guest']['name'] == setup_data['g2'].name

def test_post_appearance_validation_fail_low(client, setup_data):
    post_data = {
        "rating": 0, # Invalid rating
        "episode_id": setup_data['e2'].id, 
        "guest_id": setup_data['g2'].id
    }
    response = client.post('/appearances', json=post_data)
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    assert "Rating must be between 1 and 5" in data['errors'][0]

def test_post_appearance_validation_fail_high(client, setup_data):
    post_data = {
        "rating": 6, # Invalid rating
        "episode_id": setup_data['e2'].id, 
        "guest_id": setup_data['g2'].id
    }
    response = client.post('/appearances', json=post_data)
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    assert "Rating must be between 1 and 5" in data['errors'][0]