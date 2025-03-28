from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from .base import CRUDBase


class CharityProjectCRUD(CRUDBase):
    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[dict[str, str]]:
        return await session.execute(
            select(
                CharityProject.name,
                CharityProject.create_date,
                CharityProject.close_date,
                CharityProject.description
            ).where(
                CharityProject.fully_invested.is_(True)
            )
        ).all()


charity_project_crud = CharityProjectCRUD(CharityProject)
