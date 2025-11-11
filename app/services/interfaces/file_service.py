from abc import ABC, abstractmethod
from typing import Optional
import uuid
from fastapi import UploadFile
from app.schemas.file import FileResponse, FileUpload, FileListResponse
from app.schemas.task import TaskResponse

class IFileService(ABC):
    
    @abstractmethod
    async def upload_file(
        self, 
        user_id: uuid.UUID, 
        file: UploadFile, 
        upload_data: FileUpload
    ) -> TaskResponse:
        """Загрузка файла и создание задачи обработки"""
        ...
    
    @abstractmethod
    async def get_user_files(self, user_id: uuid.UUID) -> FileListResponse:
        """Получение всех файлов пользователя"""
        ...
    
    @abstractmethod
    async def get_file_by_id(
        self, 
        user_id: uuid.UUID, 
        file_id: uuid.UUID
    ) -> Optional[FileResponse]:
        """Получение файла по ID"""
        ...
    
    @abstractmethod
    async def delete_file(
        self, 
        user_id: uuid.UUID, 
        file_id: uuid.UUID
    ) -> bool:
        """Удаление файла"""
        ...
    
    @abstractmethod
    async def get_file_download_url(
        self, 
        user_id: uuid.UUID, 
        file_id: uuid.UUID
    ) -> Optional[str]:
        """Получение URL для скачивания файла"""
        ...
    
    @abstractmethod
    async def get_storage_usage(self, user_id: uuid.UUID) -> dict:
        """Получение статистики использования хранилища"""
        ...