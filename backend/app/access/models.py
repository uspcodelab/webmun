from dataclasses import dataclass
from typing import Literal
from uuid import UUID


@dataclass(frozen=True)
class CommitteeAssignment:
    """Object that holds info about an UUID to a commitee and Delegation / Chair"""
    user_id: UUID
    committee_id: int  # TODO: remove this to map out to committees/conferences
    role: Literal["chair", "delegate"]
    representation_id: int | None
