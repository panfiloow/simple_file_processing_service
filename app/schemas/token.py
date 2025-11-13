from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid
from datetime import datetime

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str  # email
    user_id: uuid.UUID
    exp: datetime

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenInfo(BaseModel):
    device_info: Optional[str] = None
    ip_address: Optional[str] = None

# Схемы для работы с RefreshToken в базе данных
class RefreshTokenBase(BaseModel):
    device_info: str
    ip_address: str

class RefreshTokenCreate(RefreshTokenBase):
    user_id: uuid.UUID
    expires_at: datetime

class RefreshTokenCreateWithValue(RefreshTokenCreate):
    refresh_token: str  # Хэшированное значение

class RefreshTokenUpdate(BaseModel):
    is_active: Optional[bool] = None
    device_info: Optional[str] = None
    ip_address: Optional[str] = None

class RefreshTokenResponse(RefreshTokenBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    user_id: uuid.UUID
    is_active: bool
    created_at: datetime
    expires_at: datetime

# Для ответа со списком токенов пользователя
class UserTokensResponse(BaseModel):
    tokens: list[RefreshTokenResponse]

# Для репозитория - поиск по токену
class RefreshTokenSearch(BaseModel):
    refresh_token: str