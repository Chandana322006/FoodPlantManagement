
from datetime import date
import hashlib
import secrets
import base64

from app.models.role import Role
from app.models.user import User
from app.models.product import Product
from app.models.production_line import ProductionLine
from app.models.batch import Batch


TEST_PASSWORD = "TestPassword123!"


def create_test_password_hash(password):
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


def create_test_batch(db_session):
    role = Role(role_name="Admin")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)

    user = User(
        username="test_admin",
        email="admin@test.com",
        password_hash=create_test_password_hash(TEST_PASSWORD),
        role_id=role.role_id
    )
    db_session.add(user)

    product = Product(
        product_name="Frozen Peas",
        category="Frozen Food",
        unit_price=100
    )
    line = ProductionLine(
        line_name="Test Line",
        location="Chennai"
    )

    db_session.add_all([product, line])
    db_session.commit()
    db_session.refresh(product)
    db_session.refresh(line)
    db_session.refresh(user)

    batch = Batch(
        production_date=date(2026, 1, 1),
        shift="Morning",
        product_id=product.product_id,
        line_id=line.line_id,
        created_by=user.user_id
    )

    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)

    return batch, user


def get_admin_headers(client):
    login_response = client.post(
        "/auth/login",
        json={
            "username": "test_admin",
            "password": TEST_PASSWORD
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_create_pending_approval(client, db_session):
    batch, user = create_test_batch(db_session)
    headers = get_admin_headers(client)

    response = client.post(
        "/approvals/",
        json={
            "batch_id": batch.batch_id,
            "reviewer_id": user.user_id,
            "comments": "Please review this batch"
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Pending"


def test_approve_batch(client, db_session):
    batch, user = create_test_batch(db_session)
    headers = get_admin_headers(client)

    create_response = client.post(
        "/approvals/",
        json={
            "batch_id": batch.batch_id,
            "reviewer_id": user.user_id,
            "comments": "Ready for review"
        },
        headers=headers
    )

    assert create_response.status_code == 200

    approval_id = create_response.json()["approval_id"]

    response = client.put(
        f"/approvals/{approval_id}",
        json={
            "status": "Approved",
            "comments": "Quality verified"
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Approved"

    db_session.refresh(batch)
    assert batch.status == "Approved"


def test_reject_batch(client, db_session):
    batch, user = create_test_batch(db_session)
    headers = get_admin_headers(client)

    create_response = client.post(
        "/approvals/",
        json={
            "batch_id": batch.batch_id,
            "reviewer_id": user.user_id,
            "comments": "Review required"
        },
        headers=headers
    )

    assert create_response.status_code == 200

    approval_id = create_response.json()["approval_id"]

    response = client.put(
        f"/approvals/{approval_id}",
        json={
            "status": "Rejected",
            "comments": "Quality issue detected"
        },
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Rejected"

    db_session.refresh(batch)
    assert batch.status == "Rejected"
