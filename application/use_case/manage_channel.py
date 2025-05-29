from domain.entities.channel import Channels
from domain.repositories.channel_repository import ChannelRepository

async def create_channel(chanel_data: Channels, repository: ChannelRepository) -> Channels:
    return await repository.create_channel(chanel_data)

async def get_channel(channel_id: int, repository: ChannelRepository) -> Channels:
    return await repository.get_channel(channel_id)

async def get_all_channels(repository: ChannelRepository) -> list[Channels]:
    return await repository.get_all_channel()

async def update_channel(channel_id: int, chanel_data: Channels, repository: ChannelRepository) -> Channels:
    return await repository.update_channel(channel_id, chanel_data)

async def delete_channel(channel_id: int, repository: ChannelRepository) -> None:
    await repository.delete_channel(channel_id)