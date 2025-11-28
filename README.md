# SA Flask Code Challenge — Late Show API (Compulsory)

A small Flask API for managing Late Show episodes, guests, and their appearances. This project was built as a coding challenge and uses Flask, SQLAlchemy, Flask-Migrate and Flask-RESTful.

## ✅ Highlights

- Python Flask API with models: Episode, Guest, and an association model Appearance
- Persistence with SQLite (configurable) and migrations via Flask-Migrate
- RESTful endpoints for reading episodes & guests, creating appearances, and deleting episodes
- Test suite using pytest (in-memory SQLite for fast, isolated tests)

## Getting started

Recommended: use a Python 3.12+ virtual environment.

1. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Initialize (or recreate) the database and run migrations

```bash
# Create the SQLite DB used by default
export FLASK_APP=server/app.py
flask db init   # only the first time
flask db migrate -m "initial"
flask db upgrade
```

4. (Optional) Seed the database with example data

```bash
python server/seed.py
```

5. Run the API

```bash
python server/app.py
# The app will run on port 5555 by default: http://localhost:5555
```

## API Endpoints

All responses are JSON unless otherwise noted.

- GET /episodes
	- Returns a list of episodes (appearances omitted in this index route)

- GET /episodes/<id>
	- Returns a single episode by id and includes nested appearances and guest details
	- 404 returned: {"error": "Episode not found"} when episode does not exist

- DELETE /episodes/<id>
	- Deletes an episode (cascade removes appearances). Returns 204 No Content on success.

- GET /guests
	- Returns a list of guests (appearances omitted)

- POST /appearances
	- Creates a new appearance. Expected JSON payload:

```json
{
	"rating": 1-5,
	"episode_id": <episode id>,
	"guest_id": <guest id>
}
```

	- On success: returns 201 with the new appearance including nested episode and guest
	- Validation: rating must be integer 1–5. Invalid rating returns status 400 with errors.

## Tests

Run tests with pytest (project contains tests under `server/testing`):

```bash
pytest
```

Notes:
- The test suite uses an in-memory SQLite database to avoid interfering with local development DB files.
- If you run tests and want logging, run with `pytest -q` or `pytest -q -s`.

## Files of interest

- `server/app.py` — main Flask app and API routes
- `server/models.py` — SQLAlchemy model definitions
- `server/seed.py` — helper to populate the DB with sample data
- `server/testing/` — pytest test suite

## .gitignore
This repository already includes a `.gitignore` tailored for Python/Flask projects.

---

If you'd like, I can adapt this README for a specific deployment target (Heroku / Railway / Docker) or add API examples with curl / httpie requests. 
# SA-FLASK-CODE-CHALLENGE---LATE-SHOW-API-COMPULSORY-