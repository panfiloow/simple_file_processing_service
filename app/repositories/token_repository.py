from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces.token_repository import ITokenRepository
from app.repositories.base_repository import BaseRepository
from app.models import RefreshToken

class TokenRepository(BaseRepository[RefreshToken], ITokenRepository):
    """
    Репозиторий для работы с токенами jwt
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, RefreshToken)

    async def get_by_refresh_token(self, refresh_token) -> Optional[RefreshToken]:
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.refresh_token == refresh_token)
        )
        return result.scalar_one_or_none()
    
    async def get_active_by_user_id(self, user_id: uuid.UUID) -> List[RefreshToken]:
        result = await self.db.execute(
            select(RefreshToken).where(
                and_(
                    RefreshToken.user_id == user_id,
                    RefreshToken.is_active,
                    RefreshToken.expires_at > datetime.now()
                )
            )
        )
        return result.scalars().all()
    
    async def revoke_by_id(self, token_id: uuid.UUID) -> bool:
        token = await self.get_by_id(token_id)
        if token:
            return await self.update(token_id, {"is_active": False}) is not None
        return False
    
    async def revoke_all_user_tokens(self, user_id: uuid.UUID) -> bool:
        tokens = await self.get_active_by_user_id(user_id)
        if tokens:
            for token in tokens:
                await self.update(token.id, {"is_active": False})
            return True
        return False
    
    async def token_exists(self, refresh_token) -> bool:
        result = await self.db.execute(
            select(RefreshToken.id).where(
                and_(
                    RefreshToken.refresh_token == refresh_token,
                    RefreshToken.is_active
                )
            )
        )
        return result.scalar_one_or_none() is not None
    
    async def is_token_active(self, token_id: uuid.UUID) -> bool:
        token = await self.get_by_id(token_id)
        return bool(token and token.is_active and token.expires_at > datetime.now())
    
    async def cleanup_expired_tokens(self) -> int:
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.expires_at <= datetime.now())
        )
        expired_tokens = result.scalars().all()
        
        count = 0
        for token in expired_tokens:
            await self.db.delete(token)
            count += 1
        
        if count > 0:
            await self.db.commit()
        
        return count
    
    async def get_all_by_user_id(self, user_id: uuid.UUID) -> List[RefreshToken]:
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.user_id == user_id)
        )

        return result.scalars().all()
    
    async def get_active_tokens_count(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(RefreshToken.id)).where(
                and_(
                    RefreshToken.user_id == user_id,
                    RefreshToken.is_active,
                    RefreshToken.expires_at > datetime.utcnow()
                )
            )
        )
        return result.scalar_one() or 0
    
    async def revoke_old_tokens(self, user_id: uuid.UUID, keep_last_n: int = 5) -> int:
        active_tokens = await self.get_active_by_user_id(user_id)
        
        if len(active_tokens) <= keep_last_n:
            return 0
        
        sorted_tokens = sorted(active_tokens, key=lambda x: x.created_at, reverse=True)
        
        tokens_to_revoke = sorted_tokens[keep_last_n:]
        
        for token in tokens_to_revoke:
            await self.update(token.id, {"is_active": False})
        
        return len(tokens_to_revoke)
    
    async def get_by_device_info(self, user_id: uuid.UUID, device_info: str) -> Optional[RefreshToken]:
        result = await self.db.execute(
            select(RefreshToken).where(
                and_(
                    RefreshToken.user_id == user_id,
                    RefreshToken.device_info == device_info,
                    RefreshToken.is_active
                )
            )
        )
        return result.scalar_one_or_none()        
