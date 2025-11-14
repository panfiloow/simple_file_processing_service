from datetime import timezone
from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.repositories.interfaces.user_repository import IUserRepository
from app.repositories.base_repository import BaseRepository
from app.models import User

class UserRepository(BaseRepository[User], IUserRepository):
    """
    Репозиторий для работы с пользователями
    """
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Получить пользователя по email
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    

    async def get_all_active(self) -> List[User]:
        """
        Получить всех активных пользователей
        """
        result = await self.db.execute(
            select(User).where(User.is_active)
        )
        return result.scalars().all()

    async def user_exists(self, email: str) -> bool:
        """
        Проверить существование пользователя по email
        Более эффективно, чем get_by_email, т.к. загружает только ID
        """
        result = await self.db.execute(
            select(User.id).where(User.email == email)
        )
        return result.scalar_one_or_none() is not None

    async def update_last_login(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Обновить время последнего входа пользователя
        Специфичный метод для User
        """
        return await self.update(user_id, {"last_login_at": datetime.now(timezone.utc)})

    async def deactivate_user(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Деактивировать пользователя
        Специфичный метод для User
        """
        return await self.update(user_id, {"is_active": False})

    async def activate_user(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Активировать пользователя
        Специфичный метод для User
        """
        return await self.update(user_id, {"is_active": True})

    async def get_users_by_creation_date_range(
        self, 
        start_date, 
        end_date
    ) -> List[User]:
        """
        Получить пользователей по диапазону дат регистрации
        Специфичный метод для User
        """
        result = await self.db.execute(
            select(User).where(
                User.created_at >= start_date,
                User.created_at <= end_date
            )
        )
        return result.scalars().all()
    
