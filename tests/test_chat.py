from app.chat import llm
from tests.conftest import client

def fake_llm(message: str) -> str:
    return "mocked ai response"


def test_send_chat_authenticated(monkeypatch):
    
    monkeypatch.setattr(
    "app.chat.routes.call_llm",
    fake_llm
)


    # Register & login
    client.post(
        "/api/auth/register",
        json={
            "username": "chatuser",
            "email": "chat@example.com",
            "password": "SecurePass123!"
        }
    )

    login = client.post(
        "/api/auth/login",
        json={
            "email": "chat@example.com",
            "password": "SecurePass123!"
        }
    )

    token = login.json()["access_token"]

    response = client.post(
        "/api/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={"message": "Hello"}
    )

    assert response.status_code == 200
    assert response.json()["ai_response"] == "mocked ai response"


def test_unauthorized_access():
    response = client.post(
        "/api/chat",
        json={"message": "Hello"}
    )

    assert response.status_code == 401


def test_get_chat_history(monkeypatch):
    monkeypatch.setattr(llm, "call_llm", fake_llm)

    login = client.post(
        "/api/auth/login",
        json={
            "email": "chat@example.com",
            "password": "SecurePass123!"
        }
    )

    token = login.json()["access_token"]

    response = client.get(
        "/api/chat/history",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "chats" in response.json()


def test_delete_chat(monkeypatch):
    monkeypatch.setattr(llm, "call_llm", fake_llm)

    login = client.post(
        "/api/auth/login",
        json={
            "email": "chat@example.com",
            "password": "SecurePass123!"
        }
    )

    token = login.json()["access_token"]

    chat = client.post(
        "/api/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={"message": "To delete"}
    )

    chat_id = chat.json()["chat_id"]

    delete = client.delete(
        f"/api/chat/{chat_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert delete.status_code == 200
