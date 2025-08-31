"""
Fact Card model for storing search results.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass
import json

@dataclass
class FactCard:
    """Fact Card model for storing search results."""
    id: Optional[int] = None
    user_id: int = 0
    title: str = ""
    summary: str = ""
    category: str = "General"
    confidence: Optional[str] = None
    sources: str = "[]"  # JSON string containing array of source objects
    search_query: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def sources_as_list(self) -> List[Dict[str, Any]]:
        """Get sources as a parsed list."""
        try:
            return json.loads(self.sources) if self.sources else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    @sources_as_list.setter
    def sources_as_list(self, value: List[Dict[str, Any]]) -> None:
        """Set sources from a list."""
        self.sources = json.dumps(value, separators=(",", ":"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert fact card to dictionary for API responses."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "summary": self.summary,
            "category": self.category,
            "confidence": self.confidence,
            "sources": self.sources_as_list,
            "search_query": self.search_query,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_fact_card_format(self) -> Dict[str, Any]:
        """Convert to frontend fact card format."""
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "category": self.category,
            "confidence": self.confidence,
            "sources": self.sources_as_list,
            "search_query": self.search_query,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_search_result(cls, user_id: int, search_query: str, search_result: Dict[str, Any]) -> "FactCard":
        """Create FactCard from search API result."""
        return cls(
            user_id=user_id,
            title=search_result.get("title", ""),
            summary=search_result.get("summary", ""),
            category=search_result.get("category", "General"),
            confidence=search_result.get("confidence", ""),
            sources=json.dumps(search_result.get("sources", []), separators=(",", ":")),
            search_query=search_query,
            created_at=datetime.now()
        )
    
    @classmethod
    def from_db_row(cls, row: tuple) -> "FactCard":
        """Create FactCard from database row."""
        if not row:
            return None
        
        return cls(
            id=int(row[0]) if len(row) > 0 and row[0] is not None else None,
            user_id=int(row[1]) if len(row) > 1 and row[1] is not None else 0,
            title=str(row[2]) if len(row) > 2 and row[2] is not None else "",
            summary=str(row[3]) if len(row) > 3 and row[3] is not None else "",
            category=str(row[4]) if len(row) > 4 and row[4] is not None else "General",
            confidence=str(row[5]) if len(row) > 5 and row[5] is not None else None,
            sources=str(row[6]) if len(row) > 6 and row[6] is not None else "[]",
            search_query=str(row[7]) if len(row) > 7 and row[7] is not None else "",
            created_at=datetime.fromisoformat(str(row[8]).replace('Z', '+00:00')) if len(row) > 8 and row[8] else None,
            updated_at=datetime.fromisoformat(str(row[9]).replace('Z', '+00:00')) if len(row) > 9 and row[9] else None
        )
