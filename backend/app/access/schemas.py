from pydantic import BaseModel

from . import enums


class SessionRepresentation(BaseModel):
    role: enums.SessionRoles
    representation_id: int | None
