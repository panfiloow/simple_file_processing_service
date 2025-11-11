from pydantic import BaseModel
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