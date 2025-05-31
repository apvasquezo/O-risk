from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from domain.entities.channel import Channels as ChanelEntity
from infrastructure.orm.models import Channel as ORMChannel

class ChannelRepository:
    def __init__(self, session: AsyncSession):
        self.session=session
    
    async def create_channel(self, channel:ChanelEntity) ->ChanelEntity:
        stmt= insert(ORMChannel).values(description=channel.description
            ).returning(
                ORMChannel.id_channel,
                ORMChannel.description
            )
        try:
            result= await self.session.execute(stmt)
            await self.session.commit()
            row= result.fetchone()
            if row:
                return ChanelEntity(
                    id_channel=row.id_channel,
                    description=row.description
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Channel already exists ") from e
    
    async def get_channel(self, channel_id:int) -> Optional[ChanelEntity]:
        stmt = select(ORMChannel).where(ORMChannel.id_channel == channel_id)
        result = await self.session.execute(stmt)
        orm_channel= result.scalar_one_or_none()
        if orm_channel:
            return ChanelEntity(
                id_channel=orm_channel.id_channel,
                description=orm_channel.description
            )
        return None
    
    async def get_all_channel(self) -> List[ChanelEntity]:
        stmt = select(ORMChannel)
        result = await self.session.execute(stmt)
        orm_channels = result.scalars().all()
        return [ChanelEntity(
            id_channel=c.id_channel, 
            description=c.description
            ) for c in orm_channels]
        
    async def update_channel(self, channel_id:int, channel:ChanelEntity) -> Optional [ChanelEntity]:
        stmt = update(ORMChannel).where(ORMChannel.id_channel == channel_id).values(
            description=channel.description
            ).returning(
                ORMChannel.id_channel,
                ORMChannel.description
            )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return ChanelEntity(
                id_channel=row.id_channel,
                description=row.description
                )
        return None
    
    async def delete_channel(self, channel_id:int) -> None:
        stmt = delete(ORMChannel).where(ORMChannel.id_channel == channel_id)
        result= await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount==0:
            raise ValueError(f"Channel with id {channel_id} not found")