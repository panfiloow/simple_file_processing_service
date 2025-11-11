from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

class MessageResponse(BaseModel):
    message: str
    details: Optional[dict] = None

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    code: Optional[str] = None