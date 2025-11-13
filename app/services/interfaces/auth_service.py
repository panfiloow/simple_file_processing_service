from abc import ABC, abstractmethod
from typing import Optional
import uuid
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import TokenResponse, RefreshTokenRequest, Token

class IAuthService(ABC):
    
    @abstractmethod
    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """Регистрация нового пользователя"""
        ...
    
    @abstractmethod
    async def authenticate_user(self, login_data: UserLogin) -> Token:
        """Аутентификация пользователя"""
        ...
    
    @abstractmethod
    async def refresh_token(self, refresh_request: RefreshTokenRequest) -> TokenResponse:
        """Обновление access token"""
        ...
    
    @abstractmethod
    async def logout_user(self, user_id: uuid.UUID, refresh_token: str) -> bool:
        """Выход пользователя (отзыв токена)"""
        ...
    
    @abstractmethod
    async def logout_all_sessions(self, user_id: uuid.UUID) -> bool:
        """Выход со всех устройств"""
        ...
    
    @abstractmethod
    async def verify_token(self, token: str) -> Optional[dict]:
        """Верификация JWT токена"""
        ...
    
    @abstractmethod
    async def get_current_user(self, token: str) -> Optional[UserResponse]:
        """Получение текущего пользователя по токену"""
        ...