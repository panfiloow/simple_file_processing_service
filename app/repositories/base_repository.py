from typing import List, Optional, Type
import uuid
from sqlalchemy import select, update as sql_update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces.base_repository import T, IBaseRepository


class BaseRepository(IBaseRepository[T]):
    """
    Репозиторий с базовыми CRUD операциями
    """

    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    async def get_by_id(self, id: uuid.UUID) -> Optional[T]:
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, entity: T) -> T:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
    
    async def update(self, id: uuid.UUID, update_data: dict) -> Optional[T]:
        stmt = (
            sql_update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
            .returning(self.model)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        updated_entity = result.scalar_one_or_none()
        if updated_entity:
            await self.db.refresh(updated_entity)
        return updated_entity
    
    async def delete(self, id: uuid.UUID) -> bool:
        entity = await self.get_by_id(id)
        if entity:
            await self.db.delete(entity)
            await self.db.commit()
            return True
        return False
    
    async def get_all(self) -> List[T]:
        result = await self.db.execute(select(self.model))
        return result.scalars().all()
    
    async def get_many_by_ids(self, ids: List[uuid.UUID]) -> List[T]:
        if not ids:
            return []
        result = await self.db.execute(
            select(self.model).where(self.model.id.in_(ids))
        )
        return result.scalars().all()
    
    async def count(self) -> int:
        result = await self.db.execute(select(func.count(self.model.id)))
        return result.scalar_one()
    
    async def exists(self, id: uuid.UUID) -> bool:  
        result = await self.db.execute(
            select(self.model.id).where(self.model.id == id)
        )
        return result.scalar_one_or_none() is not None