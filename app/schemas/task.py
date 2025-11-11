from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
import uuid
from datetime import datetime
from enum import Enum

from app.schemas.file import FileOperationType

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskBase(BaseModel):
    operation_type: FileOperationType
    parameters: Optional[Dict[str, Any]] = None

class TaskCreate(TaskBase):
    user_id: uuid.UUID
    file_id: uuid.UUID
    celery_task_id: str

class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    progress: Optional[int] = None
    result_file_path: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notification_sent: Optional[bool] = None

class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    user_id: uuid.UUID
    file_id: uuid.UUID
    celery_task_id: str
    status: TaskStatus
    progress: int
    result_file_path: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    notification_sent: bool

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total_count: int

class TaskProgressUpdate(BaseModel):
    progress: int
    status: Optional[TaskStatus] = None