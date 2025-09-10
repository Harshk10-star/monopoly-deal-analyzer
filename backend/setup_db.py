#!/usr/bin/env python3
"""
Database setup script for Monopoly Deal Analyzer
"""

import os
import sys
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models.game import User, GameAnalysis, Payment

def setup_database():
    """Create all database tables"""
    
    print("Setting up Monopoly Deal Analyzer database...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # You can add sample data here if needed
        print("Database is ready for use!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("Make sure your database is running and DATABASE_URL is correct in .env file")
        return False
    
    return True

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check if DATABASE_URL is set
    if not os.getenv("DATABASE_URL"):
        print("❌ DATABASE_URL not found in environment variables")
        print("Please create a .env file with your database configuration")
        sys.exit(1)
    
    # Setup database
    if setup_database():
        print("\n🎉 Database setup completed successfully!")
        print("You can now start the backend server with: python start.py")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)



