"""
Search API routes integrating existing search functionality.
"""
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.dependencies import get_current_user_id, get_search_service, get_fact_card_service
from app.services.search_service import SearchService
from app.services.fact_card_service import FactCardService

router = APIRouter(prefix="/search", tags=["Search"])

class SearchRequest(BaseModel):
    """Schema for search request."""
    claim: str
    
    class Config:
        schema_extra = {
            "example": {
                "claim": "Eating vegetables daily improves overall health"
            }
        }

class SearchResponse(BaseModel):
    """Schema for search response."""
    claim: str
    is_verified: bool
    explanation: str
    sources: List[dict]
    confidence: float
    
    class Config:
        schema_extra = {
            "example": {
                "claim": "Eating vegetables daily improves overall health",
                "is_verified": True,
                "explanation": "Scientific evidence supports this claim...",
                "sources": [
                    {
                        "title": "Nutrition Study",
                        "url": "https://example.com/study",
                        "snippet": "Research shows..."
                    }
                ],
                "confidence": 0.85
            }
        }

@router.post("/verify", response_model=SearchResponse)
def search_verified_claim(
    request: SearchRequest,
    user_id: int = Depends(get_current_user_id),
    search_service: SearchService = Depends(get_search_service),
    fact_card_service: FactCardService = Depends(get_fact_card_service)
):
    """Search and verify a health claim."""
    result = search_service.search_verified_claim(request.claim, user_id)
    
    # Automatically save the search result as a fact card
    try:
        # Convert search result to fact card format
        search_result_for_card = {
            "title": result["claim"],
            "summary": result["explanation"],
            "category": "Health Research",  # Will be classified by the service
            "confidence": f"{int(result['confidence'] * 100)}%",
            "sources": [
                {
                    "name": source.get("title", "Source"),
                    "url": source.get("url", "#")
                } for source in result["sources"]
            ]
        }
        
        # Save as fact card
        fact_card_service.save_search_result(user_id, request.claim, search_result_for_card)
    except Exception as e:
        # Don't fail the search if fact card saving fails
        print(f"Warning: Failed to save fact card: {e}")
    
    return SearchResponse(**result)

@router.get("/history")
def get_search_history(
    user_id: int = Depends(get_current_user_id),
    search_service: SearchService = Depends(get_search_service),
    limit: int = 10
):
    """Get user's search history."""
    return search_service.get_search_history(user_id, limit)
