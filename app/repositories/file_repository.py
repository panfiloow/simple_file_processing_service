from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces.file_repository import IFileRepository
from app.repositories.base_repository import BaseRepository
from app.models import File

class FileRepository(BaseRepository[File], IFileRepository):
    """
    Репозиторий для работы с файлами
    """
    def __init__(self, db : AsyncSession):
        super().__init__(db, File)

    async def get_by_user_id(self, user_id: uuid.UUID) -> List[File]:
        result = await self.db.execute(
            select(File).where(File.user_id == user_id)
        )
        return result.scalars().all()
    
    async def get_by_filename(self, user_id: uuid.UUID, filename: str) -> Optional[File]:
       result = await self.db.execute(
           select(File).where(
               and_(
                   File.user_id == user_id,
                   File.original_filename == filename
               )
           )
       )
       return result.scalar_one_or_none()
           
    async def get_recent_files(self, user_id: uuid.UUID, limit: int = 10) -> List[File]:
        result = await self.db.execute(
            select(File)
            .where(File.user_id == user_id)
            .order_by(File.uploaded_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_large_files(self, user_id: uuid.UUID, size_threshold: int) -> List[File]:
        result = await self.db.execute(
            select(File).where(
                and_(
                    File.user_id == user_id,
                    File.file_size > size_threshold
                )
            )
        )
        return result.scalars().all()
    
    async def get_files_by_type(self, user_id: uuid.UUID, mime_type: str) -> List[File]:
        result = await self.db.execute(
            select(File).where(
                and_(
                    File.user_id == user_id,
                    File.mime_type == mime_type
                )
            )
        )
        return result.scalars().all()
    
    async def get_files_by_extension(self, user_id: uuid.UUID, extension: str) -> List[File]:
        result = await self.db.execute(
            select(File).where(
                and_(
                    File.user_id == user_id,
                    File.extension == extension
                )
            )
        )
        return result.scalars().all()
    
    async def update_file_status(self, file_id: uuid.UUID, is_processed: bool) -> Optional[File]:
        return await self.update(file_id, {"is_processed": is_processed})
  
    async def update_file_path(self, file_id: uuid.UUID, new_path: str) -> Optional[File]:
        return await self.update(file_id, {"file_path": new_path})
    
    async def get_user_files_count(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(File.id)).where(File.user_id == user_id)
        )
        return result.scalar_one() or 0
    
    async def get_total_storage_used(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.sum(File.file_size), 0)).where(File.user_id == user_id)
        )
        return result.scalar_one() or 0
    
    async def get_files_uploaded_in_period(
        self, 
        user_id: uuid.UUID, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[File]:
        result = await self.db.execute(
            select(File).where(
                and_(
                    File.user_id == user_id,
                    File.uploaded_at >= start_date,
                    File.uploaded_at <= end_date
                )
            )
        )
        return result.scalars().all()
    
    async def file_exists_for_user(self, user_id: uuid.UUID, filename: str) -> bool:
        result = await self.db.execute(
            select(File.id).where(
                and_(
                    File.user_id == user_id,
                    File.original_filename == filename
                )
            )
        )
        return result.scalar_one_or_none() is not None
