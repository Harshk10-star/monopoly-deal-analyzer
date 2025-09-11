#!/usr/bin/env python3
"""
Deal Analyzer Pro - Combined Frontend + Backend Service
This serves both the React frontend and FastAPI backend from a single service.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_frontend():
    """Check if frontend static files exist"""
    backend_static = Path("backend/static")
    index_file = backend_static / "index.html"
    
    if index_file.exists():
        print("Frontend static files found!")
        return True
    else:
        print("ERROR: Frontend static files not found in backend/static/")
        print("Please run 'npm run build' in the frontend directory first.")
        return False

if __name__ == "__main__":
    # Check if frontend files exist
    if not check_frontend():
        sys.exit(1)
    
    # Add backend to Python path
    backend_path = Path(__file__).parent / "backend"
    sys.path.insert(0, str(backend_path))
    
    # Import and run the backend server
    from main_deploy import app
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Deal Analyzer Pro on port {port}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )