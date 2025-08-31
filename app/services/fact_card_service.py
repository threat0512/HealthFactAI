"""
Fact Card service with business logic.
"""
from typing import List, Optional, Dict, Any
from app.models.fact_card import FactCard
from app.repositories.fact_card_repository import FactCardRepository
from app.schemas.health_categories import classify_health_claim

class FactCardService:
    """Service for fact card operations."""
    
    def __init__(self, fact_card_repository: FactCardRepository):
        self.fact_card_repository = fact_card_repository
    
    def save_search_result(self, user_id: int, search_query: str, 
                          search_result: Dict[str, Any]) -> Optional[FactCard]:
        """Save a search result as a fact card."""
        try:
            # Classify the search query to ensure proper categorization
            category = classify_health_claim(search_query)
            
            # Override the category in search result with our classification
            search_result["category"] = category.value
            
            # Create fact card from search result
            fact_card = FactCard.from_search_result(user_id, search_query, search_result)
            
            # Save to database
            return self.fact_card_repository.create(fact_card)
            
        except Exception as e:
            print(f"Error saving search result: {e}")
            return None
    
    def get_user_fact_cards(self, user_id: int, category: str = "All", 
                           limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get fact cards for a user, optionally filtered by category."""
        try:
            if category.lower() == "all":
                fact_cards = self.fact_card_repository.get_by_user_id(user_id, limit, offset)
            else:
                fact_cards = self.fact_card_repository.get_by_user_and_category(
                    user_id, category, limit, offset
                )
            
            # Convert to fact card format for frontend
            return [fact_card.to_fact_card_format() for fact_card in fact_cards]
            
        except Exception as e:
            print(f"Error getting user fact cards: {e}")
            return []
    
    def get_user_categories(self, user_id: int) -> List[str]:
        """Get all categories that have fact cards for a user."""
        try:
            categories = self.fact_card_repository.get_categories_for_user(user_id)
            # Always include "All" at the beginning
            if categories and "All" not in categories:
                categories.insert(0, "All")
            elif not categories:
                categories = ["All"]
            return categories
            
        except Exception as e:
            print(f"Error getting user categories: {e}")
            return ["All"]
    
    def search_fact_cards(self, user_id: int, search_term: str, 
                         category: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Search user's fact cards."""
        try:
            fact_cards = self.fact_card_repository.search_fact_cards(
                user_id, search_term, category, limit
            )
            return [fact_card.to_fact_card_format() for fact_card in fact_cards]
            
        except Exception as e:
            print(f"Error searching fact cards: {e}")
            return []
    
    def get_fact_card_stats(self, user_id: int) -> Dict[str, Any]:
        """Get statistics about user's fact cards."""
        try:
            total_cards = self.fact_card_repository.count_by_user(user_id)
            categories = self.fact_card_repository.get_categories_for_user(user_id)
            
            category_counts = {}
            for category in categories:
                count = self.fact_card_repository.count_by_user_and_category(user_id, category)
                category_counts[category] = count
            
            return {
                "total_fact_cards": total_cards,
                "categories": categories,
                "category_counts": category_counts
            }
            
        except Exception as e:
            print(f"Error getting fact card stats: {e}")
            return {
                "total_fact_cards": 0,
                "categories": ["All"],
                "category_counts": {}
            }
    
    def delete_fact_card(self, user_id: int, fact_card_id: int) -> bool:
        """Delete a fact card (with user ownership verification)."""
        try:
            # First verify the fact card belongs to the user
            fact_card = self.fact_card_repository.get_by_id(fact_card_id)
            if not fact_card or fact_card.user_id != user_id:
                return False
            
            return self.fact_card_repository.delete(fact_card_id)
            
        except Exception as e:
            print(f"Error deleting fact card: {e}")
            return False
