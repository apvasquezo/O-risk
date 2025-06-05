from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.channel_repository import ChannelRepository
from application.use_case.manage_channel import (
    create_channel,
    get_channel,
    get_all_channels,
    update_channel,
    delete_channel
)
from utils.auth import role_required

router = APIRouter(
    prefix="/channels",
    tags=["Canales"],
    #dependencies=[Depends(role_required("super"))] 
)

class ChannelCreate(BaseModel):
    description: str

class ChannelResponse(BaseModel):
    id_channel: int
    description: str

@router.post("/", response_model=ChannelResponse, status_code=201)
async def create_channel_endpoint(channel: ChannelCreate, db: AsyncSession = Depends(get_async_session), _: None = Depends(role_required("super"))):
    repository = ChannelRepository(db)
    created = await create_channel(channel, repository)
    return ChannelResponse(**created.model_dump())

@router.get("/{channel_id}", response_model=ChannelResponse)
async def read_channel(channel_id: int, db: AsyncSession = Depends(get_async_session), _: None = Depends(role_required("super"))):
    repository = ChannelRepository(db)
    channel = await get_channel(channel_id, repository)
    if channel is None:
        raise HTTPException(status_code=404, detail="Canal no encontrado")
    return ChannelResponse(**channel.model_dump())

@router.get("/", response_model=List[ChannelResponse])
async def read_channels(db: AsyncSession = Depends(get_async_session)):
    repository = ChannelRepository(db)
    channels = await get_all_channels(repository)
    return [ChannelResponse(**c.model_dump()) for c in channels]

@router.put("/{channel_id}", response_model=ChannelResponse)
async def update_channel_endpoint(channel_id: int, channel: ChannelCreate, db: AsyncSession = Depends(get_async_session), _: None = Depends(role_required("super"))):
    repository = ChannelRepository(db)
    updated = await update_channel(channel_id, channel, repository)
    if updated is None:
        raise HTTPException(status_code=404, detail="Canal no encontrado")
    return ChannelResponse(**updated.model_dump())

@router.delete("/{channel_id}", response_model=dict)
async def delete_channel_endpoint(channel_id: int, db: AsyncSession = Depends(get_async_session), _: None = Depends(role_required("super"))):
    repository = ChannelRepository(db)
    await delete_channel(channel_id, repository)
    return {"detail": "Canal eliminado"}

