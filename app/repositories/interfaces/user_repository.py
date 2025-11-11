from abc import abstractmethod, ABC
from datetime import datetime
from typing import List, Optional
import uuid
from app.models import User
from app.repositories.interfaces.base_repository import IBaseRepository


class IUserRepository(IBaseRepository[User], ABC):
  
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def get_all_active(self) -> List[User]: ...

    @abstractmethod
    async def user_exists(self, email: str) -> bool: ...

    @abstractmethod
    async def update_last_login(self, user_id: uuid.UUID) -> Optional[User]: ...

    @abstractmethod
    async def deactivate_user(self, user_id: uuid.UUID) -> Optional[User]: ...

    @abstractmethod
    async def activate_user(self, user_id: uuid.UUID) -> Optional[User]: ...

    @abstractmethod
    async def get_users_by_creation_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[User]: ...
