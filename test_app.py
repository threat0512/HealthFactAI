from main import create_application

try:
    app = create_application()
    print("✅ App created successfully")
    
    print("\nAll routes:")
    for route in app.routes:
        if hasattr(route, 'path'):
            methods = getattr(route, 'methods', 'N/A')
            print(f"  {methods} {route.path}")
        elif hasattr(route, 'routes'):  # For sub-routers
            for sub_route in route.routes:
                if hasattr(sub_route, 'path'):
                    methods = getattr(sub_route, 'methods', 'N/A')
                    print(f"  {methods} {sub_route.path}")
    
    print("\n✅ Route listing completed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
