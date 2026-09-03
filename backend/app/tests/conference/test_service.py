from datetime import datetime
from uuid import uuid4

import pytest

from app.conference.models import (
    Committee,
    CommitteeAssignment,
    Conference,
)
from app.conference.schemas import CommitteeCreate, ConferenceCreate
from app.conference.service import (
    create_committee,
    create_conference,
    promote_conference_assignment_to_committee_assignment,
)
from app.core.exceptions import AccessDeniedError, ConflictError


class FakeSession:
    def __init__(self) -> None:
        self.commits = 0

    async def commit(self) -> None:
        self.commits += 1


def conference(owner_id):
    now = datetime.now()
    return Conference(
        id=1,
        name="I WebMUN",
        status="planned",
        owner_id=owner_id,
        location=None,
        logo_url=None,
        theme_color=None,
        start_date=None,
        end_date=None,
        created_at=now,
        updated_at=now,
    )


def committee():
    now = datetime.now()
    return Committee(
        id=10,
        conference_id=1,
        name="CSNU",
        acronym="CSNU",
        committee_type="Traditional",
        logo_url=None,
        theme_color="#1d4ed8",
        status="planned",
        created_at=now,
        updated_at=now,
    )


@pytest.mark.anyio
async def test_create_conference_adds_owner_assignment(monkeypatch):
    owner_id = uuid4()
    fake_session = FakeSession()
    created_assignments = []

    async def repo_create_conference(*_args, **_kwargs):
        return conference(owner_id)

    async def repo_create_assignment(*_args, **kwargs):
        created_assignments.append(
            {
                "conference_id": kwargs["conference_id"],
                "user_id": kwargs["user_id"],
                "role": kwargs["role"],
            }
        )

    monkeypatch.setattr(
        "app.conference.service.repository.create_conference", repo_create_conference
    )
    monkeypatch.setattr(
        "app.conference.service.repository.create_conference_assignment",
        repo_create_assignment,
    )

    result = await create_conference(
        fake_session,
        data=ConferenceCreate(name="I WebMUN"),
        owner_id=owner_id,
    )

    assert result.id == 1
    assert created_assignments == [
        {
            "conference_id": 1,
            "user_id": owner_id,
            "role": "owner",
        }
    ]
    assert fake_session.commits == 1


@pytest.mark.anyio
async def test_create_committee_requires_conference_management_role(monkeypatch):
    async def cannot_manage(*_args, **_kwargs):
        raise AccessDeniedError("User cannot manage this conference")

    monkeypatch.setattr(
        "app.conference.service.access.verify_can_manage_conference", cannot_manage
    )

    with pytest.raises(AccessDeniedError, match="cannot manage"):
        await create_committee(
            FakeSession(),
            conference_id=1,
            user_id=uuid4(),
            data=CommitteeCreate(name="CSNU"),
        )


@pytest.mark.anyio
async def test_create_committee_commits_when_user_can_manage(monkeypatch):
    fake_session = FakeSession()

    async def can_manage(*_args, **_kwargs):
        return None

    async def repo_create_committee(*_args, **_kwargs):
        return committee()

    monkeypatch.setattr(
        "app.conference.service.access.verify_can_manage_conference", can_manage
    )
    monkeypatch.setattr(
        "app.conference.service.repository.create_committee", repo_create_committee
    )

    result = await create_committee(
        fake_session,
        conference_id=1,
        user_id=uuid4(),
        data=CommitteeCreate(name="CSNU"),
    )

    assert result.id == 10
    assert fake_session.commits == 1


@pytest.mark.anyio
async def test_promotion_refuses_to_replace_delegate_assignment(monkeypatch):
    async def can_grant(*_args, **_kwargs):
        return None

    async def existing_delegate(*_args, **_kwargs):
        return CommitteeAssignment(
            user_id=uuid4(),
            committee_id=10,
            role="delegate",
            representation_id=3,
        )

    monkeypatch.setattr(
        "app.conference.service.access.verify_conference_assignment_can_grant_session_access",
        can_grant,
    )
    monkeypatch.setattr(
        "app.conference.service.repository.get_committee_assignment", existing_delegate
    )

    with pytest.raises(ConflictError, match="delegate"):
        await promote_conference_assignment_to_committee_assignment(
            FakeSession(),
            conference_id=1,
            committee_id=10,
            user_id=uuid4(),
        )


@pytest.mark.anyio
async def test_promotion_creates_committee_session_access(monkeypatch):
    fake_session = FakeSession()
    user_id = uuid4()

    async def can_grant(*_args, **_kwargs):
        return None

    async def no_existing_assignment(*_args, **_kwargs):
        return None

    async def upsert_assignment(*_args, **kwargs):
        return CommitteeAssignment(
            user_id=kwargs["user_id"],
            committee_id=kwargs["committee_id"],
            role=kwargs["role"],
            representation_id=None,
        )

    monkeypatch.setattr(
        "app.conference.service.access.verify_conference_assignment_can_grant_session_access",
        can_grant,
    )
    monkeypatch.setattr(
        "app.conference.service.repository.get_committee_assignment",
        no_existing_assignment,
    )
    monkeypatch.setattr(
        "app.conference.service.repository.upsert_committee_session_assignment",
        upsert_assignment,
    )

    result = await promote_conference_assignment_to_committee_assignment(
        fake_session,
        conference_id=1,
        committee_id=10,
        user_id=user_id,
    )

    assert result.user_id == user_id
    assert result.role == "chair"
    assert result.representation_id is None
    assert fake_session.commits == 1
