from unittest.mock import MagicMock

from src.database.models import User
from src.services.auth import auth_service


def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post(
        "/auth/auth/signup",
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


def test_repeat_create_user(client, user):
    response = client.post(
        "/auth/auth/signup",
        json=user,
    )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed(client, user):
    response = client.post(
        "/auth/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


def test_login_wrong_password(client, session, user):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.email_confirmed = True
    response = client.post(
        "/auth/auth/login",
        data={"username": user.get('email'), "password": 'password'},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


def test_login_wrong_email(client, user):
    response = client.post(
        "/auth/auth/login",
        data={"username": 'email', "password": user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"


def test_login_user(client, session, user):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.email_confirmed = True
    session.commit()
    response = client.post(
        "/auth/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_refresh_token(client, user):
    response = client.post(
        "/auth/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    response = client.get(
        "/auth/auth/refresh_token",
        headers={"Authorization": f'bearer {data["refresh_token"]}'},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_confirmed_email(client, user):
    token_verification = auth_service.create_email_token({"sub": user.get('email')})
    response = client.get(
        f"/auth/auth/confirmed_email/{token_verification}",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Your email is already confirmed"