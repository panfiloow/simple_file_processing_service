from abc import abstractmethod, ABC
from typing import List, Optional
import uuid
from app.models import Task
from app.repositories.interfaces.base_repository import IBaseRepository

class ITaskRepository(IBaseRepository[Task], ABC):
    """
    Интерфейс репозитория для работы с задачами обработки
    """

    @abstractmethod
    async def get_by_user_id(self, user_id: uuid.UUID) -> List[Task]:
        """Получить все задачи пользователя"""
        ...

    @abstractmethod
    async def get_by_celery_task_id(self, celery_task_id: str) -> Optional[Task]:
        """Найти задачу по ID задачи Celery"""
        ...

    @abstractmethod
    async def get_by_status(self, status: str) -> List[Task]:
        """Получить задачи по статусу"""
        ...

    @abstractmethod
    async def get_user_tasks_by_status(self, user_id: uuid.UUID, status: str) -> List[Task]:
        """Получить задачи пользователя по статусу"""
        ...

    @abstractmethod
    async def get_pending_tasks(self) -> List[Task]:
        """Получить все ожидающие задачи"""
        ...

    @abstractmethod
    async def get_completed_tasks(self) -> List[Task]:
        """Получить все завершенные задачи"""
        ...

    @abstractmethod
    async def get_failed_tasks(self) -> List[Task]:
        """Получить все failed задачи"""
        ...

    @abstractmethod
    async def update_status(
        self, 
        task_id: uuid.UUID, 
        status: str, 
        error_message: Optional[str] = None
    ) -> Optional[Task]:
        """Обновить статус задачи"""
        ...

    @abstractmethod
    async def update_progress(self, task_id: uuid.UUID, progress: int) -> Optional[Task]:
        """Обновить прогресс задачи"""
        ...

    @abstractmethod
    async def mark_as_completed(
        self, 
        task_id: uuid.UUID, 
        result_file_path: Optional[str] = None
    ) -> Optional[Task]:
        """Пометить задачу как завершенную"""
        ...

    @abstractmethod
    async def mark_as_failed(self, task_id: uuid.UUID, error_message: str) -> Optional[Task]:
        """Пометить задачу как failed"""
        ...

    @abstractmethod
    async def get_recent_tasks(self, user_id: uuid.UUID, limit: int = 10) -> List[Task]:
        """Получить последние задачи пользователя"""
        ...

    @abstractmethod
    async def get_tasks_by_operation_type(self, operation_type: str) -> List[Task]:
        """Получить задачи по типу операции"""
        ...

    @abstractmethod
    async def get_user_tasks_by_operation_type(
        self, 
        user_id: uuid.UUID, 
        operation_type: str
    ) -> List[Task]:
        """Получить задачи пользователя по типу операции"""
        ...

    @abstractmethod
    async def get_tasks_requiring_notification(self) -> List[Task]:
        """Получить задачи, требующие отправки уведомления"""
        ...

    @abstractmethod
    async def mark_notification_sent(self, task_id: uuid.UUID) -> Optional[Task]:
        """Пометить что уведомление отправлено"""
        ...

    @abstractmethod
    async def get_old_completed_tasks(self, days_old: int = 30) -> List[Task]:
        """Получить старые завершенные задачи для очистки"""
        ...

    @abstractmethod
    async def get_user_tasks_count(self, user_id: uuid.UUID) -> int:
        """Получить количество задач пользователя"""
        ...

    @abstractmethod
    async def get_tasks_stats(self) -> dict:
        """Получить статистику по задачам"""
        ...