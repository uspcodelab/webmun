from dataclasses import dataclass
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
from pydantic import BaseModel
from app.core.config import Settings


class AuthUser(BaseModel):
    user_id: UUID
    email: str | None

class InvalidTokenError(Exception):
    pass


class AuthService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def verify_user_token(
            self,
            token: str # self contained token that already has info like id, email, etc
    ) -> AuthUser:
        """Local Verification of user's JWT + Supabase JWT Secret"""
        try:
            payload = jwt.decode(
                token,
                self.settings.SUPABASE_JWT_SECRET.get_secret_value(),
                self.settings.JWT_ALGORITHM,
                audience="authenticated"  
            )

            return AuthUser(user_id=UUID(payload.get("id")), email=payload.get("email"))

        except jwt.ExpiredSignatureError:
            raise InvalidTokenError("Token has expired")

        except jwt.InvalidTokenError:
            raise InvalidTokenError("Token is invalid")
