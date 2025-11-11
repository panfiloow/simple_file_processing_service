from abc import abstractmethod, ABC
from datetime import datetime
from typing import List, Optional
import uuid
from app.models import File
from app.repositories.interfaces.base_repository import IBaseRepository

class IFileRepository(IBaseRepository[File], ABC):

    @abstractmethod
    async def get_by_user_id(self, user_id: uuid.UUID) -> List[File]:
        """Получить все файлы пользователя"""
        ...

    @abstractmethod
    async def get_by_filename(self, user_id: uuid.UUID, filename: str) -> Optional[File]:
        """Найти файл по имени у конкретного пользователя"""
        ...

    @abstractmethod
    async def get_recent_files(self, user_id: uuid.UUID, limit: int = 10) -> List[File]:
        """Получить последние загруженные файлы пользователя"""
        ...

    @abstractmethod
    async def get_large_files(self, user_id: uuid.UUID, size_threshold: int) -> List[File]:
        """Получить файлы пользователя больше указанного размера"""
        ...

    @abstractmethod
    async def get_files_by_type(self, user_id: uuid.UUID, mime_type: str) -> List[File]:
        """Получить файлы пользователя по MIME-типу"""
        ...

    @abstractmethod
    async def get_files_by_extension(self, user_id: uuid.UUID, extension: str) -> List[File]:
        """Получить файлы пользователя по расширению"""
        ...

    @abstractmethod
    async def update_file_status(self, file_id: uuid.UUID, is_processed: bool) -> Optional[File]:
        """Обновить статус обработки файла"""
        ...

    @abstractmethod
    async def update_file_path(self, file_id: uuid.UUID, new_path: str) -> Optional[File]:
        """Обновить путь к файлу (после обработки)"""
        ...

    @abstractmethod
    async def get_user_files_count(self, user_id: uuid.UUID) -> int:
        """Получить количество файлов пользователя"""
        ...

    @abstractmethod
    async def get_total_storage_used(self, user_id: uuid.UUID) -> int:
        """Получить общий объем хранилища, используемый пользователем (в байтах)"""
        ...

    @abstractmethod
    async def get_files_uploaded_in_period(
        self, 
        user_id: uuid.UUID, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[File]:
        """Получить файлы, загруженные в указанный период"""
        ...

    @abstractmethod
    async def file_exists_for_user(self, user_id: uuid.UUID, filename: str) -> bool:
        """Проверить существование файла с таким именем у пользователя"""
        ...
