"""
Debug script to test route registration and imports
"""
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    print("Testing imports...")
    
    # Test config import
    from app.core.config import settings
    print("✅ Config imported")
    print(f"API_V1_STR: {settings.API_V1_STR}")
    
    # Test database import
    from app.core.database import db_manager
    print("✅ Database manager imported")
    
    # Test dependencies
    from app.core.dependencies import get_auth_service
    print("✅ Dependencies imported")
    
    # Test auth service
    from app.services.auth_service import AuthService
    print("✅ Auth service imported")
    
    # Test auth router
    from app.api.v1.auth import router as auth_router
    print("✅ Auth router imported")
    print(f"Auth router prefix: {auth_router.prefix}")
    print(f"Auth router routes: {[route.path for route in auth_router.routes]}")
    
    # Test main API router
    from app.api.v1 import api_router
    print("✅ Main API router imported")
    print(f"Main router routes: {[route.path for route in api_router.routes]}")
    
    # Test main app creation
    from main import create_application
    app = create_application()
    print("✅ FastAPI app created")
    print("All routes:")
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"  {route.methods if hasattr(route, 'methods') else 'N/A'} {route.path}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
