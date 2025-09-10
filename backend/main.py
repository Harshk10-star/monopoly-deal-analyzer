"""
Combined FastAPI app that serves both the API and the React frontend
Perfect for single-service deployment to Railway/Render/etc.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os

# Import your existing API code
from main_simple import app as api_app

# Create main app
app = FastAPI(
    title="Monopoly Deal Analyzer",
    description="Full-stack app with configuration system and AI analysis",
    version="1.0.0"
)

# Mount the API routes
app.mount("/api", api_app)

# Serve static files (React build)
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"

if frontend_dist.exists():
    app.mount("/static", StaticFiles(directory=frontend_dist / "assets"), name="static")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the React app"""
        return FileResponse(frontend_dist / "index.html")
    
    @app.get("/{path:path}")
    async def serve_frontend_routes(path: str):
        """Serve React app for all routes (SPA routing)"""
        file_path = frontend_dist / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        # Return index.html for SPA routing
        return FileResponse(frontend_dist / "index.html")
else:
    @app.get("/")
    async def root():
        return {
            "message": "Monopoly Deal Analyzer API",
            "frontend": "Build frontend first: cd frontend && npm run build",
            "api_docs": "/docs"
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)