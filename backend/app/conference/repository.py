from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.conference import schemas
from app.core.database import RepositoryError


async def create_conference(
    session: AsyncSession, user_id: UUID, payload: schemas.ConferenceCreate
) -> int:
    query = text("""
        INSERT INTO public.conferences
            (name, owner_id, location, color, start_date, end_date)
        VALUES (
            name = :name,
            owner_id = :owner_id,
            location = :location,
            color = :color,
            start_date = :start_date,
            end_date = :end_date
        )
        RETURNING id
    """)

    try:
        result = await session.execute(
            query,
            {
                "name": payload.name,
                "owner_id": user_id,
                "location": payload.location,
                "color": payload.color,
                "start_date": payload.start_date,
                "end_date": payload.end_date,
            },
        )
        row = result.mappings().one()
        return row.get("id", -1)

    except SQLAlchemyError:
        raise RepositoryError("Could not create conference")
