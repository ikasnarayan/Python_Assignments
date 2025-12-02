import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models import Movie

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(Movie).delete()
        db.commit()
        for i in range(1, 31):  # 30 movies for tests
            db.add(Movie(id=i, title=f"TestMovie {i}", year=2000 + (i % 20), genre="Action" if i % 2 == 0 else "Drama"))
        db.commit()
    finally:
        db.close()

def test_first_page_ok():
    r = client.get("/movies/?page=1")
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total_records"] == 30
    assert data["total_pages"] == 3
    assert len(data["movies"]) == 10
    assert data["navigation"]["next_page"] == 2
    assert data["navigation"]["previous_page"] is None

def test_last_page_ok():
    r = client.get("/movies/?page=3")
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 3
    assert len(data["movies"]) == 10
    assert data["navigation"]["next_page"] is None
    assert data["navigation"]["previous_page"] == 2

def test_page_not_found():
    r = client.get("/movies/?page=4")
    assert r.status_code == 404
    assert r.json()["detail"] == "Page not found"

def test_filters_work():
    r = client.get("/movies/?page=1&genre=Action")
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total_records"] > 0
    for m in data["movies"]:
        assert m["genre"] == "Action"
