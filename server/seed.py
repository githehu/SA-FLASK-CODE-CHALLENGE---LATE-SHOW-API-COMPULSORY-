# server/seed.py

from app import app, db
from models import Episode, Guest, Appearance

def seed_data():
    with app.app_context():
        # Clear existing data
        print("Clearing database tables...")
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()
        db.session.commit()

        print("Creating Guests...")
        guest1 = Guest(name="Michael J. Fox", occupation="actor")
        guest2 = Guest(name="Sandra Bernhard", occupation="Comedian")
        guest3 = Guest(name="Tracey Ullman", occupation="television actress")
        guest4 = Guest(name="Chris Rock", occupation="Comedian")

        db.session.add_all([guest1, guest2, guest3, guest4])
        db.session.commit()

        print("Creating Episodes...")
        episode1 = Episode(date="1/11/99", number=1)
        episode2 = Episode(date="1/12/99", number=2)
        episode3 = Episode(date="1/13/99", number=3)
        episode4 = Episode(date="1/14/99", number=4)

        db.session.add_all([episode1, episode2, episode3, episode4])
        db.session.commit()

        print("Creating Appearances...")
        # Episode 1 Guests
        app1 = Appearance(episode=episode1, guest=guest1, rating=4) # Expected /episodes/1 appearance
        app2 = Appearance(episode=episode1, guest=guest2, rating=5)

        # Episode 2 Guests
        app3 = Appearance(episode=episode2, guest=guest3, rating=5) # Example POST success guest/episode

        # Episode 3 Guests
        app4 = Appearance(episode=episode3, guest=guest1, rating=3)
        app5 = Appearance(episode=episode3, guest=guest4, rating=5)

        db.session.add_all([app1, app2, app3, app4, app5])
        db.session.commit()

        print("Seeding complete.")

if __name__ == '__main__':
    seed_data()