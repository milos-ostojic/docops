def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_and_list(client):
    r = client.post("/documents", json={"title": "Faktura 1", "content": "..."})
    assert r.status_code == 201
    assert "id" in r.json()
    assert len(client.get("/documents").json()) == 1


def test_validation_error(client):
    r = client.post("/documents", json={"title": "bez contyenta"})
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"] == ["body", "content"]


def test_get_document(client):
    created = client.post("/documents", json={"title": "Ugovor", "content": "..."})
    doc_id = created.json()["id"]

    r = client.get(f"/documents/{doc_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Ugovor"


def test_get_document_not_found(client):
    docs_id = "9999"

    r = client.get(f"/documents/{docs_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Document not found"


def test_delete_document(client):
    create = client.post("/documents", json={"title": "Faktura 1", "content": "..."})
    doc_id = create.json()["id"]

    r = client.delete(f"/documents/{doc_id}")
    assert r.status_code == 204

    r = client.get(f"/documents/{doc_id}")
    assert r.status_code == 404


def test_delete_document_not_found(client):
    r = client.delete("/documents/9999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Document not found"
