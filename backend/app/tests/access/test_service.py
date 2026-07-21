from uuid import uuid4

import pytest

from app.access.models import CommitteeAssignment
from app.access.service import (
    AccessDenied,
    resolve_committee_assignment,
    verify_user_role,
)


@pytest.mark.anyio
async def test_denies_user_without_assignment(monkeypatch):
    async def no_assignment(*_args, **_kwargs):
        return None

    monkeypatch.setattr("app.access.service.get_committee_assignment", no_assignment)

    with pytest.raises(AccessDenied, match="no committee assignment"):
        await resolve_committee_assignment(object(), uuid4(), 1)


@pytest.mark.anyio
async def test_denies_delegate_without_delegation(monkeypatch):
    async def invalid_assignment(*_args, **_kwargs):
        return CommitteeAssignment(
            user_id=uuid4(),
            committee_id=1,
            role="delegate",
            representation_id=None,
        )

    monkeypatch.setattr(
        "app.access.service.get_committee_assignment", invalid_assignment
    )

    with pytest.raises(AccessDenied, match="no delegation id"):
        await resolve_committee_assignment(object(), uuid4(), 1)


@pytest.mark.anyio
async def test_returns_valid_assignment(monkeypatch):
    assignment = CommitteeAssignment(
        user_id=uuid4(),
        committee_id=1,
        role="chair",
        representation_id=None,
    )

    async def valid_assignment(*_args, **_kwargs):
        return assignment

    monkeypatch.setattr("app.access.service.get_committee_assignment", valid_assignment)

    result = await resolve_committee_assignment(object(), assignment.user_id, 1)

    assert result is assignment


@pytest.mark.anyio
async def test_role_check_denies_a_delegate_when_a_chair_is_required(monkeypatch):
    assignment = CommitteeAssignment(
        user_id=uuid4(),
        committee_id=1,
        role="delegate",
        representation_id=3,
    )

    async def delegate_assignment(*_args, **_kwargs):
        return assignment

    monkeypatch.setattr(
        "app.access.service.get_committee_assignment", delegate_assignment
    )

    with pytest.raises(AccessDenied, match="requires the chair role"):
        await verify_user_role(object(), assignment.user_id, 1, "chair")


@pytest.mark.anyio
async def test_role_check_returns_matching_assignment(monkeypatch):
    assignment = CommitteeAssignment(
        user_id=uuid4(),
        committee_id=1,
        role="chair",
        representation_id=None,
    )

    async def chair_assignment(*_args, **_kwargs):
        return assignment

    monkeypatch.setattr("app.access.service.get_committee_assignment", chair_assignment)

    assert await verify_user_role(object(), assignment.user_id, 1, "chair") is assignment
