from typing import List, Optional
from domain.entities.channel import Channel
from domain.repositories.channel_repository import ChannelRepository

async def create_channel(description: str, repository: ChannelRepository) -> Channel:
    channel = Channel(description=description)
    return await repository.create_channel(channel)

async def get_channel(channel_id: int, repository: ChannelRepository) -> Optional[Channel]:
    return await repository.get_channel(channel_id)

async def get_all_channels(repository: ChannelRepository) -> List[Channel]:
    return await repository.get_all_channels()

async def update_channel(channel_id: int, description: str, repository: ChannelRepository) -> Optional[Channel]:
    channel = Channel(id=channel_id, description=description)
    return await repository.update_channel(channel)

async def delete_channel(channel_id: int, repository: ChannelRepository) -> None:
    await repository.delete_channel(channel_id)