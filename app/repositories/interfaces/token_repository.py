from abc import abstractmethod, ABC
from typing import List, Optional
import uuid
from app.repositories.interfaces.base_repository import IBaseRepository
from app.models import RefreshToken

class ITokenRepository(IBaseRepository[RefreshToken], ABC):
    """ 
    Интерфейс репозитория для работы с refresh токенами
    """

    @abstractmethod
    async def get_by_refresh_token(self, refresh_token: str) -> Optional[RefreshToken]:
        """Найти токен по значению refresh токена"""
        ...

    @abstractmethod
    async def get_active_by_user_id(self, user_id: uuid.UUID) -> List[RefreshToken]:
        """Получить все активные токены пользователя"""
        ...

    @abstractmethod
    async def revoke_by_id(self, token_id: uuid.UUID) -> bool:
        """Отозвать конкретный токен по ID"""
        ...
    
    @abstractmethod
    async def revoke_all_user_tokens(self, user_id: uuid.UUID) -> bool:
        """Отозвать все токены пользователя"""
        ...
    
    @abstractmethod
    async def token_exists(self, refresh_token: str) -> bool:
        """Проверить существование токена по значению"""
        ...
    
    @abstractmethod
    async def is_token_active(self, token_id: uuid.UUID) -> bool:
        """Проверить активен ли токен"""
        ...
    
    @abstractmethod
    async def cleanup_expired_tokens(self) -> int:
        """Очистить просроченные токены (возвращает количество удаленных)"""
        ...
    
    @abstractmethod
    async def get_all_by_user_id(self, user_id: uuid.UUID) -> List[RefreshToken]:
        """Получить все токены пользователя (включая неактивные)"""
        ...
    
    @abstractmethod
    async def get_active_tokens_count(self, user_id: uuid.UUID) -> int:
        """Получить количество активных токенов пользователя"""
        ...
    
    @abstractmethod
    async def revoke_old_tokens(self, user_id: uuid.UUID, keep_last_n: int = 5) -> int:
        """Оставить только N последних активных токенов пользователя"""
        ...

    @abstractmethod
    async def get_by_device_info(self, user_id: uuid.UUID, device_info: str) -> Optional[RefreshToken]:
        """Найти токен по информации об устройстве"""
        ...