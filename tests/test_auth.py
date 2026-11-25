
import hashlib
import secrets
import base64

from fastapi.testclient import TestClient
from app.models.role import Role
from app.models.user import User


TEST_PASSWORD = "TestPassword123!"


def create_password_hash(password):
    salt = secrets.token_bytes(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600000
    )

    return (
        f"pbkdf2_sha256$"
        f"{base64.b64encode(salt).decode()}$"
        f"{base64.b64encode(hashed).decode()}"
    )


def create_test_admin(db_session):
    role = Role(role_name="Admin")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)

    admin = User(
        username="admin_test",
        email="admin@test.com",
        password_hash=create_password_hash(TEST_PASSWORD),
        role_id=role.role_id
    )

    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)

    return admin


def test_login_success(client, db_session):
    create_test_admin(db_session)

    response = client.post(
        "/auth/login",
        json={
            "username": "admin_test",
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_password(client, db_session):
    create_test_admin(db_session)

    response = client.post(
        "/auth/login",
        json={
            "username": "admin_test",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401


def test_login_unknown_user(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "unknown_user",
            "password": "some_password"
        }
    )

    assert response.status_code == 401


def test_get_current_user_profile(client, db_session):
    create_test_admin(db_session)

    login_response = client.post(
        "/auth/login",
        json={
            "username": "admin_test",
            "password": TEST_PASSWORD
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["username"] == "admin_test"


def test_admin_access(client, db_session):
    create_test_admin(db_session)

    login_response = client.post(
        "/auth/login",
        json={
            "username": "admin_test",
            "password": TEST_PASSWORD
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/admin-check",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Admin access granted"


def test_operator_cannot_access_admin_endpoint(client, db_session):
    operator_role = Role(role_name="Operator")
    db_session.add(operator_role)
    db_session.commit()
    db_session.refresh(operator_role)

    password = "Operator123!"

    operator = User(
        username="test_operator",
        email="operator@test.com",
        password_hash=create_password_hash(password),
        role_id=operator_role.role_id
    )

    db_session.add(operator)
    db_session.commit()

    login_response = client.post(
        "/auth/login",
        json={
            "username": "test_operator",
            "password": password
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/admin-check",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
