from tests.conftest import client 


def test_user_registration():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 201
    assert "user_id" in response.json()


def test_duplicate_email():
    client.post(
        "/api/auth/register",
        json={
            "username": "user1",
            "email": "dup@example.com",
            "password": "SecurePass123!"
        }
    )

    response = client.post(
        "/api/auth/register",
        json={
            "username": "user2",
            "email": "dup@example.com",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 409


def test_user_login_success():
    client.post(
        "/api/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "SecurePass123!"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "login@example.com",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_invalid_login():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401
