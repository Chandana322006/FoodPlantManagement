from fastapi.testclient import TestClient

from app.main import app
import pytest
import json
import time
import base64
import hmac
import hashlib

from app.routers.auth_router import SECRET_KEY
client = TestClient(app)


def test_products_without_token():
    response = client.get("/products/")

    assert response.status_code == 401


def test_products_with_admin_token():
    login_response = client.post(
        "/auth/login",
        json={
            "username": "admin_test",
            "password": "Ashwini@2006"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/products/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
@pytest.mark.parametrize("endpoint", [
    "/products/",
    "/raw-materials/",
    "/suppliers/",
    "/production-lines/",
    "/batches/",
    "/production-records/",
    "/quality-tests/",
    "/approvals/",
    "/audit-logs/",
    "/machines/",
    "/material-usage/",
    "/users/",
    "/roles/",
    "/imports/jobs",
    "/reports/production",
    "/reports/quality",
    "/exports/reports/csv",
    "/exports/reports/pdf"
])
def test_protected_endpoints_without_token(endpoint):
    response = client.get(endpoint)

    assert response.status_code == 401
def test_products_with_invalid_token():
    response = client.get(
        "/products/",
        headers={"Authorization": "Bearer invalid.token"}
    )

    assert response.status_code == 401
def test_products_with_expired_token():
    payload = {
        "user_id": 1,
        "exp": int(time.time()) - 3600
    }

    encoded_payload = base64.urlsafe_b64encode(
        json.dumps(payload).encode()
    ).decode().rstrip("=")

    signature = hmac.new(
        SECRET_KEY.encode(),
        encoded_payload.encode(),
        hashlib.sha256
    ).digest()

    encoded_signature = base64.urlsafe_b64encode(
        signature
    ).decode().rstrip("=")

    expired_token = f"{encoded_payload}.{encoded_signature}"

    response = client.get(
        "/products/",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Access token expired"