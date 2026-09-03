from dataclasses import dataclass
from uuid import uuid4

import pytest

from app.access.models import AccessibleCommittee, CommitteeAssignment
from app.access.service import (
    get_my_conference_access,
    resolve_committee_assignment,
    verify_can_manage_conference,
    verify_conference_assignment_can_grant_session_access,
    verify_user_role,
)
from app.core.exceptions import AccessDeniedError


@dataclass(frozen=True)
class Conference:
    id: int
    owner_id: object


@dataclass(frozen=True)
class ConferenceAssignment:
    role: str
    committee_id: int | None


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


@pytest.mark.anyio
async def test_get_my_conference_access_includes_owner_fallback(monkeypatch):
    owner_id = uuid4()

    async def repo_get_conference(*_args, **_kwargs):
        return Conference(id=1, owner_id=owner_id)

    async def no_assignments(*_args, **_kwargs):
        return []

    async def no_accessible_committees(*_args, **_kwargs):
        return []

    monkeypatch.setattr(
        "app.access.service.conference_repository.get_user_conference",
        repo_get_conference,
    )
    monkeypatch.setattr(
        "app.access.service.conference_repository.list_user_conference_assignments",
        no_assignments,
    )
    monkeypatch.setattr(
        "app.access.service.list_accessible_conference_committees",
        no_accessible_committees,
    )

    result = await get_my_conference_access(object(), owner_id, 1)

    assert result.roles == ["owner"]
    assert result.committee_roles == []
    assert result.accessible_committees == []
    assert result.can_manage_conference is True


@pytest.mark.anyio
async def test_get_my_conference_access_splits_conference_and_committee_roles(
    monkeypatch,
):
    user_id = uuid4()

    async def repo_get_conference(*_args, **_kwargs):
        return Conference(id=1, owner_id=uuid4())

    async def assignments(*_args, **_kwargs):
        return [
            ConferenceAssignment(role="press", committee_id=None),
            ConferenceAssignment(role="moderator", committee_id=10),
        ]

    async def accessible_committees(*_args, **_kwargs):
        return [
            AccessibleCommittee(
                committee_id=10,
                role="delegate",
                representation_id=3,
            )
        ]

    monkeypatch.setattr(
        "app.access.service.conference_repository.get_user_conference",
        repo_get_conference,
    )
    monkeypatch.setattr(
        "app.access.service.conference_repository.list_user_conference_assignments",
        assignments,
    )
    monkeypatch.setattr(
        "app.access.service.list_accessible_conference_committees",
        accessible_committees,
    )

    result = await get_my_conference_access(object(), user_id, 1)

    assert result.roles == ["press"]
    assert result.committee_roles[0].committee_id == 10
    assert result.committee_roles[0].role == "moderator"
    assert result.accessible_committees[0].committee_id == 10
    assert result.accessible_committees[0].role == "delegate"
    assert result.accessible_committees[0].representation_id == 3
    assert result.can_manage_conference is False
