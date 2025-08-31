"""
API v1 router initialization.
"""
from fastapi import APIRouter

# Import only auth for now to isolate the issue
from app.api.v1 import auth

# Create main API router
api_router = APIRouter()

# Include only auth router for testing
api_router.include_router(auth.router)

# Try to include others - comment out if they cause issues
try:
    from app.api.v1 import progress, search, quiz, fact_cards
    api_router.include_router(progress.router)
    api_router.include_router(search.router)
    api_router.include_router(quiz.router)
    api_router.include_router(fact_cards.router)
except Exception as e:
    print(f"Warning: Could not load some API modules: {e}")

# Health check endpoint
@api_router.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
