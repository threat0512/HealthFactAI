#!/usr/bin/env python3
"""
Database initialization script for HealthFactAI.
Creates necessary tables if they don't exist.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.database import db_manager
from app.core.config import settings

def create_users_table():
    """Create users table if it doesn't exist."""
    create_table_sql = """
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
    
    try:
        db_manager.execute_command(create_table_sql)
        print("✅ Users table created/verified successfully")
    except Exception as e:
        print(f"❌ Error creating users table: {e}")
        return False
    return True

def create_fact_cards_table():
    """Create fact_cards table if it doesn't exist."""
    create_table_sql = """
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
        db_manager.execute_command(create_table_sql)
        print("✅ Fact cards table created/verified successfully")
    except Exception as e:
        print(f"❌ Error creating fact_cards table: {e}")
        return False
    return True

def main():
    """Initialize the database."""
    print("🚀 Initializing HealthFactAI database...")
    print(f"📍 Database URL: {settings.DATABASE_URL[:50]}...")
    
    # Test database connection
    try:
        result = db_manager.execute_query("SELECT 1")
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Create tables
    success = True
    success &= create_users_table()
    success &= create_fact_cards_table()
    
    if success:
        print("🎉 Database initialization completed successfully!")
    else:
        print("⚠️ Some errors occurred during database initialization")

if __name__ == "__main__":
    main()
