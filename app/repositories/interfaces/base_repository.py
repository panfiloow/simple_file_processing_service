from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar, Generic
import uuid

T = TypeVar('T') 

class IBaseRepository(ABC, Generic[T]):

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Optional[T]: ...
    
    @abstractmethod
    async def create(self, entity: T) -> T: ...
    
    @abstractmethod
    async def update(self, id: uuid.UUID, update_data: dict) -> Optional[T]: ...
    
    @abstractmethod
    async def delete(self, id: uuid.UUID) -> bool: ...
    
    @abstractmethod
    async def get_all(self) -> List[T]: ...

    @abstractmethod
    async def exists(self, id: uuid.UUID) -> bool: ... 