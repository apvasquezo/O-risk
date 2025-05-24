from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.channel_repository import ChannelRepository
from application.use_case.manage_channel import (
    create_channel,
    get_channel,
    get_all_channels,
    update_channel,
    delete_channel
)

router = APIRouter()

class ChannelCreate(BaseModel):
    description: str

class ChannelResponse(BaseModel):
    id_channel: int
    description: str

@router.post("/channels/", response_model=ChannelResponse)
async def create_channel_endpoint(channel: ChannelCreate, db: AsyncSession = Depends(get_db)):
    repository = ChannelRepository(db)
    created_channel = await create_channel(channel, repository)
    return ChannelResponse(
        id_channel=created_channel.id_channel, 
        description=created_channel.description
    )

@router.get("/channels/{channel_id}", response_model=ChannelResponse)
async def read_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    repository = ChannelRepository(db)
    channel = await get_channel(channel_id,repository)
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return ChannelResponse(
        id_channel=channel.id_channel, 
        description=channel.description
    )

@router.get("/channels/", response_model=List[ChannelResponse])
async def read_channels(db: AsyncSession = Depends(get_db)):
    repository = ChannelRepository(db)
    channels = await get_all_channels(repository)
    return [ChannelResponse(
        id_channel=c.id_channel, 
        description=c.description
    ) for c in channels]

@router.put("/channels/{channel_id}", response_model=ChannelResponse)
async def update_channel(channel_id: int, channel: ChannelCreate, db: AsyncSession = Depends(get_db)):
    repository = ChannelRepository(db)
    updated_channel = await update_channel(channel_id, channel, repository)
    if updated_channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return ChannelResponse(
        id_channel=updated_channel.id_channel, 
        description=updated_channel.description
    )

@router.delete("/channels/{channel_id}", response_model=dict)
async def delete_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    repository = ChannelRepository(db)
    await delete_channel(channel_id, repository)
    return {"detail": "Channel deleted"}