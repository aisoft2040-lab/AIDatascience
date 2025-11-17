from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body.get("status") == "ok"
    assert "version" in body


def test_echo():
    r = client.post("/echo", json={"message": "hello"})
    assert r.status_code == 200
    assert r.json() == {"message": "hello"}
