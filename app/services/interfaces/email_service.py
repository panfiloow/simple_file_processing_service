from abc import ABC, abstractmethod
from app.schemas.task import TaskResponse

class IEmailService(ABC):
    
    @abstractmethod
    async def send_task_completion_notification(
        self, 
        user_email: str, 
        task: TaskResponse
    ) -> bool:
        """Отправка уведомления о завершении задачи"""
        ...
    
    @abstractmethod
    async def send_task_failed_notification(
        self, 
        user_email: str, 
        task: TaskResponse
    ) -> bool:
        """Отправка уведомления об ошибке задачи"""
        ...
    
    @abstractmethod
    async def send_registration_notification(self, user_email: str) -> bool:
        """Отправка приветственного письма после регистрации"""
        ...
    
    @abstractmethod
    async def process_pending_notifications(self) -> int:
        """Обработка ожидающих уведомлений (для Celery)"""
        ...