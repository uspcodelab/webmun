from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

import jwt
import pytest

from app.auth.service import TokenExpiredError, TokenInvalidError, verify_jwt_token


class FakeSecret:
    def __init__(self, value: str):
        self.value = value

    def get_secret_value(self) -> str:
        return self.value


@pytest.fixture
def settings():
    return SimpleNamespace(
        SUPABASE_JWT_SECRET=FakeSecret("test-secret-that-is-at-least-32-bytes"),
        JWT_ALGORITHM="HS256",
    )


def make_token(*, user_id, expires_at: datetime) -> str:
    return jwt.encode(
        {
            "sub": str(user_id),
            "email": "delegate@example.test",
            "aud": "authenticated",
            "exp": expires_at,
        },
        "test-secret-that-is-at-least-32-bytes",
        algorithm="HS256",
    )


def test_verifies_valid_supabase_style_token(settings):
    user_id = uuid4()
    token = make_token(
        user_id=user_id,
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )

    user = verify_jwt_token(token, settings)

    assert user.user_id == user_id
    assert user.email == "delegate@example.test"


def test_rejects_expired_token(settings):
    token = make_token(
        user_id=uuid4(),
        expires_at=datetime.now(UTC) - timedelta(minutes=1),
    )

    with pytest.raises(TokenExpiredError):
        verify_jwt_token(token, settings)


def test_rejects_invalid_token(settings):
    with pytest.raises(TokenInvalidError):
        verify_jwt_token("not-a-jwt", settings)
