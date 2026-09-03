from uuid import uuid4

import pytest

from app.access.models import CommitteeAssignment
from app.access.service import (
    resolve_committee_assignment,
    verify_can_manage_conference,
    verify_conference_assignment_can_grant_session_access,
    verify_user_role,
)
from app.core.exceptions import AccessDeniedError


@pytest.mark.anyio
async def test_denies_user_without_assignment(monkeypatch):
    async def no_assignment(*_args, **_kwargs):
        return None

    monkeypatch.setattr("app.access.service.get_committee_assignment", no_assignment)

    with pytest.raises(AccessDeniedError, match="no committee assignment"):
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

    with pytest.raises(AccessDeniedError, match="no delegation id"):
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

    with pytest.raises(AccessDeniedError, match="requires the chair role"):
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

    assert (
        await verify_user_role(object(), assignment.user_id, 1, "chair") is assignment
    )


@pytest.mark.anyio
async def test_conference_management_check_denies_unprivileged_user(monkeypatch):
    async def cannot_manage(*_args, **_kwargs):
        return False

    monkeypatch.setattr(
        "app.access.service.has_conference_management_role", cannot_manage
    )

    with pytest.raises(AccessDeniedError, match="cannot manage"):
        await verify_can_manage_conference(object(), uuid4(), 1)


@pytest.mark.anyio
async def test_conference_management_check_allows_privileged_user(monkeypatch):
    async def can_manage(*_args, **_kwargs):
        return True

    monkeypatch.setattr("app.access.service.has_conference_management_role", can_manage)

    await verify_can_manage_conference(object(), uuid4(), 1)


@pytest.mark.anyio
async def test_session_access_projection_check_denies_unprivileged_assignment(
    monkeypatch,
):
    async def cannot_grant(*_args, **_kwargs):
        return False

    monkeypatch.setattr(
        "app.access.service.has_conference_assignment_for_session_access",
        cannot_grant,
    )

    with pytest.raises(AccessDeniedError, match="cannot grant"):
        await verify_conference_assignment_can_grant_session_access(
            object(), uuid4(), 1, 10
        )


@pytest.mark.anyio
async def test_session_access_projection_check_allows_privileged_assignment(
    monkeypatch,
):
    async def can_grant(*_args, **_kwargs):
        return True

    monkeypatch.setattr(
        "app.access.service.has_conference_assignment_for_session_access",
        can_grant,
    )

    await verify_conference_assignment_can_grant_session_access(
        object(), uuid4(), 1, 10
    )
