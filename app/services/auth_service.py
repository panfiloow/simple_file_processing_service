from datetime import datetime, timedelta, timezone
import secrets
from typing import Optional
from app.services.interfaces import IAuthService
from app.repositories.interfaces.user_repository import IUserRepository
from app.repositories.interfaces.token_repository import ITokenRepository
import uuid
from app.core.exceptions import InvalidTokenException, UserAlreadyExistsException, InvalidCredentialsException, InactiveUserException
from app.models import User
from app.models import RefreshToken
from app.core.security import get_password_hash, verify_password, generate_tokens, verify_token
from app.schemas.user import UserResponse, UserLogin, UserCreate
from app.schemas.token import RefreshTokenRequest, Token, TokenResponse
from app.core.config import settings


class AuthService(IAuthService):

    def __init__(
        self,
        user_repository: IUserRepository,
        token_repository:ITokenRepository          
    ):
        self.user_repo = user_repository
        self.token_repo = token_repository
        
    
    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """ 
        Регистрирует нового пользователя
        """
        if await self.user_repo.user_exists(user_data.email):
            raise UserAlreadyExistsException()
        
        user = User(
            email = user_data.email,
            hashed_password = get_password_hash(user_data.password)
        )
        
        created_user = await self.user_repo.create(user)
        return UserResponse.model_validate(created_user)
    
    async def authenticate_user(self, login_data: UserLogin) -> Token:
        """ 
        Аутентификация пользователя и возвращение jwt токенов
        """
        user = await self.user_repo.get_by_email(login_data.email)
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise InvalidCredentialsException()
        
        if not user.is_active:
            raise InactiveUserException()
        
        await self.user_repo.update_last_login(user.id)

        tokens = generate_tokens(str(user.id), user.email)
        refresh_token_value = await self._create_refresh_token_in_db(user.id)
        tokens["refresh_token"] = refresh_token_value
        return Token(**tokens)

    async def refresh_token(self, refresh_request: RefreshTokenRequest) -> TokenResponse:
        hashed_refresh_token = get_password_hash(refresh_request.refresh_token)
        token_record = await self.token_repo.get_by_refresh_token(hashed_refresh_token)

        if (not token_record or 
            not token_record.is_active or 
            token_record.expires_at < datetime.now(timezone.utc)):  
            raise InvalidTokenException()
        
        user = await self.user_repo.get_by_id(token_record.user_id)
        if not user or not user.is_active:
            raise InvalidTokenException()
        
        access_token = generate_tokens(str(user.id), user.email)["access_token"]
        return TokenResponse(access_token=access_token, token_type="bearer")

    async def logout_user(self, user_id: uuid.UUID, refresh_token: str) -> bool:
        """Выход из системы путем отзыва refresh token"""
        hashed_refresh_token = get_password_hash(refresh_token)
        token_record = await self.token_repo.get_by_refresh_token(hashed_refresh_token)
        
        if token_record and token_record.user_id == user_id:
            return await self.token_repo.revoke_by_id(token_record.id)
        return False
    
    async def verify_token(self, token: str) -> Optional[dict]:
        """Проверка jwt токена"""
        return verify_token(token)
    
    async def get_current_user(self, token: str) -> Optional[UserResponse]:
        """Получить текущего пользователя из токена"""
        payload = await self.verify_token(token)
        if not payload:
            return None
            
        user_email = payload.get("sub")
        if not user_email:
            return None
            
        user = await self.user_repo.get_by_email(user_email)
        if user and user.is_active:
            return UserResponse.model_validate(user)
        return None
    
    async def logout_all_sessions(self, user_id: uuid.UUID) -> bool:
        """Выход со всех устройств"""
        return await self.token_repo.revoke_all_user_tokens(user_id)

    async def _create_refresh_token_in_db(self, user_id : uuid.UUID) -> str:
        """ 
        Создает и сохраняет refresh_token в базу данных
        """
        refresh_token_value = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        token = RefreshToken(
            user_id=user_id,
            refresh_token=get_password_hash(refresh_token_value), 
            expires_at=expires_at,
            device_info="web",
            ip_address="127.0.0.1"  #TODO: In real app, get from request
        )

        await self.token_repo.create(token)
        return refresh_token_value
