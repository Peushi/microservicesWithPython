import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test_games.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_create_game():
    response = client.post("/v1/games/", json={
        "title": "The Witcher 3",
        "genre": "RPG",
        "platform": "PC",
        "cover_url": "https://example.com/witcher3.jpg"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "The Witcher 3"
    assert data["genre"] == "RPG"
    assert "id" in data

def test_list_games():
    response = client.get("/v1/games/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

def test_get_game_not_found():
    response = client.get("/v1/games/nonexistent-id")
    assert response.status_code == 404

def test_search_games():
    client.post("/v1/games/", json={
        "title": "Dark Souls",
        "genre": "Action",
        "platform": "PC"
    })
    response = client.get("/v1/games/search?q=dark")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert results[0]["title"] == "Dark Souls"