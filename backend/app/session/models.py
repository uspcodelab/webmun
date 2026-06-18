# This file defines internal models not used as schemas for the application
# Even though it's internal, some things may be sent out to public (TODO:like SessionLiveState)
from pydantic import BaseModel
from enum import Enum

# This may be used for SessionLiveState as well, but mainly used in SessionActor
class DelegationContext(BaseModel):
    id: int
    seat: str
    name: str
    code: str

class SessionRole(str, Enum):
    CHAIR = "CHAIR"
    DELEGATE = "DELEGATE"
    # further roles are put here

class SessionActor(BaseModel):
    role: SessionRole
    display_name: str = "Placeholder"
    delegation: DelegationContext | None = None

