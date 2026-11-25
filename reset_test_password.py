
import hashlib
import secrets
import base64
from getpass import getpass

from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()

try:
    user = db.query(User).filter(
        User.username == "admin_test"
    ).first()

    if not user:
        print("User not found!")
    else:
        password = getpass("Enter your new password: ")

        if len(password) < 8:
            print("Password must contain at least 8 characters.")
        else:
            salt = secrets.token_bytes(16)

            hashed = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode(),
                salt,
                600000
            )

            salt_text = base64.b64encode(salt).decode()
            hash_text = base64.b64encode(hashed).decode()

            user.password_hash = (
                f"pbkdf2_sha256${salt_text}${hash_text}"
            )

            db.commit()
            print("Password updated successfully!")

finally:
    db.close()
