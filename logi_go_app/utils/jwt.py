# utils/jwt.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings

ACCESS_TOKEN_LIFETIME = settings.ACCESS_TOKEN_LIFETIME  # minutes
REFRESH_TOKEN_LIFETIME = settings.REFRESH_TOKEN_LIFETIME  # days


def generate_jwt_pair(user):
    now = datetime.utcnow()

    access_payload = {
        "id": user.id,
        "email": user.email,
        "type": "access",
        "exp": now + timedelta(minutes=ACCESS_TOKEN_LIFETIME),
        "iat": now,
    }

    refresh_payload = {
        "id": user.id,
        "type": "refresh",
        "exp": now + timedelta(days=REFRESH_TOKEN_LIFETIME),
        "iat": now,
    }

    access_token = jwt.encode(
        access_payload,
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    refresh_token = jwt.encode(
        refresh_payload,
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    return access_token, refresh_token


def verify_token(token):
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"],
    )