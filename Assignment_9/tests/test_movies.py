def test_create_and_get_movie(client):
    payload = {"title": "Inception", "director": "Christopher Nolan", "year": 2010}
    r = client.post("/movies", json=payload)
    assert r.status_code == 201
    created = r.json()
    assert created["id"] > 0
    assert created["title"] == payload["title"]

    r2 = client.get(f"/movies/{created['id']}")
    assert r2.status_code == 200
    got = r2.json()
    assert got["title"] == "Inception"
    assert got["director"] == "Christopher Nolan"
    assert got["year"] == 2010

def test_list_movies_pagination(client):
    for i in range(1, 6):
        client.post("/movies", json={"title": f"T{i}", "director": "D", "year": 2000 + i})

    r = client.get("/movies?skip=0&limit=3")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 3

def test_update_movie(client):
    r = client.post("/movies", json={"title": "Old", "director": "Dir", "year": 1999})
    mid = r.json()["id"]

    r2 = client.put(f"/movies/{mid}", json={"title": "New"})
    assert r2.status_code == 200
    assert r2.json()["title"] == "New"

def test_delete_movie(client):
    r = client.post("/movies", json={"title": "Temp", "director": "X"})
    mid = r.json()["id"]
    r2 = client.delete(f"/movies/{mid}")
    assert r2.status_code == 204

    r3 = client.get(f"/movies/{mid}")
    assert r3.status_code == 404
