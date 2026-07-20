import jwt
from uuid import UUID
from pydantic import BaseModel
from app.core.config import Settings


class AuthUser(BaseModel):
    user_id: UUID
    email: str | None

class InvalidTokenError(Exception):
    pass

def verify_jwt_token(
        token: str, # self contained token that already has info like id, email, etc
        settings: Settings
) -> AuthUser:
    """Local Verification of user's JWT + Supabase JWT Secret"""
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET.get_secret_value(),
            settings.JWT_ALGORITHM,
            audience="authenticated"  
        )

        return AuthUser(user_id=UUID(payload.get("id")), email=payload.get("email"))

    except jwt.ExpiredSignatureError:
        raise InvalidTokenError("Token has expired")

    except jwt.InvalidTokenError:
        raise InvalidTokenError("Token is invalid")
