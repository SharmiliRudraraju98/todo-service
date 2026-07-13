import pytest
from app import app, _todos


@pytest.fixture
def client():
    app.config["TESTING"] = True
    _todos.clear()
    with app.test_client() as client:
        yield client


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_create_and_list_todo(client):
    resp = client.post("/todos", json={"title": "Learn Docker"})
    assert resp.status_code == 201
    created = resp.get_json()
    assert created["title"] == "Learn Docker"
    assert created["done"] is False

    resp = client.get("/todos")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_create_todo_without_title_fails(client):
    resp = client.post("/todos", json={})
    assert resp.status_code == 400