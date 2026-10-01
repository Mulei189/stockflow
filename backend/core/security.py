import bcrypt
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(
        password.encode("utf-8"),
        salt
    ).decode("utf-8")

def verify_password(
    plain_password: str,
    hashed_password: str
):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def create_access_token(data: dict):
    payload = data.copy()

    payload["exp"] = (datetime.utcnow() + timedelta(days=7))
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )