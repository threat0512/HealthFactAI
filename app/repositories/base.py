"""
Base repository pattern for database operations.
Supports both PostgreSQL and SQLite through the database manager.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Any
from app.core.database import db_manager

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """Base repository with common database operations."""
    
    def __init__(self):
        self.db = db_manager
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an entity."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an entity."""
        pass
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Any]:
        """Execute a SELECT query and return results."""
        return self.db.execute_query(query, params)
    
    def execute_command(self, command: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE command and return affected rows."""
        return self.db.execute_command(command, params)
    
    def execute_command_get_id(self, command: str, params: tuple = ()) -> int:
        """Execute command and return the last inserted row ID."""
        return self.db.execute_command_get_id(command, params)
