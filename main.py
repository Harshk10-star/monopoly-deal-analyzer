#!/usr/bin/env python3
"""
Deal Analyzer Pro - Combined Frontend + Backend Service
This serves both the React frontend and FastAPI backend from a single service.
"""

import os
import sys
import subprocess
from pathlib import Path

def build_frontend():
    """Build the React frontend if not already built"""
    frontend_dir = Path("frontend")
    dist_dir = frontend_dir / "dist"
    
    if not dist_dir.exists():
        print("Building frontend...")
        try:
            # Install frontend dependencies
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            # Build frontend
            subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
            print("Frontend built successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Frontend build failed: {e}")
            return False
    
    # Copy built frontend to backend static folder
    backend_static = Path("backend/static")
    backend_static.mkdir(exist_ok=True)
    
    if dist_dir.exists():
        import shutil
        if backend_static.exists():
            shutil.rmtree(backend_static)
        shutil.copytree(dist_dir, backend_static)
        print("Frontend copied to backend/static")
    
    return True

if __name__ == "__main__":
    # Build frontend first
    if not build_frontend():
        sys.exit(1)
    
    # Add backend to Python path
    backend_path = Path(__file__).parent / "backend"
    sys.path.insert(0, str(backend_path))
    
    # Import and run the backend server
    from main_combined import app
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Deal Analyzer Pro on port {port}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )