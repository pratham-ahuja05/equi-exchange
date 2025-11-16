#!/usr/bin/env python3
"""
Database migration script to add blockchain fields to existing tables.
Run this script to update your database schema.
"""

import sqlite3
import os

def migrate_database():
    db_path = "data.db"
    
    if not os.path.exists(db_path):
        print("Database file not found. Creating new database with updated schema.")
        return
    
    print("Migrating database to add blockchain fields...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add blockchain fields to session table
        try:
            cursor.execute("ALTER TABLE session ADD COLUMN blockchain_tx_hash TEXT")
            print("Added blockchain_tx_hash to session table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("blockchain_tx_hash column already exists in session table")
            else:
                raise
        
        try:
            cursor.execute("ALTER TABLE session ADD COLUMN blockchain_block_number INTEGER")
            print("Added blockchain_block_number to session table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("blockchain_block_number column already exists in session table")
            else:
                raise
        
        # Add blockchain fields to agreement table
        try:
            cursor.execute("ALTER TABLE agreement ADD COLUMN blockchain_tx_hash TEXT")
            print("Added blockchain_tx_hash to agreement table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("blockchain_tx_hash column already exists in agreement table")
            else:
                raise
        
        try:
            cursor.execute("ALTER TABLE agreement ADD COLUMN blockchain_block_number INTEGER")
            print("Added blockchain_block_number to agreement table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("blockchain_block_number column already exists in agreement table")
            else:
                raise
        
        conn.commit()
        print("Database migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()