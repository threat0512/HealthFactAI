"""
Fact Cards API routes.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel

from app.core.dependencies import get_current_user_id, get_fact_card_service
from app.services.fact_card_service import FactCardService

class SaveFactCardRequest(BaseModel):
    """Schema for saving a search result as fact card."""
    search_query: str
    search_result: dict
    
    class Config:
        schema_extra = {
            "example": {
                "search_query": "Benefits of vitamin C",
                "search_result": {
                    "title": "Vitamin C Benefits",
                    "summary": "Vitamin C supports immune system and acts as antioxidant...",
                    "category": "Nutrition",
                    "confidence": "92%",
                    "sources": [
                        {"name": "Harvard Health", "url": "https://health.harvard.edu"}
                    ]
                }
            }
        }

class FactCardResponse(BaseModel):
    """Schema for fact card response."""
    id: int
    title: str
    summary: str
    category: str
    confidence: Optional[str] = None
    sources: List[dict] = []
    search_query: str
    created_at: Optional[str] = None

class FactCardsListResponse(BaseModel):
    """Schema for list of fact cards."""
    fact_cards: List[FactCardResponse]
    total_count: int
    category: str
    has_more: bool

class FactCardStatsResponse(BaseModel):
    """Schema for fact card statistics."""
    total_fact_cards: int
    categories: List[str]
    category_counts: dict

router = APIRouter(prefix="/fact-cards", tags=["Fact Cards"])

@router.post("/save")
def save_fact_card(
    request: SaveFactCardRequest,
    user_id: int = Depends(get_current_user_id),
    fact_card_service: FactCardService = Depends(get_fact_card_service)
):
    """Save a search result as a fact card."""
    fact_card = fact_card_service.save_search_result(
        user_id, 
        request.search_query, 
        request.search_result
    )
    
    if not fact_card:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save fact card"
        )
    
    return {"message": "Fact card saved successfully", "id": fact_card.id}

@router.get("/", response_model=FactCardsListResponse)
def get_fact_cards(
    category: str = Query(default="All", description="Category to filter by"),
    limit: int = Query(default=20, ge=1, le=100, description="Number of cards to return"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    user_id: int = Depends(get_current_user_id),
    fact_card_service: FactCardService = Depends(get_fact_card_service)
):
    """Get user's fact cards, optionally filtered by category."""
    fact_cards = fact_card_service.get_user_fact_cards(user_id, category, limit, offset)
    
    # Get total count for pagination
    stats = fact_card_service.get_fact_card_stats(user_id)
    if category.lower() == "all":
        total_count = stats["total_fact_cards"]
    else:
        total_count = stats["category_counts"].get(category, 0)
    
    has_more = offset + limit < total_count
    
    return FactCardsListResponse(
        fact_cards=fact_cards,
        total_count=total_count,
        category=category,
        has_more=has_more
    )

@router.get("/categories")
def get_user_categories(
    user_id: int = Depends(get_current_user_id),
    fact_card_service: FactCardService = Depends(get_fact_card_service)
):
    """Get all categories that have fact cards for the user."""
    categories = fact_card_service.get_user_categories(user_id)
    return {"categories": categories}

@router.get("/stats", response_model=FactCardStatsResponse)
def get_fact_card_stats(
    user_id: int = Depends(get_current_user_id),
    fact_card_service: FactCardService = Depends(get_fact_card_service)
):
    """Get statistics about user's fact cards."""
    stats = fact_card_service.get_fact_card_stats(user_id)
    return FactCardStatsResponse(**stats)

@router.get("/search")
def search_fact_cards(
    q: str = Query(..., description="Search term"),
    category: Optional[str] = Query(default=None, description="Category to filter by"),
    limit: int = Query(default=20, ge=1, le=100, description="Number of results"),
    user_id: int = Depends(get_current_user_id),
    fact_card_service: FactCardService = Depends(get_fact_card_service)
):
    """Search user's fact cards."""
    fact_cards = fact_card_service.search_fact_cards(user_id, q, category, limit)
    
    return {
        "fact_cards": fact_cards,
        "search_term": q,
        "category": category,
        "total_results": len(fact_cards)
    }

@router.delete("/{fact_card_id}")
def delete_fact_card(
    fact_card_id: int,
    user_id: int = Depends(get_current_user_id),
    fact_card_service: FactCardService = Depends(get_fact_card_service)
):
    """Delete a fact card."""
    success = fact_card_service.delete_fact_card(user_id, fact_card_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fact card not found or access denied"
        )
    
    return {"message": "Fact card deleted successfully"}
