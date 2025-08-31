import psycopg

# Test Supabase connection
DATABASE_URL = "postgresql://postgres.smatauzvktsbxvjtesey:9Ds6tk95JdNAJ2XR@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

try:
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()
    print("Existing tables:", [t[0] for t in tables])
    
    # Check if users table exists
    cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'users');")
    users_exists = cursor.fetchone()[0]
    print(f"Users table exists: {users_exists}")
    
    conn.close()
    print("✅ Database connection and queries successful")
    
except Exception as e:
    print(f"❌ Error: {e}")
