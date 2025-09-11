"""
Combined FastAPI app for Railway deployment
Serves both API and React frontend with no database dependencies
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os

# Import the stateless API
from main_stateless import app as api_app

# Create main app
app = FastAPI(
    title="Deal Analyzer Pro",
    description="AI-powered property card game analyzer",
    version="1.0.0"
)

# Mount the API routes
app.mount("/api", api_app)

# Serve static files (React build)
static_dir = Path(__file__).parent / "static"

if static_dir.exists():
    # Mount static assets
    assets_dir = static_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the React app"""
        return FileResponse(static_dir / "index.html")
    
    @app.get("/{path:path}")
    async def serve_frontend_routes(path: str):
        """Serve React app for all routes (SPA routing)"""
        # Check if it's a static file first
        file_path = static_dir / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        
        # For all other routes, return the React app (SPA routing)
        return FileResponse(static_dir / "index.html")
else:
    @app.get("/")
    async def root():
        return {
            "message": "Deal Analyzer Pro API",
            "status": "Frontend not built",
            "api_docs": "/docs",
            "api_health": "/api/health"
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Deal Analyzer Pro on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)