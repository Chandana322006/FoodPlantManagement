
import os
import json
import time
import hmac
import hashlib
import base64

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.role import Role


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

security = HTTPBearer(auto_error=False)

SECRET_KEY = os.getenv(
    "FOOD_PLANT_SECRET_KEY",
    "development-only-change-this-secret"
)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


def verify_password(password: str, stored_hash: str) -> bool:

    try:
        algorithm, salt_text, hash_text = stored_hash.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        salt = base64.b64decode(salt_text)
        expected_hash = base64.b64decode(hash_text)

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            600000
        )

        return hmac.compare_digest(
            actual_hash,
            expected_hash
        )

    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int) -> str:

    payload = {
        "user_id": user_id,
        "exp": int(time.time()) + 3600
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

    return f"{encoded_payload}.{encoded_signature}"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    try:
        encoded_payload, encoded_signature = (
            credentials.credentials.split(".")
        )

        expected_signature = hmac.new(
            SECRET_KEY.encode(),
            encoded_payload.encode(),
            hashlib.sha256
        ).digest()

        actual_signature = base64.urlsafe_b64decode(
            encoded_signature + "=" * (-len(encoded_signature) % 4)
        )

        if not hmac.compare_digest(
            expected_signature,
            actual_signature
        ):
            raise ValueError("Invalid signature")

        payload = json.loads(
            base64.urlsafe_b64decode(
                encoded_payload + "=" * (-len(encoded_payload) % 4)
            )
        )

        if payload["exp"] < time.time():
            raise HTTPException(
                status_code=401,
                detail="Access token expired"
            )

        user = db.query(User).filter(
            User.user_id == payload["user_id"]
        ).first()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=401,
                detail="Invalid or inactive user"
            )

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )


def require_roles(*allowed_roles):

    def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

        role = db.query(Role).filter(
            Role.role_id == current_user.role_id
        ).first()

        if not role or role.role_name.lower() not in [
            name.lower() for name in allowed_roles
        ]:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == login_data.username
    ).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(user.user_id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 3600
    }

@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    role = db.query(Role).filter(
        Role.role_id == current_user.role_id
    ).first()

    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "role": role.role_name if role else None,
        "is_active": current_user.is_active
    }


@router.get("/admin-check")
def admin_check(
    current_user: User = Depends(require_roles("Admin"))
):
    return {
        "message": "Admin access granted",
        "username": current_user.username
    }
