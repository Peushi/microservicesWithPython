import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from app.database import SessionLocal, engine
from app.models import Base, User

USERS = [
    {"username": "nova",        "email": "nova@gamehub.io"},
    {"username": "alex_g",      "email": "alex@gamehub.io"},
    {"username": "maya_r",      "email": "maya@gamehub.io"},
    {"username": "thunderbyte", "email": "thunder@gamehub.io"},
    {"username": "pixel_queen", "email": "pixel@gamehub.io"},
]

FAKE_HASH = "hashed_password"

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    imported = 0
    for data in USERS:
        existing = db.query(User).filter(User.username == data["username"]).first()
        if existing:
            continue
        user = User(
            username=data["username"],
            email=data["email"],
            hashed_password=FAKE_HASH,
        )
        db.add(user)
        imported += 1
    db.commit()
    db.close()
    print(f"Imported {imported} users.")

if __name__ == "__main__":
    run()