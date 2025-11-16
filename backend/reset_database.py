"""
Reset Database Script
Run this if you encounter database schema errors after updating models
"""

import os
from sqlmodel import create_engine, SQLModel
from app.models import Session, Offer, Agreement

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

def reset_database():
    """Delete and recreate database with new schema"""
    # Delete existing database file
    if os.path.exists("data.db"):
        os.remove("data.db")
        print("✅ Deleted old database file")
    
    # Create new database with updated schema
    engine = create_engine(DATABASE_URL, echo=False)
    SQLModel.metadata.create_all(engine)
    print("✅ Created new database with updated schema")
    print("✅ Database reset complete!")

if __name__ == "__main__":
    print("⚠️  WARNING: This will delete all existing data!")
    response = input("Continue? (yes/no): ")
    if response.lower() == "yes":
        reset_database()
    else:
        print("Cancelled.")

