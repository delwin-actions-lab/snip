from fastapi.testclient import TestClient

from snip_api.main import app

client = TestClient(app)


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_and_follow():
    r = client.post("/links", json={"url": "https://example.com/a/very/long/path"})
    assert r.status_code == 201
    code = r.json()["code"]
    assert len(code) == 7

    r = client.get(f"/{code}", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "https://example.com/a/very/long/path"


def test_clicks_are_counted():
    code = client.post("/links", json={"url": "https://example.com/"}).json()["code"]
    for _ in range(3):
        client.get(f"/{code}", follow_redirects=False)
    assert client.get(f"/links/{code}").json()["clicks"] == 3


def test_rejects_invalid_url():
    r = client.post("/links", json={"url": "not-a-url"})
    assert r.status_code == 422


def test_unknown_code_is_404():
    assert client.get("/doesnotexist", follow_redirects=False).status_code == 404


def test_stats_for_unknown_code_is_404():
    r = client.get("/links/doesnotexist")
    assert r.status_code == 404
    assert r.json() == {"detail": "unknown code"}
