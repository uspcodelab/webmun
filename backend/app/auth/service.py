import jwt
from uuid import UUID
from pydantic import BaseModel
from app.core.config import Settings

# Self documented errors: might be better for protection
class TokenInvalidError(Exception):
    pass 

class TokenExpiredError(Exception):
    pass

class AuthUser(BaseModel):
    user_id: UUID
    email: str | None


def verify_jwt_token(
    token: str,  # self contained token that already has info like id, email, etc
    settings: Settings,
) -> AuthUser:
    """Local Verification of user's JWT + Supabase JWT Secret"""
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET.get_secret_value(),
            settings.JWT_ALGORITHM,
            audience="authenticated",
        )

        return AuthUser(user_id=UUID(payload.get("sub")), email=payload.get("email"))
    
    except jwt.exceptions.ExpiredSignatureError:
        raise TokenExpiredError("Access token expired")
    
    except jwt.exceptions.InvalidTokenError:
        raise TokenInvalidError("Access token invalid")
