from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Macroprocess as ORMMacroprocess
from domain.entities.Macroprocess import Macroprocess

class MacroprocessRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_macroprocess(self, macroprocess: Macroprocess) -> Macroprocess:
        stmt = insert(ORMMacroprocess).values(
            description=macroprocess.description
        ).returning(ORMMacroprocess.id_macro, ORMMacroprocess.description)
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return Macroprocess(id_macro=row.id_macro, description=row.description)
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Macroprocess creation failed") from e

    async def get_macroprocess(self, macroprocess_id: int) -> Optional[Macroprocess]:
        stmt = select(ORMMacroprocess).where(ORMMacroprocess.id_macro == macroprocess_id)
        result = await self.session.execute(stmt)
        orm_macroprocess = result.scalar_one_or_none()
        if orm_macroprocess:
            return Macroprocess(id_macro=orm_macroprocess.id_macro, description=orm_macroprocess.description)
        return None

    async def get_all_macroprocesses(self) -> List[Macroprocess]:
        stmt = select(ORMMacroprocess)
        result = await self.session.execute(stmt)
        orm_macroprocesses = result.scalars().all()
        return [Macroprocess(id_macro=m.id_macro, description=m.description) for m in orm_macroprocesses]

    async def update_macroprocess(self, macroprocess_id: int, macroprocess: Macroprocess) -> Optional[Macroprocess]:
        stmt = update(ORMMacroprocess).where(ORMMacroprocess.id_macro == macroprocess_id).values(
            description=macroprocess.description
        ).returning(ORMMacroprocess.id_macro, ORMMacroprocess.description)
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return Macroprocess(id_macro=row.id_macro, description=row.description)
        return None

    async def delete_macroprocess(self, macroprocess_id: int) -> None:
        stmt = delete(ORMMacroprocess).where(ORMMacroprocess.id == macroprocess_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Macroprocess with id {macroprocess_id} not found")