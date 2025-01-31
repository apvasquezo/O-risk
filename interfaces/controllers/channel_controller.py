from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.channel_repository import ChannelRepository
from domain.entities.channel import Channel

router = APIRouter()

class ChannelCreate(BaseModel):
    description: str

class ChannelResponse(BaseModel):
    id: int
    description: str

@router.post("/channels/", response_model=ChannelResponse)
async def create_channel(channel: ChannelCreate, db: AsyncSession = Depends(get_db)):
    repository = ChannelRepository(db)
    created_channel = await repository.create_channel(Channel(description=channel.description))
    return ChannelResponse(id=created_channel.id, description=created_channel.description)

@router.get("/channels/{channel_id}", response_model=ChannelResponse)
async def read_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    repository = ChannelRepository(db)
    channel = await repository.get_channel(channel_id)
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return ChannelResponse(id=channel.id, description=channel.description)

@router.get("/channels/", response_model=List[ChannelResponse])
async def read_channels(db: AsyncSession = Depends(get_db)):
    repository = ChannelRepository(db)
    channels = await repository.get_all_channels()
    return [ChannelResponse(id=c.id, description=c.description) for c in channels]

@router.put("/channels/{channel_id}", response_model=ChannelResponse)
async def update_channel(channel_id: int, channel: ChannelCreate, db: AsyncSession = Depends(get_db)):
    repository = ChannelRepository(db)
    updated_channel = await repository.update_channel(channel_id, Channel(description=channel.description))
    if updated_channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return ChannelResponse(id=updated_channel.id, description=updated_channel.description)

@router.delete("/channels/{channel_id}", response_model=dict)
async def delete_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    repository = ChannelRepository(db)
    await repository.delete_channel(channel_id)
    return {"detail": "Channel deleted"}