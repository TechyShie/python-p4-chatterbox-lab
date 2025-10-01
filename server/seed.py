from app import app
from models import db, Message

with app.app_context():
    db.drop_all()
    db.create_all()

    messages = [
        Message(body="Hello 👋", username="Ian"),
        Message(body="How's it going?", username="Alex"),
        Message(body="Good morning!", username="Sam")
    ]

    db.session.add_all(messages)
    db.session.commit()
    print("Seeded database successfully!")
