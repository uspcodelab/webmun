from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import ec

import app.auth.service as auth_service
from app.auth.service import TokenExpiredError, TokenInvalidError, verify_jwt_token


@pytest.fixture
def signing_key(monkeypatch):
    private_key = ec.generate_private_key(ec.SECP256R1())
    jwk_client = SimpleNamespace(
        get_signing_key_from_jwt=lambda _: SimpleNamespace(key=private_key.public_key())
    )
    monkeypatch.setattr(auth_service, "get_jwk_client", lambda _: jwk_client)
    return private_key


@pytest.fixture
def settings():
    return SimpleNamespace(SUPABASE_URL="https://supabase.example.test")


def make_token(*, user_id, expires_at: datetime, signing_key) -> str:
    return jwt.encode(
        {
            "sub": str(user_id),
            "email": "delegate@example.test",
            "aud": "authenticated",
            "exp": expires_at,
        },
        signing_key,
        algorithm="ES256",
    )


def test_verifies_valid_supabase_style_token(settings, signing_key):
    user_id = uuid4()
    token = make_token(
        user_id=user_id,
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
        signing_key=signing_key,
    )

    user = verify_jwt_token(token, settings)

    assert user.user_id == user_id
    assert user.email == "delegate@example.test"


def test_rejects_expired_token(settings, signing_key):
    token = make_token(
        user_id=uuid4(),
        expires_at=datetime.now(UTC) - timedelta(minutes=1),
        signing_key=signing_key,
    )

    with pytest.raises(TokenExpiredError):
        verify_jwt_token(token, settings)


def test_rejects_invalid_token(settings, signing_key):
    with pytest.raises(TokenInvalidError):
        verify_jwt_token("not-a-jwt", settings)
