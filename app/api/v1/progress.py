"""
Progress tracking API routes.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.dependencies import get_progress_service, get_current_user_id
from app.services.progress_service import ProgressService
from app.schemas.progress import ProgressResponse, CategoriesResponse

class SearchActivityRequest(BaseModel):
    """Schema for search activity tracking."""
    claim: str

class QuizActivityRequest(BaseModel):
    """Schema for quiz activity tracking."""
    claim: str
    questions_count: int = 0

class QuizAnswersRequest(BaseModel):
    """Schema for quiz answers tracking."""
    answers: List[str]
    correct_answers: List[str]

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.get("/", response_model=ProgressResponse)
def get_user_progress(
    user_id: int = Depends(get_current_user_id),
    progress_service: ProgressService = Depends(get_progress_service)
):
    """Get current user's progress data."""
    progress = progress_service.get_user_progress(user_id)
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User progress not found"
        )
    
    return ProgressResponse(**progress)

@router.get("/categories", response_model=CategoriesResponse)
def get_categories_breakdown(
    user_id: int = Depends(get_current_user_id),
    progress_service: ProgressService = Depends(get_progress_service)
):
    """Get user's fact categories breakdown for pie chart."""
    progress = progress_service.get_user_progress(user_id)
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User progress not found"
        )
    
    categories = progress.get("categories", {})
    total = sum(categories.values())
    
    return CategoriesResponse(categories=categories, total=total)

@router.post("/search")
def track_search_activity(
    request: SearchActivityRequest,
    user_id: int = Depends(get_current_user_id),
    progress_service: ProgressService = Depends(get_progress_service)
):
    """Track search activity for progress."""
    success = progress_service.add_search_fact(user_id, request.claim)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track search activity"
        )
    
    return {"message": "Search activity tracked successfully"}

@router.post("/quiz")
def track_quiz_activity(
    request: QuizActivityRequest,
    user_id: int = Depends(get_current_user_id),
    progress_service: ProgressService = Depends(get_progress_service)
):
    """Track quiz generation activity for progress."""
    success = progress_service.add_quiz_fact(user_id, request.claim, None, request.questions_count)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track quiz activity"
        )
    
    return {"message": "Quiz activity tracked successfully"}

@router.post("/quiz_answers")
def track_quiz_answers(
    request: QuizAnswersRequest,
    user_id: int = Depends(get_current_user_id),
    progress_service: ProgressService = Depends(get_progress_service)
):
    """Track quiz answers for progress."""
    success = progress_service.add_quiz_answers(user_id, request.answers, request.correct_answers)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track quiz answers"
        )
    
    return {"message": "Quiz answers tracked successfully"}
