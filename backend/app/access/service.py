from uuid import UUID
from app.access.models import CommitteeAssignment
from app.access.repository import AccessRepository
from app.session.enums import SessionRole

class AccessDenied(Exception):
    ...

class AccessService:
    def __init__(self, repository: AccessRepository):
        self.repository = repository

    async def resolve_committee_assignment(
        self,
        user_id: UUID,
        session_id: int, 
    ) -> CommitteeAssignment:
        assignment = await self.repository.get_committee_assignment(user_id, session_id)
        
        if assignment is None: 
            raise AccessDenied("User has no committee assignment")

        if assignment.role == SessionRole.DELEGATE and assignment.delegation_id is None:
            raise AccessDenied("Delegate role has no delegation id")

        return assignment
