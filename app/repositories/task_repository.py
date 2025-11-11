from typing import List, Optional, Dict
import uuid
from datetime import datetime, timedelta
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces.task_repository import ITaskRepository
from app.repositories.base_repository import BaseRepository
from app.models import Task

class TaskRepository(BaseRepository[Task], ITaskRepository):
    """
    Репозиторий для работы с задачами обработки
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, Task)

    async def get_by_user_id(self, user_id: uuid.UUID) -> List[Task]:
        result = await self.db.execute(
            select(Task).where(Task.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_celery_task_id(self, celery_task_id: str) -> Optional[Task]:
        result = await self.db.execute(
            select(Task).where(Task.celery_task_id == celery_task_id)
        )
        return result.scalar_one_or_none()

    async def get_by_status(self, status: str) -> List[Task]:
        result = await self.db.execute(
            select(Task).where(Task.status == status)
        )
        return result.scalars().all()

    async def get_user_tasks_by_status(self, user_id: uuid.UUID, status: str) -> List[Task]:
        result = await self.db.execute(
            select(Task).where(
                and_(
                    Task.user_id == user_id,
                    Task.status == status
                )
            )
        )
        return result.scalars().all()

    async def get_pending_tasks(self) -> List[Task]:
        result = await self.db.execute(
            select(Task).where(Task.status == 'pending')
        )
        return result.scalars().all()

    async def get_completed_tasks(self) -> List[Task]:
        result = await self.db.execute(
            select(Task).where(Task.status == 'completed')
        )
        return result.scalars().all()

    async def get_failed_tasks(self) -> List[Task]:
        result = await self.db.execute(
            select(Task).where(Task.status == 'failed')
        )
        return result.scalars().all()

    async def update_status(
        self, 
        task_id: uuid.UUID, 
        status: str, 
        error_message: Optional[str] = None
    ) -> Optional[Task]:
        update_data = {"status": status}
        
        if status == 'processing':
            update_data["started_at"] = datetime.utcnow()
        elif status in ['completed', 'failed']:
            update_data["completed_at"] = datetime.utcnow()
        
        if error_message:
            update_data["error_message"] = error_message
            
        return await self.update(task_id, update_data)

    async def update_progress(self, task_id: uuid.UUID, progress: int) -> Optional[Task]:
        return await self.update(task_id, {"progress": progress})

    async def mark_as_completed(
        self, 
        task_id: uuid.UUID, 
        result_file_path: Optional[str] = None
    ) -> Optional[Task]:
        update_data = {
            "status": "completed",
            "completed_at": datetime.utcnow(),
            "progress": 100
        }
        if result_file_path:
            update_data["result_file_path"] = result_file_path
            
        return await self.update(task_id, update_data)

    async def mark_as_failed(self, task_id: uuid.UUID, error_message: str) -> Optional[Task]:
        return await self.update(task_id, {
            "status": "failed",
            "completed_at": datetime.utcnow(),
            "error_message": error_message
        })

    async def get_recent_tasks(self, user_id: uuid.UUID, limit: int = 10) -> List[Task]:
        result = await self.db.execute(
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_tasks_by_operation_type(self, operation_type: str) -> List[Task]:
        result = await self.db.execute(
            select(Task).where(Task.operation_type == operation_type)
        )
        return result.scalars().all()

    async def get_user_tasks_by_operation_type(
        self, 
        user_id: uuid.UUID, 
        operation_type: str
    ) -> List[Task]:
        result = await self.db.execute(
            select(Task).where(
                and_(
                    Task.user_id == user_id,
                    Task.operation_type == operation_type
                )
            )
        )
        return result.scalars().all()

    async def get_tasks_requiring_notification(self) -> List[Task]:
        result = await self.db.execute(
            select(Task).where(
                and_(
                    Task.status.in_(['completed', 'failed']),
                    not Task.notification_sent
                )
            )
        )
        return result.scalars().all()

    async def mark_notification_sent(self, task_id: uuid.UUID) -> Optional[Task]:
        return await self.update(task_id, {"notification_sent": True})

    async def get_old_completed_tasks(self, days_old: int = 30) -> List[Task]:
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        result = await self.db.execute(
            select(Task).where(
                and_(
                    Task.status == 'completed',
                    Task.completed_at < cutoff_date
                )
            )
        )
        return result.scalars().all()

    async def get_user_tasks_count(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(Task.id)).where(Task.user_id == user_id)
        )
        return result.scalar_one() or 0

    async def get_tasks_stats(self) -> Dict[str, int]:
        result = await self.db.execute(
            select(
                Task.status,
                func.count(Task.id).label('count')
            ).group_by(Task.status)
        )
        
        stats = {row.status: row.count for row in result.all()}
        
        total_result = await self.db.execute(select(func.count(Task.id)))
        stats['total'] = total_result.scalar_one() or 0
        
        return stats