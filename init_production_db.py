"""
Simple database initialization for deployment.
Run this after deployment to create tables.
"""
import os
import psycopg

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL environment variable not set")
    exit(1)

def init_database():
    """Initialize database tables."""
    
    # SQL to create users table
    users_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE,
        facts_learned TEXT DEFAULT '[]',
        current_streak INTEGER DEFAULT 0,
        longest_streak INTEGER DEFAULT 0,
        total_facts_count INTEGER DEFAULT 0,
        last_activity_date VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # SQL to create fact_cards table
    fact_cards_table_sql = """
    CREATE TABLE IF NOT EXISTS fact_cards (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        category VARCHAR(100) DEFAULT 'General',
        source_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        # Connect to database
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                # Create tables
                cursor.execute(users_table_sql)
                cursor.execute(fact_cards_table_sql)
                conn.commit()
                print("✅ Database tables created successfully")
                
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Initializing production database...")
    if init_database():
        print("🎉 Database initialization completed!")
    else:
        print("❌ Database initialization failed!")
        exit(1)
