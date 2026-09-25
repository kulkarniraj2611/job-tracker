import pytest

from app import create_app, db
from app.models import Application, Status


@pytest.fixture
def client():
    app = create_app("config.TestConfig")
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_index_empty(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"No applications yet" in resp.data


def test_create_application_via_api(client):
    resp = client.post("/api/applications", json={
        "company_name": "Acme Corp",
        "role": "Backend Engineer",
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["company_name"] == "Acme Corp"
    assert data["status"] == "APPLIED"


def test_create_requires_company_name(client):
    resp = client.post("/api/applications", json={"role": "Engineer"})
    assert resp.status_code == 400


def test_get_all_applications(client):
    client.post("/api/applications", json={"company_name": "Acme"})
    client.post("/api/applications", json={"company_name": "Globex"})
    resp = client.get("/api/applications")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


def test_valid_status_transition(client):
    create_resp = client.post("/api/applications", json={"company_name": "Acme"})
    app_id = create_resp.get_json()["id"]

    resp = client.put(f"/api/applications/{app_id}", json={"status": "INTERVIEW"})
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "INTERVIEW"


def test_invalid_status_transition_rejected(client):
    create_resp = client.post("/api/applications", json={"company_name": "Acme"})
    app_id = create_resp.get_json()["id"]

    # APPLIED -> OFFER is not an allowed direct transition
    resp = client.put(f"/api/applications/{app_id}", json={"status": "OFFER"})
    assert resp.status_code == 400


def test_delete_application(client):
    create_resp = client.post("/api/applications", json={"company_name": "Acme"})
    app_id = create_resp.get_json()["id"]

    del_resp = client.delete(f"/api/applications/{app_id}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/applications/{app_id}")
    assert get_resp.status_code == 404


def test_reminders_endpoint(client):
    from datetime import date, timedelta

    client.post("/api/applications", json={
        "company_name": "Acme",
        "reminder_date": str(date.today() + timedelta(days=1)),
    })
    client.post("/api/applications", json={
        "company_name": "FarFuture Inc",
        "reminder_date": str(date.today() + timedelta(days=30)),
    })

    resp = client.get("/api/applications/reminders")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["company_name"] == "Acme"
