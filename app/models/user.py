"""
User model and database operations.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date, timezone
import json
from dataclasses import dataclass

@dataclass
class User:
    """User model."""
    id: Optional[int] = None
    username: str = ""
    password: str = ""
    email: Optional[str] = None
    facts_learned: str = "[]"  # JSON string
    current_streak: int = 0
    longest_streak: int = 0
    total_facts_count: int = 0
    last_activity_date: Optional[str] = None  # ISO date string
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def facts_as_list(self) -> List[Dict[str, Any]]:
        """Get facts_learned as a parsed list."""
        try:
            return json.loads(self.facts_learned) if self.facts_learned else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    @facts_as_list.setter
    def facts_as_list(self, value: List[Dict[str, Any]]) -> None:
        """Set facts_learned from a list."""
        self.facts_learned = json.dumps(value, separators=(",", ":"))
    
    def add_fact(self, content: str, category: str, source_url: Optional[str] = None, 
                 fact_type: str = "general", **extra_data) -> None:
        """Add a new fact to the user's learned facts."""
        facts = self.facts_as_list
        new_fact = {
            "content": content,
            "category": category,
            "source_url": source_url,
            "learned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "type": fact_type,
            **extra_data
        }
        facts.append(new_fact)
        self.facts_as_list = facts
        self.total_facts_count += 1
    
    def get_category_breakdown(self) -> Dict[str, int]:
        """Get count of facts by category, filtered to only show health categories."""
        from app.schemas.health_categories import HealthCategory
        
        facts = self.facts_as_list
        categories = {}
        
        # Only include valid health categories
        valid_categories = {cat.value for cat in HealthCategory}
        
        for fact in facts:
            category = fact.get("category", "General")
            
            # Filter out non-health categories like "Quiz" and map to valid categories
            if category == "Quiz" or category == "quiz_answer":
                continue  # Skip quiz-related categories
            elif category not in valid_categories:
                category = "General"  # Map invalid categories to General
            
            categories[category] = categories.get(category, 0) + 1
        
        return categories
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "facts_learned": self.facts_learned,
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "total_facts_count": self.total_facts_count,
            "last_activity_date": self.last_activity_date,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_db_row(cls, row: tuple) -> "User":
        """Create User from database row."""
        if not row:
            return None
        
        # Assuming standard user table structure
        return cls(
            id=int(row[0]) if len(row) > 0 and row[0] is not None else None,
            username=str(row[1]) if len(row) > 1 and row[1] is not None else "",
            password=str(row[2]) if len(row) > 2 and row[2] is not None else "",
            email=str(row[3]) if len(row) > 3 and row[3] is not None else None,
            facts_learned=str(row[4]) if len(row) > 4 and row[4] is not None else "[]",
            current_streak=int(row[5]) if len(row) > 5 and row[5] is not None else 0,
            longest_streak=int(row[6]) if len(row) > 6 and row[6] is not None else 0,
            total_facts_count=int(row[7]) if len(row) > 7 and row[7] is not None else 0,
            last_activity_date=row[8] if len(row) > 8 else None
        )
