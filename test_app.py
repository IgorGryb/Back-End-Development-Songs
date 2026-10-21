"""PyTest suite for the Songs microservice (IBM Back-End Development Capstone)."""
import pytest
from app import app, songs


@pytest.fixture(autouse=True)
def clean_db():
    songs.delete_many({})
    yield
    songs.delete_many({})


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _make(client, title="Imagine", artist="John Lennon"):
    resp = client.post("/song", json={"title": title, "artist": artist})
    assert resp.status_code == 201
    return resp.get_json()["id"]


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "OK"


def test_get_song_empty(client):
    assert client.get("/song").get_json() == []


def test_post_then_get_song(client):
    sid = _make(client)
    songs_list = client.get("/song").get_json()
    assert len(songs_list) == 1
    assert songs_list[0]["id"] == sid
    assert songs_list[0]["title"] == "Imagine"


# ---------- Exercise 5: PUT song ----------
def test_put_song_updates_title(client):
    sid = _make(client)
    resp = client.put(f"/song/{sid}", json={"title": "Imagine (Remastered)"})
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Imagine (Remastered)"
    got = client.get(f"/song/{sid}").get_json()
    assert got["title"] == "Imagine (Remastered)"


def test_put_song_updates_artist(client):
    sid = _make(client, artist="Unknown")
    resp = client.put(f"/song/{sid}", json={"artist": "John Lennon"})
    assert resp.status_code == 200
    assert resp.get_json()["artist"] == "John Lennon"


def test_put_song_not_found(client):
    assert client.put("/song/000000000000000000000000", json={"title": "x"}).status_code == 404


# ---------- Exercise 6: DELETE song ----------
def test_delete_song_removes_it(client):
    sid = _make(client)
    resp = client.delete(f"/song/{sid}")
    assert resp.status_code == 200
    assert resp.get_json()["deleted"] == sid
    assert client.get("/song").get_json() == []


def test_delete_song_not_found(client):
    assert client.delete("/song/000000000000000000000000").status_code == 404
