"""
Database connection manager supporting both PostgreSQL and SQLite.
PostgreSQL is the primary choice for production, SQLite for development fallback.
"""
import os
from typing import Union, Optional
import sqlite3
import psycopg
from psycopg.rows import dict_row
from .config import settings

class DatabaseManager:
    """Database connection manager supporting both SQLite and PostgreSQL"""
    
    def __init__(self):
        self.db_type = settings.DB_TYPE
        self.connection = None
    
    def get_connection(self):
        """Get database connection based on configuration"""
        if settings.is_postgresql:
            return self._get_postgresql_connection()
        else:
            return self._get_sqlite_connection()
    
    def _get_postgresql_connection(self):
        """Get PostgreSQL connection with retry logic"""
        import time
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                if settings.DATABASE_URL and "postgresql" in settings.DATABASE_URL.lower():
                    # Use DATABASE_URL if provided (Supabase style)
                    return psycopg.connect(
                        settings.DATABASE_URL, 
                        row_factory=dict_row,
                        connect_timeout=10,
                        autocommit=False
                    )
                else:
                    # Use individual connection parameters
                    return psycopg.connect(
                        host=settings.DB_HOST,
                        dbname=settings.DB_NAME,
                        user=settings.DB_USER,
                        password=settings.DB_PASSWORD,
                        port=settings.DB_PORT,
                        row_factory=dict_row,
                        connect_timeout=10,
                        autocommit=False
                    )
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise Exception(f"PostgreSQL connection failed after {max_retries} attempts: {e}")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
    
    def _get_sqlite_connection(self):
        """Get SQLite connection (fallback)"""
        try:
            return sqlite3.connect(settings.DB_NAME)
        except Exception as e:
            raise Exception(f"SQLite connection failed: {e}")
    
    def execute_query(self, query: str, params: tuple = None):
        """Execute a SELECT query and return results"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return results
            else:
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def execute_command(self, command: str, params: tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE and return affected rows"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(command, params)
            else:
                cursor.execute(command)
            
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def execute_command_get_id(self, command: str, params: tuple = None) -> int:
        """Execute command and return the last inserted row ID"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(command, params)
            else:
                cursor.execute(command)
            
            conn.commit()
            
            if settings.is_postgresql:
                # PostgreSQL: get the last inserted ID using RETURNING clause or sequence
                if "RETURNING" in command.upper():
                    result = cursor.fetchone()
                    if isinstance(result, dict):
                        # psycopg3 with dict_row returns a dict
                        return list(result.values())[0]
                    else:
                        # tuple result
                        return result[0]
                else:
                    cursor.execute("SELECT lastval()")
                    result = cursor.fetchone()
                    if isinstance(result, dict):
                        return list(result.values())[0]
                    else:
                        return result[0]
            else:
                # SQLite: get the last inserted ID
                return cursor.lastrowid
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

# Global database manager instance
db_manager = DatabaseManager()
