from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.service import (
    AuthUser,
    TokenExpiredError,
    TokenInvalidError,
    verify_jwt_token,
)
from app.core.config import Settings, get_settings

bearer = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthUser:
    """Dependency injection to get current user"""
    try:
        return verify_jwt_token(
            token=credentials.credentials,
            settings=settings,
        )
    except TokenExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # TODO: map this out to an outer table, since both WS and HTTP uses this
            detail="token_expired",  
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except TokenInvalidError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # TODO: map this out to an outer table, since both WS and HTTP uses this
            detail="token_invalid",  
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
