from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from infrastructure.database.db_config import get_async_session
from infrastructure.interfaces.controller import 

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/plans-by-status")
async def get_plan_status_count(db: AsyncSession = Depends(get_async_session)):
    stmt = select(Plan_action.state, func.count()).group_by(Plan_action.state)
    result = await db.execute(stmt)
    return {state: count for state, count in result.all()}