import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine
from app.models import Base, Game

GAMES = [
    {
        "title": "Minecraft",
        "genre": "Sandbox",
        "platform": "PC",
        "cover_url": None,
    },
    {
        "title": "Valorant",
        "genre": "FPS",
        "platform": "PC",
        "cover_url": None,
    },
    {
        "title": "Elden Ring",
        "genre": "RPG",
        "platform": "PC",
        "cover_url": None,
    },
    {
        "title": "Rocket League",
        "genre": "Sports",
        "platform": "Multi-platform",
        "cover_url": None,
    },
    {
        "title": "Stardew Valley",
        "genre": "Simulation",
        "platform": "Multi-platform",
        "cover_url": None,
    },
]

def run():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    imported = 0

    for data in GAMES:
        existing = db.query(Game).filter(Game.title == data["title"]).first()

        if existing:
            continue

        game = Game(
            title=data["title"],
            genre=data["genre"],
            platform=data["platform"],
            cover_url=data["cover_url"],
        )

        db.add(game)
        imported += 1

    db.commit()
    db.close()

    print(f"Imported {imported} games.")

if __name__ == "__main__":
    run()