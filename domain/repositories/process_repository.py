from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Process as ORMProcess
from domain.entities.Process import Process as ProcessEntity

class ProcessRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_process(self, process: ProcessEntity) -> ProcessEntity:
        stmt = insert(ORMProcess).values(
            macroprocess_id=process.macroprocess_id,
            description=process.description,
            personal_id=process.personal_id,
        ).returning(
            ORMProcess.id_process, 
            ORMProcess.macroprocess_id, 
            ORMProcess.description,
            ORMProcess.personal_id
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return ProcessEntity(
                    id_process=row.id_process, 
                    macroprocess_id=row.macroprocess_id, 
                    description=row.description,
                    personal_id=row.personal_id,
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Process creation failed") from e

    async def get_process(self, process_id: int) -> Optional[ProcessEntity]:
        stmt = select(ORMProcess).where(ORMProcess.id_process == process_id)
        result = await self.session.execute(stmt)
        orm_process = result.scalar_one_or_none()
        if orm_process:
            return ProcessEntity(
                id_process=orm_process.id_process, 
                macroprocess_id=orm_process.macroprocess_id, 
                description=orm_process.description,
                personal_id=orm_process.personal_id
            )
        return None

    async def get_all_processes(self) -> List[ProcessEntity]:
        stmt = select(ORMProcess)
        result = await self.session.execute(stmt)
        orm_processes = result.scalars().all()
        return [
            ProcessEntity(
                id_process=p.id_process, 
                macroprocess_id=p.macroprocess_id, 
                description=p.description,
                personal_id=p.personal_id
            ) for p in orm_processes
        ]

    async def update_process(self, process_id: int, process: ProcessEntity) -> Optional[ProcessEntity]:
        stmt = update(ORMProcess).where(ORMProcess.id_process == process_id).values(
            macroprocess_id=process.macroprocess_id,
            description=process.description,
            personal_id=process.personal_id,
        ).returning(
            ORMProcess.id_process, 
            ORMProcess.macroprocess_id, 
            ORMProcess.description,
            ORMProcess.personal_id
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return ProcessEntity(
                id_process=row.id_process, 
                macroprocess_id=row.macroprocess_id, 
                description=row.description,
                personal=row.personal_id
            )
        return None

    async def delete_process(self, process_id: int) -> None:
        stmt = delete(ORMProcess).where(ORMProcess.id_process == process_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Process with id {process_id} not found")