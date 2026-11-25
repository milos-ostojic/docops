from fastapi.testclient import TestClient

from docops.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code ==200
    assert r.json() == {"status": "ok"}


def test_create_and_list():
    r = client.post("/documents", json={"title": "Faktura 1", "content": "..."})
    assert r.status_code == 201
    assert "id" in r.json()
    assert len(client.get("/documents").json()) >= 1

def test_validation_error():
    r = client.post('/documents', json={"title": "bez contyenta"})
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"] == ["body", "content"]