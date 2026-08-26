from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime

import pytest

import app.conference.service as conference_service
from app.conference.models import ConferenceAssignment
from app.conference.schemas import CommitteeCreate, ConferenceCreate, EnrollMember
from app.conference.service import (
    resolve_committee_assignment,
    resolve_session_assignment,
    verify_user_role,
)
from app.core.exceptions import AccessDeniedError, NotFoundError


@pytest.mark.anyio
async def test_denies_user_without_assignment(monkeypatch):
    async def no_assignment(*_args, **_kwargs):
        return None

    monkeypatch.setattr(
        "app.conference.service.repository.get_committee_assignment", no_assignment
    )

    with pytest.raises(AccessDeniedError, match="no assignment"):
        await resolve_committee_assignment(object(), uuid4(), committee_id=1)


@pytest.mark.anyio
async def test_denies_delegate_without_delegation(monkeypatch):
    async def invalid_assignment(*_args, **_kwargs):
        return ConferenceAssignment(
            user_id=uuid4(),
            committee_id=1,
            role="delegate",
            representation_id=None,
        )

    monkeypatch.setattr(
        "app.conference.service.repository.get_committee_assignment", invalid_assignment
    )

    with pytest.raises(AccessDeniedError, match="no delegation id"):
        await resolve_committee_assignment(object(), uuid4(), committee_id=1)


@pytest.mark.anyio
async def test_returns_valid_assignment(monkeypatch):
    assignment = ConferenceAssignment(
        user_id=uuid4(),
        committee_id=1,
        role="chair",
        representation_id=None,
    )

    async def valid_assignment(*_args, **_kwargs):
        return assignment

    monkeypatch.setattr(
        "app.conference.service.repository.get_committee_assignment", valid_assignment
    )

    result = await resolve_committee_assignment(
        object(), assignment.user_id, committee_id=1
    )

    assert result is assignment


@pytest.mark.anyio
async def test_resolves_assignment_for_a_session(monkeypatch):
    assignment = ConferenceAssignment(
        user_id=uuid4(),
        committee_id=1,
        role="chair",
        representation_id=None,
    )
    get_session_assignment = AsyncMock(return_value=assignment)
    monkeypatch.setattr(
        "app.conference.service.repository.get_session_assignment",
        get_session_assignment,
    )
    session = object()

    result = await resolve_session_assignment(
        session, assignment.user_id, session_id=9
    )

    assert result is assignment
    get_session_assignment.assert_awaited_once_with(
        session=session, user_id=assignment.user_id, session_id=9
    )


@pytest.mark.anyio
async def test_role_check_denies_a_delegate_when_a_chair_is_required(monkeypatch):
    assignment = ConferenceAssignment(
        user_id=uuid4(),
        committee_id=1,
        role="delegate",
        representation_id=3,
    )

    async def delegate_assignment(*_args, **_kwargs):
        return assignment

    monkeypatch.setattr(
        "app.conference.service.repository.get_committee_assignment", delegate_assignment
    )

    with pytest.raises(AccessDeniedError, match="requires the chair role"):
        await verify_user_role(object(), assignment.user_id, 1, "chair")


@pytest.mark.anyio
async def test_role_check_returns_matching_assignment(monkeypatch):
    assignment = ConferenceAssignment(
        user_id=uuid4(),
        committee_id=1,
        role="chair",
        representation_id=None,
    )

    async def chair_assignment(*_args, **_kwargs):
        return assignment

    monkeypatch.setattr(
        "app.conference.service.repository.get_committee_assignment", chair_assignment
    )

    assert (
        await verify_user_role(object(), assignment.user_id, 1, "chair") is assignment
    )


@pytest.mark.anyio
async def test_get_conference_info_denies_an_unassigned_user(monkeypatch):
    get_role = AsyncMock(return_value=None)
    get_conference = AsyncMock()
    monkeypatch.setattr(
        conference_service.repository, "get_user_conference_role", get_role
    )
    monkeypatch.setattr(
        conference_service.repository, "get_conference_by_id", get_conference
    )

    with pytest.raises(NotFoundError, match="Conference with id 7 not found"):
        await conference_service.get_conference_info(object(), uuid4(), 7)

    get_conference.assert_not_awaited()


@pytest.mark.anyio
async def test_get_conference_info_combines_role_and_committees(monkeypatch):
    user_id = uuid4()
    conference = {"id": 7, "name": "WebMUN", "status": "planned"}
    committees = [{"id": 3, "name": "Security Council"}]
    monkeypatch.setattr(
        conference_service.repository,
        "get_user_conference_role",
        AsyncMock(return_value="chair"),
    )
    monkeypatch.setattr(
        conference_service.repository,
        "get_conference_by_id",
        AsyncMock(return_value=conference),
    )
    monkeypatch.setattr(
        conference_service.repository,
        "list_committees_for_conference",
        AsyncMock(return_value=committees),
    )

    result = await conference_service.get_conference_info(object(), user_id, 7)

    assert result == {
        "id": 7,
        "name": "WebMUN",
        "status": "planned",
        "caller_role": "chair",
        "committees": committees,
    }


@pytest.mark.anyio
async def test_create_committee_requires_a_conference_manager(monkeypatch):
    create_committee = AsyncMock()
    monkeypatch.setattr(
        conference_service.repository,
        "get_user_conference_role",
        AsyncMock(return_value="delegate"),
    )
    monkeypatch.setattr(
        conference_service.repository, "create_committee", create_committee
    )

    with pytest.raises(AccessDeniedError, match="owners and admins"):
        await conference_service.create_committee(
            object(), uuid4(), 7, CommitteeCreate(name="Security Council", code="SC")
        )

    create_committee.assert_not_awaited()


@pytest.mark.anyio
async def test_create_committee_forwards_an_authorized_request(monkeypatch):
    session = AsyncMock()
    user_id = uuid4()
    payload = CommitteeCreate(name="Security Council", code="SC")
    created = {"id": 3, "conference_id": 7, "name": payload.name}
    create_committee = AsyncMock(return_value=created)
    monkeypatch.setattr(
        conference_service.repository,
        "get_user_conference_role",
        AsyncMock(return_value="admin"),
    )
    monkeypatch.setattr(
        conference_service.repository, "create_committee", create_committee
    )

    result = await conference_service.create_committee(session, user_id, 7, payload)

    assert result == created
    create_committee.assert_awaited_once_with(
        session=session, conference_id=7, payload=payload
    )
    session.commit.assert_awaited_once()


@pytest.mark.anyio
async def test_enroll_member_forwards_an_authorized_request(monkeypatch):
    session = AsyncMock()
    user_id = uuid4()
    payload = EnrollMember(
        name="Ada Lovelace", email="ada@example.com", role="delegate"
    )
    enrolled = {"id": 4, "email": payload.email, "role": payload.role}
    enroll_member = AsyncMock(return_value=enrolled)
    monkeypatch.setattr(
        conference_service.repository,
        "get_user_conference_role",
        AsyncMock(return_value="owner"),
    )
    monkeypatch.setattr(
        conference_service.repository, "enroll_member", enroll_member
    )

    result = await conference_service.enroll_member(session, user_id, 7, payload)

    assert result == enrolled
    enroll_member.assert_awaited_once_with(
        session=session, conference_id=7, payload=payload
    )
    session.commit.assert_awaited_once()


@pytest.mark.anyio
async def test_create_conference_commits_after_creating_it(monkeypatch):
    session = AsyncMock()
    user_id = uuid4()
    payload = ConferenceCreate(
        name="WebMUN",
        start_date=datetime.now(),
        end_date=datetime.now(),
    )
    create_conference = AsyncMock(return_value=7)
    monkeypatch.setattr(
        conference_service.repository, "create_conference", create_conference
    )

    conference_id = await conference_service.create_conference(
        session, user_id, payload
    )

    assert conference_id == 7
    create_conference.assert_awaited_once_with(
        session=session, user_id=user_id, payload=payload
    )
    session.commit.assert_awaited_once()


@pytest.mark.anyio
async def test_get_user_conferences_returns_dashboard_summaries(monkeypatch):
    session = object()
    user_id = uuid4()
    summaries = [
        {
            "id": 7,
            "name": "WebMUN",
            "logo": None,
            "color": "#0f172a",
            "status": "planned",
            "caller_role": "owner",
        }
    ]
    get_user_conferences = AsyncMock(return_value=summaries)
    monkeypatch.setattr(
        conference_service.repository, "get_user_conferences", get_user_conferences
    )

    result = await conference_service.get_user_conferences(session, user_id)

    assert result == summaries
    get_user_conferences.assert_awaited_once_with(session=session, user_id=user_id)
