from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.database.mongodb import users_collection


SECRET_KEY = "customer-support-secret-key-change-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(username: str, role: str):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def register_user(user):

    existing_user = users_collection.find_one({
        "username": user.username
    })

    if existing_user:
        return None, "Username already exists"

    hashed_password = hash_password(user.password)

    user_data = {
        "username": user.username,
        "password": hashed_password,
        "role": user.role,
        "created_at": datetime.now(timezone.utc)
    }

    result = users_collection.insert_one(user_data)

    return str(result.inserted_id), None


def login_user(user):

    existing_user = users_collection.find_one({
        "username": user.username
    })

    if not existing_user:
        return None, "Invalid username or password"

    if not verify_password(
        user.password,
        existing_user["password"]
    ):
        return None, "Invalid username or password"

    token = create_access_token(
        existing_user["username"],
        existing_user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": existing_user["role"]
    }, None