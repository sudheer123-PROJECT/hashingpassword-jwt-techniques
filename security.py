
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

import jwt
from jwt import InvalidTokenError
from dotenv import load_dotenv
from pwdlib import PasswordHash


# 1. Load .env file
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY or SECRET_KEY in {
    "PASTE_YOUR_GENERATED_SECRET_HERE",
    "YOUR_ACTUAL_GENERATED_SECRET_KEY"
}:
    raise RuntimeError(
        "SECRET_KEY missing. Generate a key and save it in .env"
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# 2. Password hashing setup
password_hash = PasswordHash.recommended()


# 3. Hash password
def hash_password(password: str):
    return password_hash.hash(password)


# 4. Verify password
def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(
        plain_password,
        hashed_password
    )


# 5. Create JWT token
def create_access_token(user_id: int):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# 6. Verify JWT token
def verify_access_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not isinstance(user_id, str) or not user_id.isdigit():
            return None

        return int(user_id)

    except InvalidTokenError:
        return None
