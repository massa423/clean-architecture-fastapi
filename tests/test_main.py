from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_users():
    response = client.get("/api/v1/users")
    assert response.status_code == 200


def test_read_users_1():
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200


def test_read_users_2():
    response = client.get("/api/v1/users/2")
    assert response.status_code == 200


def test_read_users_100():
    response = client.get("/api/v1/users/100")
    assert response.status_code == 404


def test_post_users_testdata1():
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "testdata1",
            "password": "password",
            "email": "testdata1@example.com",
        },
    )
    assert response.status_code == 201


def test_post_users_testdata1_duplicate_name():
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "testdata1",
            "password": "password",
            "email": "testdata1_again@example.com",
        },
    )
    assert response.status_code == 409


def test_post_users_testdata1_duplicate_email():
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "testdata1_again",
            "password": "password",
            "email": "testdata1@example.com",
        },
    )
    assert response.status_code == 409
