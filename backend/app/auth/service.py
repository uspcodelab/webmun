import jwt
from functools import lru_cache
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


@lru_cache
def get_jwk_client(supabase_url: str) -> jwt.PyJWKClient:
    """Cache Supabase's public signing keys for asymmetric access tokens."""
    return jwt.PyJWKClient(
        f"{supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"
    )


def verify_jwt_token(
    token: str,  # self contained token that already has info like id, email, etc
    settings: Settings,
) -> AuthUser:
    """Verify either legacy HS256 or current Supabase ES256 access tokens."""
    try:
        algorithm = jwt.get_unverified_header(token).get("alg")

        if algorithm == "HS256":
            key = settings.SUPABASE_JWT_SECRET.get_secret_value()
        elif algorithm == "ES256":
            key = get_jwk_client(str(settings.SUPABASE_URL)).get_signing_key_from_jwt(
                token
            ).key
        else:
            raise TokenInvalidError("Unsupported access token algorithm")

        payload = jwt.decode(
            token,
            key,
            algorithms=[algorithm],
            audience="authenticated",
        )

        return AuthUser(user_id=UUID(payload["sub"]), email=payload.get("email"))

    except jwt.exceptions.ExpiredSignatureError:
        raise TokenExpiredError("Access token expired")

    except (jwt.exceptions.PyJWTError, KeyError, TypeError, ValueError):
        raise TokenInvalidError("Access token invalid")
