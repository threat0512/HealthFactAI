"""
Fact Card repository for database operations.
"""
from typing import Optional, List
# PostgreSQL support through database manager
from app.repositories.base import BaseRepository
from app.models.fact_card import FactCard

class FactCardRepository(BaseRepository[FactCard]):
    """Repository for fact card-related database operations."""
    
    def create(self, fact_card: FactCard) -> FactCard:
        """Create a new fact card."""
        command = """
            INSERT INTO fact_cards (user_id, title, summary, category, confidence, 
                                   sources, search_query, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        params = (
            fact_card.user_id,
            fact_card.title,
            fact_card.summary,
            fact_card.category,
            fact_card.confidence,
            fact_card.sources,
            fact_card.search_query
        )
        
        fact_card_id = self.execute_command_get_id(command, params)
        fact_card.id = fact_card_id
        return fact_card
    
    def get_by_id(self, fact_card_id: int) -> Optional[FactCard]:
        """Get fact card by ID."""
        query = """
            SELECT id, user_id, title, summary, category, confidence, sources, 
                   search_query, created_at, updated_at
            FROM fact_cards WHERE id = %s
        """
        rows = self.execute_query(query, (fact_card_id,))
        return FactCard.from_db_row(rows[0]) if rows else None
    
    def get_by_user_id(self, user_id: int, limit: int = 50, offset: int = 0) -> List[FactCard]:
        """Get all fact cards for a user, ordered by most recent first."""
        query = """
            SELECT id, user_id, title, summary, category, confidence, sources, 
                   search_query, created_at, updated_at
            FROM fact_cards 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        rows = self.execute_query(query, (user_id, limit, offset))
        return [FactCard.from_db_row(row) for row in rows]
    
    def get_by_user_and_category(self, user_id: int, category: str, 
                                 limit: int = 50, offset: int = 0) -> List[FactCard]:
        """Get fact cards for a user filtered by category."""
        if category.lower() == "all":
            return self.get_by_user_id(user_id, limit, offset)
        
        query = """
            SELECT id, user_id, title, summary, category, confidence, sources, 
                   search_query, created_at, updated_at
            FROM fact_cards 
            WHERE user_id = %s AND category = %s
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        rows = self.execute_query(query, (user_id, category, limit, offset))
        return [FactCard.from_db_row(row) for row in rows]
    
    def get_categories_for_user(self, user_id: int) -> List[str]:
        """Get all categories that have fact cards for a user."""
        query = """
            SELECT DISTINCT category 
            FROM fact_cards 
            WHERE user_id = %s 
            ORDER BY category
        """
        rows = self.execute_query(query, (user_id,))
        return [row[0] for row in rows]
    
    def count_by_user(self, user_id: int) -> int:
        """Count total fact cards for a user."""
        query = "SELECT COUNT(*) FROM fact_cards WHERE user_id = %s"
        rows = self.execute_query(query, (user_id,))
        return rows[0][0] if rows else 0
    
    def count_by_user_and_category(self, user_id: int, category: str) -> int:
        """Count fact cards for a user in a specific category."""
        if category.lower() == "all":
            return self.count_by_user(user_id)
        
        query = "SELECT COUNT(*) FROM fact_cards WHERE user_id = %s AND category = %s"
        rows = self.execute_query(query, (user_id, category))
        return rows[0][0] if rows else 0
    
    def update(self, fact_card: FactCard) -> FactCard:
        """Update an existing fact card."""
        command = """
            UPDATE fact_cards 
            SET title = %s, summary = %s, category = %s, confidence = %s, 
                sources = %s, search_query = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        params = (
            fact_card.title,
            fact_card.summary,
            fact_card.category,
            fact_card.confidence,
            fact_card.sources,
            fact_card.search_query,
            fact_card.id
        )
        
        self.execute_command(command, params)
        return fact_card
    
    def delete(self, fact_card_id: int) -> bool:
        """Delete a fact card."""
        command = "DELETE FROM fact_cards WHERE id = %s"
        return self.execute_command(command, (fact_card_id,)) > 0
    
    def delete_by_user(self, user_id: int) -> bool:
        """Delete all fact cards for a user."""
        command = "DELETE FROM fact_cards WHERE user_id = %s"
        return self.execute_command(command, (user_id,)) > 0
    
    def search_fact_cards(self, user_id: int, search_term: str, 
                         category: Optional[str] = None, limit: int = 50) -> List[FactCard]:
        """Search fact cards by title, summary, or search query."""
        base_query = """
            SELECT id, user_id, title, summary, category, confidence, sources, 
                   search_query, created_at, updated_at
            FROM fact_cards 
            WHERE user_id = %s AND (
                title LIKE %s OR 
                summary LIKE %s OR 
                search_query LIKE %s
            )
        """
        
        params = [user_id, f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"]
        
        if category and category.lower() != "all":
            base_query += " AND category = %s"
            params.append(category)
        
        base_query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)
        
        rows = self.execute_query(base_query, params)
        return [FactCard.from_db_row(row) for row in rows]
