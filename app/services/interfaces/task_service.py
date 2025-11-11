from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from app.schemas.task import TaskResponse, TaskListResponse

class ITaskService(ABC):
    
    @abstractmethod
    async def get_user_tasks(self, user_id: uuid.UUID) -> TaskListResponse:
        """Получение всех задач пользователя"""
        ...
    
    @abstractmethod
    async def get_task_by_id(
        self, 
        user_id: uuid.UUID, 
        task_id: uuid.UUID
    ) -> Optional[TaskResponse]:
        """Получение задачи по ID"""
        ...
    
    @abstractmethod
    async def get_task_status(
        self, 
        user_id: uuid.UUID, 
        task_id: uuid.UUID
    ) -> Optional[str]:
        """Получение статуса задачи"""
        ...
    
    @abstractmethod
    async def cancel_task(
        self, 
        user_id: uuid.UUID, 
        task_id: uuid.UUID
    ) -> bool:
        """Отмена задачи"""
        ...
    
    @abstractmethod
    async def process_file_conversion(self, task_id: uuid.UUID) -> bool:
        """Обработка конвертации файла (для Celery)"""
        ...
    
    @abstractmethod
    async def update_task_progress(
        self, 
        task_id: uuid.UUID, 
        progress: int
    ) -> bool:
        """Обновление прогресса задачи"""
        ...
    
    @abstractmethod
    async def get_pending_tasks(self) -> List[TaskResponse]:
        """Получение ожидающих задач (для Celery)"""
        ...