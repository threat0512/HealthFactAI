"""
User repository for database operations.
"""
from typing import Optional, List
# PostgreSQL support through database manager
from app.repositories.base import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository[User]):
    """Repository for user-related database operations."""
    
    def create(self, user: User) -> User:
        """Create a new user."""
        command = """
            INSERT INTO users (username, password, email, facts_learned, current_streak, 
                             longest_streak, total_facts_count, last_activity_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            user.username, user.password, user.email, user.facts_learned,
            user.current_streak, user.longest_streak, user.total_facts_count,
            user.last_activity_date
        )
        
        user_id = self.execute_command_get_id(command, params)
        user.id = user_id
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        query = """
            SELECT id, username, password, email, facts_learned, current_streak,
                   longest_streak, total_facts_count, last_activity_date
            FROM users WHERE id = %s
        """
        rows = self.execute_query(query, (user_id,))
        return User.from_db_row(rows[0]) if rows else None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        query = """
            SELECT id, username, password, email, facts_learned, current_streak,
                   longest_streak, total_facts_count, last_activity_date
            FROM users WHERE username = %s
        """
        rows = self.execute_query(query, (username,))
        return User.from_db_row(rows[0]) if rows else None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        query = """
            SELECT id, username, password, email, facts_learned, current_streak,
                   longest_streak, total_facts_count, last_activity_date
            FROM users WHERE email = %s
        """
        rows = self.execute_query(query, (email,))
        return User.from_db_row(rows[0]) if rows else None
    
    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        """Get user by username or email."""
        if "@" in identifier:
            return self.get_by_email(identifier)
        else:
            return self.get_by_username(identifier)
    
    def update(self, user: User) -> User:
        """Update user."""
        command = """
            UPDATE users 
            SET username = %s, password = %s, email = %s, facts_learned = %s,
                current_streak = %s, longest_streak = %s, total_facts_count = %s,
                last_activity_date = %s
            WHERE id = %s
        """
        params = (
            user.username, user.password, user.email, user.facts_learned,
            user.current_streak, user.longest_streak, user.total_facts_count,
            user.last_activity_date, user.id
        )
        
        self.execute_command(command, params)
        return user
    
    def update_progress(self, user_id: int, facts_learned: str, total_facts_count: int,
                       current_streak: int, longest_streak: int, last_activity_date: str) -> bool:
        """Update user progress fields efficiently."""
        command = """
            UPDATE users 
            SET facts_learned = %s, total_facts_count = %s, current_streak = %s,
                longest_streak = %s, last_activity_date = %s
            WHERE id = %s
        """
        params = (facts_learned, total_facts_count, current_streak, 
                 longest_streak, last_activity_date, user_id)
        
        return self.execute_command(command, params) > 0
    
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        command = "DELETE FROM users WHERE id = %s"
        return self.execute_command(command, (user_id,)) > 0
    
    def exists_username(self, username: str) -> bool:
        """Check if username exists."""
        query = "SELECT 1 FROM users WHERE username = %s"
        rows = self.execute_query(query, (username,))
        return len(rows) > 0
    
    def exists_email(self, email: str) -> bool:
        """Check if email exists."""
        if not email:
            return False
        query = "SELECT 1 FROM users WHERE email = %s"
        rows = self.execute_query(query, (email,))
        return len(rows) > 0
