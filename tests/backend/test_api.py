import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app import create_app


def test_health():
    client = create_app().test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_analyze_empty():
    client = create_app().test_client()
    response = client.post("/api/analyze", json={"password": ""})
    assert response.status_code == 400


def test_analyze_rejects_query_password():
    client = create_app().test_client()
    response = client.get("/api/analyze?password=secret")
    assert response.status_code in {400, 405}


def test_analyze_success_no_echo():
    client = create_app().test_client()
    secret = "N0tARealPassword!xyz"
    response = client.post("/api/analyze", json={"password": secret})
    assert response.status_code == 200
    data = response.get_json()
    assert "score" in data
    assert secret not in json.dumps(data)
    assert "password" not in data


def test_compare():
    client = create_app().test_client()
    response = client.post(
        "/api/compare",
        json={"password_a": "password", "password_b": "long-unique-passphrase-example"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["b"]["score"] > data["a"]["score"]
